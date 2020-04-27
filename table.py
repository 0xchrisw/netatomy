#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode=True;

import json
import xml.etree.ElementTree as elementTree
from pathlib import Path
import math
import html


connections = { }


def elem2str( elem ):
  elem = elementTree.tostring( elem, encoding='utf-8', method='html' )
  return html.unescape( elem.decode( ) )


def createTable( ):
  html_table = elementTree.Element( 'table' )
  table_attr = {
    'BORDER': '0',
    'CELLBORDER': '1',
    'CELLSPACING': '0',
    'ALIGN': 'CENTER',
    #'FIXEDSIZE': 'TRUE',
    #'HEIGHT': '300',
    #'WIDTH': '300'
  }
  for k, v in table_attr.items( ):
    html_table.set( k, v )
  return html_table


def createNode( device ):
  rows = [ ]
  cols = [ ]

  adapters = device['network']['adapters']
  adapter_count = len( adapters.keys( ) )
  if adapter_count % 2:
    adapter_count += 1


  html_table = createTable( )
  for i in range( math.ceil( adapter_count / 2 ) ):
    rows.append( elementTree.SubElement( html_table, "tr") )

  i = 0
  r = 0
  for k,v in adapters.items( ):
    row = rows[ r ]

    if i is 1:
      cell = elementTree.SubElement( row, 'td' )
      cell.set( 'port', 'hostname' )
      cell.set( 'rowspan', str( len( rows ) ) )
      cell.text = device[ 'hostname' ]

    cell = elementTree.SubElement( row, 'td' )
    cell.text = "<br/>".join( [ k, str( v[ 'ip' ] ), v[ 'mac' ], v[ 'vendor' ] ] )
    cell.set( 'port', str( i ) )
    if i % 2:
      r += 1
    connections[ k ] = i
    i += 1
  if len( adapters.keys( ) ) % 2:
    row = rows[ r ]
    cell = elementTree.SubElement( row, 'td' )
    row = rows[ r ]
    cell.set( 'port', str( i ) )
  return elem2str( html_table )



def createChild( device ):
  conns = device['network'][ 'connections' ]
  edges = [ ]
  nodes = [ ]

  n = 0
  for iface, links in conns.items( ):
    src = 'h1:' + str( connections[ iface ] )
    for link in links:
      table = createTable( )
      body = elementTree.SubElement( table, "tr")
      body.set( 'port', f'0' )
      cell = elementTree.SubElement( body, "td")
      cell.text = "<br/>".join( [
        link[ 'ip' ],
        link[ 'mac' ],
        link[ 'vendor' ]
      ] )
      nodes.append( elem2str( table ) )
      edges.append( ( src, f'n{n}:0' ) )
      n += 1
  print( edges )
  return nodes
  


dev = json.loads( Path( 'raspberrypi.json' ).read_text( ).strip( ) )
print(  createNode( dev ) )

print( '-' * 60 )

print( connections )

print( '-' * 60 )

print( createChild( dev ) )



# https://www.programcreek.com/python/index/1129/xml.etree.ElementTree

'''<
<TABLE
  BORDER="0"
  CELLBORDER="1"
  CELLSPACING="0"
  ALIGN="CENTER"
  FIXEDSIZE="TRUE"
  HEIGHT="300"
  WIDTH="300">
  <TR>
    <TD
      ALIGN="CENTER"
      FIXEDSIZE="TRUE"
      HEIGHT="300">{{INTERFACE}}</TD>
    <TD
      PORT="f1"
      ALIGN="CENTER"
      FIXEDSIZE="TRUE"
      HEIGHT="300">{{HOSTNAME}}</TD>
    <TD
      PORT="f2"
      ALIGN="CENTER"
      FIXEDSIZE="TRUE"
      HEIGHT="300">{{INTERFACE}}</TD>
  </TR>
</TABLE>>'''
