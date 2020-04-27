#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode=True;

import os
import sys 
import time

import psutil
import subprocess

def checkIfProcessRunning( processName ):
  '''
  Check if there is any running process that contains the given name processName.
  '''
  #Iterate over the all the running process
  for proc in psutil.process_iter():
    try:
      # Check if process name contains the given name string.
      if processName.lower() in proc.name().lower():
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass
  return False;


def findProcessIdByName(processName):
  '''
  Get a list of all the PIDs of a all the running process whose name contains
  the given string processName
  '''

  listOfProcessObjects = []

  #Iterate over the all the running process
  for proc in psutil.process_iter():
    try:
      pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
      # Check if process name contains the given name string.
      if processName.lower() in pinfo['name'].lower() :
        listOfProcessObjects.append(pinfo)
    except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
      pass
  return listOfProcessObjects;
  


class Watcher(object):
  running = True
  refresh_delay_secs = 6

  # Constructor
  def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
    self._cached_stamp = 0
    self.filename = watch_file
    self.call_func_on_change = call_func_on_change
    self.args = args
    self.kwargs = kwargs

  # Look for changes
  def look(self):
    stamp = os.stat(self.filename).st_mtime
    if stamp != self._cached_stamp:
      self._cached_stamp = stamp
      # File has changed, so do something...
      print('File changed')
      if self.call_func_on_change is not None:
        #self.call_func_on_change(*self.args, **self.kwargs)
        #self.call_func_on_change( )
        self.call_func_on_change( self.filename )

  # Keep watching in a loop    
  def watch(self):
    while self.running: 
      try: 
        # Look for changes
        time.sleep(self.refresh_delay_secs) 
        self.look() 
      except KeyboardInterrupt: 
        print('\nDone') 
        break 
      except FileNotFoundError:
        # Action on file not found
        pass
      except: 
        print('Unhandled error: %s' % sys.exc_info()[0])


import importlib
def unreload( watch_file, first_run=False ):
  watch_module = watch_file.replace( '.py', '' )
  #if first_run:
  #  __import__( watch_module )
  try:
    if watch_module in sys.modules:
      print( '=' * 39 )
      print( 'ACTION: Reloading module...' )
      importlib.reload( sys.modules[ watch_module ] )
      #del sys.modules[ watch_module ]
      
      ######## TODO ########
      #if checkIfProcessRunning( 'ImageMagick' ):
        #for pid in findProcessIdByName( 'ImageMagick' ):
        #print( 'RUNNING')
        #subprocess.call( ['pkill', 'ImageMagick' ] )
    else:
      __import__( watch_module )
      ## Handle `from X import Y` case
      ## METHOD 1:
      ##foo = reload(foo); from foo import *
      ## METHOD 2
      ##for name in names:
      ##  globals()[name] = getattr(sys.modules[module_name], name)
      ##__import__( watch_module, fromlist=names )
  except Exception as e:
    print( 'EXCEPTION: Error occured importing watch file.' )
    print( e )
    


watch_file = 'map.py';

#unreload( watch_file, True )

watcher = Watcher( watch_file, unreload )
watcher.watch( )  # start the watch going



'''
#watch_file = 'my_file.txt'
#watcher = Watcher(watch_file)  # simple
#watcher = Watcher(watch_file, custom_action, text='yes, changed')  # also call custom action function
#watcher.watch()  # start the watch going

https://stackoverflow.com/questions/182197/how-do-i-watch-a-file-for-changes
http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
https://stackoverflow.com/questions/437589/how-do-i-unload-reload-a-module
https://learning.oreilly.com/library/view/python-cookbook/0596001673/ch14s02.html
'''

'''
TODO
Version Detection
from sys import version_info
if version_info[0] < 3:
    pass # Python 2 has built in reload
elif version_info[0] == 3 and version_info[1] <= 4:
    from imp import reload # Python 3.0 - 3.4 
else:
    from importlib import reload # Python 3.5+
'''


