#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode=True;

from netatomy.Enumerate import *
from pathlib import Path


class Device( Enumerate ):
  # TODO
  # environmental variables, Applications & Services,
  # Installed Applications, Scheduled Jobs, Users
  def __init__( self ):
    
    #super( ).__init__( )
    enum = super( )
    
    self.hostname = enum.hostname( )
    self.distro = enum.distro( )
    self.kernel = enum.kernel( )
    
    self.network = {
      # TODO -DHCP Server, DNS Server, Gateway
      'adapters': enum.interfaces( ),
      'ports': {
        'local': list( ),
        'remote': list( )
      },
      'connections': enum.arp( ),
    }

  ### Viewing/Debugging ###
  def __repr__(self): 
    import json
    return json.dumps( 
      vars( self ),
      ensure_ascii=False,
      sort_keys=False,
      indent=2
    )
  def toJSON( self ):
    return json.loads( self.__repr__( ) )
  def save( self ):
    Path( f'{self.hostname}.json' ).write_text(
      json.dumps(
        vars( self ),
        ensure_ascii=False,
        sort_keys=False,
        indent=2
      )
    )
  ### /Viewing/Debugging ###


'''
https://www.datacamp.com/community/tutorials/super-multiple-inheritance-diamond-problem
https://stackabuse.com/object-oriented-programming-in-python/
https://www.thegeekstuff.com/2019/03/python-oop-examples/
https://www.geeksforgeeks.org/object-oriented-programming-in-python-set-1-class-and-its-members/
https://python.swaroopch.com/oop.html
https://www.programiz.com/python-programming/object-oriented-programming
'''


