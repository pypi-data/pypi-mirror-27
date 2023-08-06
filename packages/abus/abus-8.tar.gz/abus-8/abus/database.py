# -*- coding: UTF-8 -*-
# Copyright © 2017 Cornelius Grotjahn - This file is covered by the LICENCE file in the project root directory.
from   contextlib import contextmanager
import logging
import os.path
import queue
import re
import shutil
import sqlite3
import sys
import time
from   typing import Callable, Iterable, Tuple

from abus.cornelib import Schapp
from abus.rebuild import find_index_files, find_compressed_backups

class connect:
   def __init__(self, database_path, archive_root_path, allow_create=False):
      """
      Returns an object for the index database.

      :param database_path:
      :param allow_create: whether blank database should be created if `database_path` does not exist.
      :rtype: Database
      """
      self.db= Database(database_path, archive_root_path, allow_create)
   def __enter__(self):
      return self.db
   def __exit__(self, exc_type, exc_val, exc_tb):
      self.db.close()

class DeletionTracker(object):
   def __init__(self, connection_generator: Callable[[],sqlite3.Connection]):
      """Creates objects representing all known paths (existing and known deleted).
      Caller removes paths that still exist from this list using seen()
      and marks the rest as deleted using complete()"""
      self.get_connection= connection_generator
      with self.get_connection() as conn:
         self.all_files= set(path for (path,) in conn.execute("""select distinct path from content"""))
         self.deleted= set(path for (path,) in conn.execute("""select path from deletion"""))
         self.all_files.difference_update(self.deleted)
   def seen(self, path: str) -> None:
      """Marks a path as definitely existing"""
      if path in self.deleted:
         with self.get_connection() as conn:
            conn.execute("delete from deletion where path=?", [path])
      self.all_files.discard(path)
   def complete(self):
      """Marks all paths not previous seen() as deleted. Must only be called if caller is sure that all
      existing paths have been seen()"""
      if self.all_files:
         t= time.time()
         with self.get_connection() as conn:
            conn.executemany("""insert into deletion(path, timestamp) values(?,?)""",
                             ((p,t) for p in self.all_files))
            conn.executemany("delete from last_checksummed where path=?",
                             ((p,)for p in self.all_files))

