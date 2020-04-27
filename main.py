#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode=True;

from netatomy import *


host = Device( )
host.save( )
#print( host )

'''
import json
from graphviz import Digraph

def Graph( host_data ):
  nodes = [ ]
  edges = [ ]

  network     = host_data.network
  #connections = network[ 'connections' ]
  #LAN         = connections[ 'LAN' ]
  #print( LAN )

  adapters = network[ 'adapters' ]
  #for adapter in adapters:
  #  
  #root = { 'ip': network[''] }
  #nodes.append( root )
  pass

Graph( host )
'''

'''
TODO
  o https://www.kernel.org/doc/Documentation/sysctl/kernel.txt
     - /proc/sys/kernel/domainname
     - 
  o https://www.kernel.org/doc/Documentation/sysctl/net.txt
  o https://www.kernel.org/doc/Documentation/sysctl/user.txt
  o https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
'''


