# -*- coding: UTF-8 -*-
# Copyright © 2017 Cornelius Grotjahn - This file is covered by the LICENCE file in the project root directory.
from   contextlib import contextmanager
import os
import queue
import threading
import time
from   typing import Dict

from abus import crypto
from abus import database

class IndexFile(object):
   """Open .lst file for recording all new backups. Use static `open` to create with context manager.
   Use `add_entry` for each new backup file."""
   def __init__(self, stream):
      self.lock= threading.Lock()
      self.stream= stream
   def add_entry(self, checksum, timestamp, path):
      with self.lock:
         print(checksum, timestamp, path, file=self.stream)
   @staticmethod
   @contextmanager
   def open(run_name, cfg, archive_dir):
      """Returns new `IndexFile` in a context manager"""
      d= cfg.archive_root_path+ "/"+archive_dir
      index_file_path= d+ "/"+run_name+".lst"
      partial_path= index_file_path+".part"
      os.makedirs(d, exist_ok=True)
      try:
         with crypto.open_txt(partial_path, "w", cfg.password) as stream:
            yield IndexFile(stream)
      except:
         os.unlink(partial_path)
         raise
      else:
         os.rename(partial_path, index_file_path)

class DeletionTracker(object):
   def __init__(self, indexdb:database.Database):
      """Creates objects representing all known paths (existing and known deleted).
      Caller removes paths that still exist from this list using seen()
      and marks the rest as deleted using complete()"""
      self.all_files= set(indexdb.get_undeleted_files())
      self.indexdb= indexdb
   def seen(self, path: str) -> None:
      """Marks a path as definitely existing"""
      self.indexdb.unmark_deleted(path)
      self.all_files.discard(path)
   def complete(self, index_file):
      """Marks all paths not previous seen() as deleted. Must only be called if caller is sure that all
      existing paths have been seen()"""
      if self.all_files:
         t= time.time()
         for p in self.all_files:
            index_file.add_entry("deleted", t, p)
         self.indexdb.mark_deleted(t, self.all_files)

def read_blocks(stream):
   """returns contents of binary files as list of byte-blocks"""
   block_size= 8192
   while True:
      block= stream.read(block_size)
      yield block
      if len(block) < block_size:
         break

class ArchiveDirsToUse(object):
   """List of spaces in archive subdirectories available for new backup files"""
   def __init__(self, initial_subdir_usage: Dict[str,int]):
      """List of spaces in archive subdirectories available for new backup files

      :param initial_subdir_usage: existing archive_dir -> n files therein
      """
      self.returns= queue.Queue()
      self.sequence= self._sequence(initial_subdir_usage)
   @staticmethod
   def _sequence(initial_subdir_usage):
      files_per_dir= 100
      for archive_dir, n in initial_subdir_usage.items():
         for _ in range(n, files_per_dir):
            yield archive_dir
      def mkdirname(n):
         least= "{:02}".format(n%100)
         return least if n<100 else least + "/" + mkdirname(n//100)
      n= -1
      while True:
         n += 1
         archive_dir= mkdirname(n)
         if archive_dir not in initial_subdir_usage:
            for _ in range(files_per_dir):
               yield archive_dir
   def get(self) -> str:
      """Returns archive subdirectory (relative to archive root) with space for one more backup files
      and reserves the space."""
      try:
         return self.returns.get_nowait()
      except queue.Empty:
         return next(self.sequence)
   @contextmanager
   def get_returnable(self):
      """Returns archive subdirectory like get() in a context manager, which returns the space on Exception."""
      archive_dir= self.get()
      try:
         yield archive_dir
      except:
         self.returns.put(archive_dir)
         raise