class Database(object):
   def __init__(self, database_path, archive_root_path, allow_create):
      self.dbpath= database_path
      existed= os.path.exists(database_path)
      if not existed and not allow_create:
         raise RuntimeError("could not find database "+database_path)
      self.connection_pool_size= 0
      self.connection_pool= queue.Queue()
      self._set_connection_pool_size(1)
      self._check_schema(archive_root_path)
   def close(self):
      self._set_connection_pool_size(0)

   def _set_connection_pool_size(self, n):
      while self.connection_pool_size < n:
         conn= sqlite3.connect(self.dbpath, timeout=60, check_same_thread=False)
         conn.isolation_level= None # autocommit
         conn.execute("PRAGMA synchronous=OFF")
         self.connection_pool.put(conn)
         self.connection_pool_size += 1
      while self.connection_pool_size > n:
         self.connection_pool.get().close()
         self.connection_pool_size -= 1

   @contextmanager
   def _get_connection(self):
      """
      Returns a connection object from the pool with context manager.

      :rtype:sqlite3.Connection
      """
      conn= self.connection_pool.get()
      try:
         yield conn
      finally:
         self.connection_pool.put(conn)

   def _check_schema(self, archive_root_path):
      abus_src_dir= os.path.dirname(__file__)
      schema_file_path= abus_src_dir+"/schema.sql"
      upgrade_file_name_pattern= re.compile(r"upgrade-([0-9]+)[.]sql")
      upgrade_file_paths= sorted(
         direntry.path for direntry in os.scandir(abus_src_dir)
         if upgrade_file_name_pattern.match(direntry.name))

      def get_legacy_version(conn: sqlite3.Connection) -> str:
         """Returns script that backfills DB vesion, if necessary"""
         # did not have version table in versions <= 2.4, may need to find out manually if version is 0,1,or 2
         tables= set(conn.execute("select name from sqlite_master where type='table'").fetchall())
         if ("completed_run",) in tables:
            return "2"
         elif ("run",) in tables:
            return "1"
         else:
            return "0" # blank database

      with self._get_connection() as conn:
         schapp= Schapp(conn, schema_file_path, upgrade_file_paths, get_legacy_version)
         if not schapp.requires_upgrade:
            return

      logging.info("index database needs upgrading")
      print("index database needs upgrading - this may take a while", file=sys.stderr)
      with self._take_backup():
         with self._get_connection() as conn:
            schapp.perform_upgrade(conn)
            if 0 < schapp.preupgrade_major_version < 3:
               # need to fill-in new columns from archive directory scan
               logging.info("reconstructing new index data")
               print("reconstructing new index data", file=sys.stderr)
               data= ((archive_dir, run_name) for run_name,archive_dir in find_index_files(archive_root_path))
               conn.executemany("update run set archive_dir= ? where run_name = ?", data)
               data= ((checksum,) for checksum in find_compressed_backups(archive_root_path))
               conn.executemany("update location set is_compressed= 1 where checksum = ?", data)

   @contextmanager
   def _take_backup(self):
      """Context manager that creates a backup copy of the database and
      restores or deletes it on exit
      depending on whether an exception has been raised"""
      connection_pool_size= self.connection_pool_size
      self._set_connection_pool_size(0)
      backup= self.dbpath + ".backup"
      logging.info("taking backup of index database")
      shutil.copyfile(self.dbpath, backup)
      self._set_connection_pool_size(1)
      try:
         yield
      except:
         self._set_connection_pool_size(0)
         logging.info("index database upgrade failed, restoring backup")
         shutil.copyfile(backup, self.dbpath)
         os.unlink(backup)
         raise
      else:
         os.unlink(backup)
         self._set_connection_pool_size(connection_pool_size)

   def _make_runname(self, timestamp):
      tm= time.localtime(timestamp)
      # format chosen to make the run name a "word" in most editors:
      return time.strftime("%Y_%m_%d_%H%M", tm)

   def open_backup_run(self, archive_dir):
      run_name= self._make_runname(time.time())
      with self._get_connection() as conn:
         n= conn.execute("select count(*) from run where run_name=?", [run_name]).fetchall()[0][0]
      if n>0:
         raise RuntimeError("There is already a run with the current timestamp (minute granularity")
      conn.execute("insert into run(run_name, archive_dir) values(?,?)", [run_name, archive_dir])
      return run_name

   def get_archivedir_usage(self):
      with self._get_connection() as conn:
         rows= conn.execute("select archive_dir, count(*) as n from location group by archive_dir")
         counts= {archive_dir:n for archive_dir,n in rows}
         rows= conn.execute("select archive_dir, count(*) as n from run group by archive_dir")
         for archive_dir, n in rows:
            counts[archive_dir]= counts.get(archive_dir, 0) + n
         return counts

   def get_deletion_tracker(self) -> DeletionTracker:
      """Returns objects representing all known paths (existing and known deleted).
      Caller removes paths that still exist from this list using seen()
      and marks the rest as deleted using complete()"""
      return DeletionTracker(self._get_connection)

   def is_file_unchanged(self, path: str, st_dev: int, st_ino: int, mtime: float, ctime: float) -> bool:
      """Whether the given path's metadata is unchanged since the last call to remember_latest_version,
      indicating that the file content is also unchanged and the file need not be backed up"""
      if st_dev>=2**63: st_dev -= 2**64 # sqlite cannot handle u64
      if st_ino>=2**63: st_ino -= 2**64
      with self._get_connection() as conn:
         rs= conn.execute("""select 1
            from last_checksummed
            where path=? and st_dev=? and st_ino=? and mtime=? and ctime=?""",
               (  path,      st_dev,      st_ino,      mtime,      ctime)).fetchall()
      return len(rs)==1

   def remember_file_metadata(self, path: str, st_dev: int, st_ino: int, mtime: float, ctime: float) -> None:
      """Stores metadata for path so that any change can be detected in future backups"""
      if st_dev>=2**63: st_dev -= 2**64 # sqlite cannot handle u64
      if st_ino>=2**63: st_ino -= 2**64
      with self._get_connection() as conn:
         cur= conn.execute("""
            update last_checksummed
            set st_dev=?, st_ino=?, mtime=?, ctime=? where path=?""",
               (st_dev,   st_ino,   mtime,   ctime,        path))
         if cur.rowcount==0:
            conn.execute("insert into last_checksummed(path, st_dev, st_ino, mtime, ctime) values(?,?,?,?,?)",
                                                      (path, st_dev, st_ino, mtime, ctime))

   def have_checksum(self, checksum: str) -> bool:
      """whether there is an existing backup for the given checksum"""
      with self._get_connection() as conn:
         rs= conn.execute("select archive_dir from location where checksum=?", [checksum]).fetchall()
      return len(rs)==1

   def remember_archivedir(self, checksum, archive_dir_rel, is_compressed):
      with self._get_connection() as conn:
         conn.execute("insert into location(checksum, archive_dir, is_compressed) values(?,?,?)",
                      (checksum, archive_dir_rel, is_compressed))

   def add_backup_entry(self, run_name: str, path: str, timestamp: float, checksum: str) -> bool:
      """Creates a new content entry unless the previous entry for the `path` has the same data.

      :returns: whether new entry was created"""
      with self._get_connection() as conn:
         prev= conn.execute("""select timestamp, checksum
            from content
            where path = ?
            order by run_name desc
            limit 1""", [path]).fetchall()
         if prev and prev == [(timestamp, checksum)]:
            return False
         conn.execute("""insert into content(run_name, path, timestamp, checksum)
            values(?,?,?,?)""", (run_name, path, timestamp, checksum))
         return True

   def get_all_backup_files(self):
      """
      Returns list of all checksums in backup

      :rtype: ((checksum, archive_dir, is_compressed))
      """
      with self._get_connection() as conn:
         return conn.execute("select checksum, archive_dir, is_compressed from location")

   def get_all_runs(self):
      """
      Returns list of all runs in DB

      :rtype: ((run_name, archive_dir))
      """
      with self._get_connection() as conn:
         return conn.execute("select run_name, archive_dir from run")

   def get_archive_contents(self, patterns, cutoff_date, show_all: bool) -> Iterable[Tuple[str,float,str,str,int]]:
      """
      Returns content of archive for listing or restore.

      :param patterns: glob-operator patterns for path to match any of
      :type patterns: string list
      :param cutoff_date: time from which files are ignored or None
      :type cutoff_date: time.time() format
      :param show_all: whether all files should be returned rather than just those from the latest run
      :returns: (path, timestamp, archive_dir, checksum, is_compressed)s
      """
      with self._get_connection() as conn:
         sql= "select distinct path, min(timestamp), archive_dir, content.checksum, is_compressed from content"
         sql_args= []
         where_clauses= [] # to be built now but added later
         where_args= []

         if cutoff_date is None:
            if show_all:
               # show all without cutoff date is just everything
               pass
            else:
               # show one without cutoff means latest run
               where_clauses.append("run_name = (select max(run_name) from content)")
         else:
            if show_all:
               # show all with cutoff date
               where_clauses.append("timestamp <= ?")
               where_args.append(cutoff_date)
            else:
               # show one with cutoff date requires subquery for the latest
               sql += " join (select path as p, max(timestamp) as t from content "
               sql +=       " where timestamp <= ?"
               sql_args.append(cutoff_date)
               sql +=       " group by path) as latest"
               sql +=  " on path = latest.p and timestamp = latest.t"

         sql += " join location on location.checksum = content.checksum"

         if patterns:
            where_clauses.append("("
               +" or ".join("path glob ?" for x in patterns)
               +")")
            where_args.extend(patterns)

         if where_clauses:
            sql += " where " + " and ".join(where_clauses)
            sql_args.extend(where_args)

         sql += " group by path, archive_dir, content.checksum"
         sql += " order by path, min(timestamp) desc"
         yield from conn.execute(sql, sql_args)

   def rebuild_location_table(self, actual_content_list: Iterable[Tuple[str, str, bool]]) -> Tuple[int, int, int]:
      """
      Adjusts the location table to reflect data in dictionary.

      :param actual_content_list: (checksum, archive_dir, is_compressed)s of required state
      :type actual_content_list: iterable
      :returns: counts: (updates, inserts, deletes)
      """
      actual_content= {checksum:(archive_dir,is_compressed)
                       for checksum,archive_dir,is_compressed in actual_content_list}
      updates= []
      deletes= []
      with self._get_connection() as conn:
         conn.execute("delete from deletion")
         for checksum,archive_dir,is_compressed in conn.execute("select checksum, archive_dir, is_compressed from location"):
            # leaving actual_content with all records that are not in database:
            actual_values= actual_content.get(checksum)
            if actual_values is None:
               deletes.append((checksum,))
            else:
               del actual_content[checksum]
               if actual_values!=(archive_dir,is_compressed!=0):
                  archive_dir, is_compressed= actual_values
                  updates.append((archive_dir, is_compressed, checksum))
         conn.executemany("delete from location where checksum = ?", deletes)
         conn.executemany("update location set archive_dir= ?, is_compressed= ? where checksum = ?", updates)
         data= ((k,a,b) for k,(a,b) in actual_content.items())
         conn.executemany("insert into location(checksum,archive_dir,is_compressed) values(?,?,?)", data)
      return len(updates), len(actual_content), len(deletes)

   def rebuild_content(self, run_name:str, run_archive_dir:str,
                       checksum_timestamp_path_rows: Iterable[Tuple[str,str,str]]) -> Tuple[int,int,int]:
      """
      Replaces all rows in content table for a given run_name with the given values.
      All calls from a single rebuild must be in order of run_name.

      :param run_name:Run whose content rows will all be deleted and then replaced.
      :param run_archive_dir: The relative dir containing the run file
      :param checksum_timestamp_path_rows: New rows (without run_nam column itself)
      :return: number of records changed, added, deleted
      """
      typed_ctp= ((c,float(t),p) for c,t,p in checksum_timestamp_path_rows)
      with self._get_connection() as conn:
         conn.execute("""create temp table if not exists required_content(
            path text not null primary key,
            timestamp float not null,
            checksum text not null)""")
         conn.execute("delete from required_content")
         conn.executemany("insert into required_content(checksum, timestamp, path) values(?,?,?)", typed_ctp)
         conn.execute("delete from required_content where checksum='error'")
         conn.execute("delete from required_content where checksum not in(select checksum from location)")
         conn.execute("""delete from required_content 
            where rowid in(select required_content.rowid 
               from (select path, max(run_name) as prev_run 
                     from content
                     where run_name < ? 
                     group by path
                     ) as LATEST
                  join content on content.run_name = LATEST.prev_run and content.path = LATEST.path
                  join required_content on required_content.path = content.path 
                     and required_content.checksum = content.checksum 
                     and required_content.timestamp = content.timestamp)""", [run_name])
         changed= conn.execute("""select count(*)
            from content join required_content on content.path=required_content.path
               and (content.checksum!=required_content.checksum or content.timestamp!=required_content.timestamp)
            where content.run_name=?""", [run_name]).fetchall()[0][0]
         new= conn.execute("""select count(*)
            from required_content left join content on content.path=required_content.path and content.run_name=?
            where content.path is null""", [run_name]).fetchall()[0][0]
         removed= conn.execute("""select count(*)
            from content left join required_content on required_content.path = content.path
            where content.run_name=? and required_content.path is null""", [run_name]).fetchall()[0][0]
         conn.execute("delete from content where run_name=?", [run_name])
         conn.execute("""insert into content(run_name, path, timestamp, checksum)
            select ?, path, timestamp, checksum from required_content""", [run_name])
         exists= conn.execute("select archive_dir from run where run_name=?", [run_name]).fetchall()
         if len(exists)==0:
            new += 1
            conn.execute("""insert into run(run_name, archive_dir) values(?,?)""",
                         (run_name, run_archive_dir))
         elif exists[0]!=(run_archive_dir,):
            changed += 1
            conn.execute("""update run set archive_dir= ? where run_name=?""",
                         (run_archive_dir, run_name))
      return changed, new, removed

   def remove_runs(self, other_than: Iterable[str]):
      """
      Removes all runs from content and completed_runs, whose run_name is not in `other_than`

      :return: number of deleted rows
      """
      other_than= list(other_than)
      place_holders= ",?" * len(other_than)
      n= 0
      with self._get_connection() as conn:
         for table in "run", "content":
            stmt= "delete from "+table+" where run_name not in("+place_holders[1:]+")"
            cur= conn.execute(stmt, other_than)
            n += cur.rowcount
      return n

   def remove_location_entry(self, checksum):
      """
      Reflects in DB that a backup file has been deleted

      :param checksum: of deleted location file
      """
      with self._get_connection() as conn:
         conn.execute("delete from content where checksum=?", [checksum])
         conn.execute("delete from deletion where path not in(select path from content)")
         conn.execute("delete from location where checksum=?", [checksum])

   def get_purgeable_backups(self, rounders):
      """
      Returns list of backup files that are superfluous and to be deleted.

      :param: rounders: retention policy definition: (rounder,age)-list
      :return:  (checksum, archive_dir, path, timestamp)-list
      """
      case_clause= "case " +"when timestamp >= ? then cast(timestamp/? as int)*? "*len(rounders) +"else 0 end"
      now= time.time()
      params= []
      for r,a in sorted(rounders):
         params.extend([now-a*86400, r*86400, r*86400])
      params.append(params[-3]) # slot 0 threshold for EXCEPTION_FOR_DELETED

      with self._get_connection() as conn:
         cur= conn.execute("""
            with SLOTTED as(
                  select distinct path, timestamp, """+case_clause+""" as slot
                  from content
                  )
               ,LONG_DELETED as(
                  select deletion.path
                  from deletion
                     join SLOTTED on SLOTTED.path = deletion.path
                  where deletion.timestamp < ?
                  group by deletion.path
                  having count(SLOTTED.path)=1 and max(SLOTTED.slot)=0
                  )
               ,KEEP_VERSIONS as(
                  select path, max(timestamp) as timestamp
                  from SLOTTED
                  where path not in(select path from LONG_DELETED)
                  group by path, slot
                  )
               ,KEEP_CHECKSUMS as(
                  select distinct content.checksum
                  from content join KEEP_VERSIONS on content.path = KEEP_VERSIONS.path
                     and content.timestamp = KEEP_VERSIONS.timestamp
                  )
               ,PURGE as(
                  select distinct location.checksum, location.archive_dir, content.path, content.timestamp
                  from location
                     join content on content.checksum = location.checksum
                  where location.checksum not in(select checksum from KEEP_CHECKSUMS)
                  )
            select *
            from PURGE
            order by checksum, path, timestamp
            """, params)
         result= cur.fetchall()
      return result

   def purge_runs(self, run_names: Iterable[str]) -> None:
      """
      Purges given runs after checking that they can be purged.
      """
      run_names= set(run_names)
      run_names.intersection_update(r for r,a in self.get_purgeable_runs())
      run_names= list(run_names)
      if run_names:
         place_holders= ",?" * len(run_names)
         with self._get_connection() as conn:
            for table in ("run", "content"):
               conn.execute("delete from {} where run_name in({})".format(table, place_holders[1:]), run_names)

   def get_purgeable_runs(self) -> Iterable[Tuple[str,str]]:
      """
      Returns runs that can be purged.

      :returns: (run_name, archive_dir)s
      """
      with self._get_connection() as conn:
         return conn.execute("""
            select run_name, archive_dir
            from run
            where run_name not in(select run_name
                  from content join location on location.checksum = content.checksum)
               and run_name <> (select max(run_name) from run)""")
