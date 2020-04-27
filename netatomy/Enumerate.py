#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode=True;

import json
from pathlib import Path
import socket, struct, fcntl


class Enumerate( object ):
  # TODO - file file paths
  OUIDB = json.loads( Path( 'netatomy/OUI.json' ).read_text( ) )

  ### Utils ###
  def read( self, f ):
    return Path( f ).read_text( ).strip( )
  ### /Utils ###


  ####################################################################################
  #
  def hostname( self ):
    return Path( '/proc/sys/kernel/hostname' ).read_text( ).strip( )
  ####################################################################################
  

  ####################################################################################
  #
  def kernel( self ):
    #return self.read( '/proc/version' )
    return self.read( '/proc/sys/kernel/osrelease' )
  ####################################################################################


  ####################################################################################
  #
  def distro( self ):
    release = self.read( '/etc/os-release' ).split( "\n" )[0].replace( '"', '' )
    return release.split( '=')[1]    
  ####################################################################################
  
  
  ####################################################################################
  #
  def iface_addr(  self, ifname ):
    try:
      #s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      return socket.inet_ntoa( fcntl.ioctl(
               s.fileno( ),
               0x8915,  # SIOCGIFADDR
               struct.pack( '256s', ifname.encode( 'utf-8' ) )
            )[ 20:24 ])
    except:
      return None

  def OUI(  self, MAC ):
    OUIDB = self.OUIDB
    prefix = MAC[ :8 ].replace( ':', '-' )
    if prefix in OUIDB:
      return " ".join( OUIDB[ prefix ] ).strip( )
    else:
      return 'Unknown'

  def interfaces( self ):
    # https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-net
    adapters = { }

    for iface in Path( '/sys/class/net/' ).iterdir( ):
      name = iface.parts[ -1 ]
      mac = self.read( f'{iface}/address' ).upper( )
      adapters[ name ] = {
        'ip':  self.iface_addr( name ),
        'mac': mac,
        'state': ( 'DOWN', 'UP' )[ int( self.read( f'{iface}/carrier' ) ) ],
        'mtu': self.read( f'{iface}/mtu' ),
        'vendor': self.OUI( mac )
      }
    return adapters
  ####################################################################################


  ####################################################################################
  #
  def arp( self ):
    # for i in {1..254} ;do (ping -c 1 192.168.1.$i | grep "bytes from" &) ;done
    #route_table = self.read( '/proc/net/fib_trie' )
    table = { }

    arp_table = self.read( '/proc/net/arp' ).split( "\n" )[ 1: ]
    for entry in arp_table:
      try:
        ip, _, _, mac, _, iface = entry.split( )
        table.setdefault( iface, [ ] ).append( {
          'ip':     ip,
          'mac':    mac,
          'iface':  iface,
          'vendor': self.OUI( mac )
        } )
        '''
        table[ ip ] = {
          'MAC':    mac,
          'iface':  iface,
          'vendor': self.OUI( mac )
        }
        '''
        #table.setdefault( 'iface', [ ] ).append( ) 
      except Exception as e:
        print( e )
        pass
    return table
    

  def arpScan( self ):
    '''
    interfaces = self.interfaces( )
    for iface, attr in interfaces.items( ):
      if  attr[ 'state' ] is "UP" and not attr[ 'ip' ].startswith( '127' ):
        ip = attr[ 'ip' ]
        print( '.'.join( ip.split( '.' )[ :3 ] ) )
        #print( iface )
    '''
    '''
    # Requires Root
    #import threading
    #from scapy.all import *
    interfaces = self.interfaces( )
    pkt = Ether( src=RandMAC( ),
                 dst="ff:ff:ff:ff:ff:ff" )/
         ARP( op=2, psrc="0.0.0.0", hwdst="ff:ff:ff:ff:Ff:ff" )/
         Padding( load="A" * 18 )    
    for interface in interfaces.keys( ):
      print( f'Sending ARP Request on {interface}...' )
      sendp(pkt, iface=interface, verbose=0)
    '''
    pass
  ####################################################################################


'''
def doARP():
    for _ in range(MAX / THREADS):
        # some of this copped from https://stackoverflow.com/questions/1487389/python-scapy-mac-flooding-script
        pkt = Ether(src=RandMAC(), dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, psrc="0.0.0.0",hwdst="ff:ff:ff:ff:Ff:ff")/Padding(load="A" * 18)
        sendp(pkt, iface=IFACE, verbose=0)


for _ in range(THREADS):
    t = threading.Thread(target=doARP, args=())
    t.start()
'''


'''
https://ired.team/offensive-security-experiments/active-directory-kerberos-abuse/active-directory-enumeration-with-powerview
https://github.com/infosecn1nja/Red-Teaming-Toolkit
https://github.com/yeyintminthuhtut/Awesome-Red-Teaming
https://github.com/diego-treitos/linux-smart-enumeration
https://tools.kali.org/information-gathering/enum4linux
https://medium.com/basic-linux-privilege-escalation/basic-linux-privilege-escalation-966de11f9997
https://github.com/rebootuser/LinEnum
http://www.0daysecurity.com/penetration-testing/enumeration.html
'''


'''
import fcntl
import socket
import struct
def hex2dot( packed ):
  if len( packed ) is 4: # port
    return int( packed, 16 )
  addr = int( packed, 16 )
  return socket.inet_ntoa( struct.pack( "<I", addr ) )


def Device_Net( ):
  ## https://www.kernel.org/doc/Documentation/networking/proc_net_tcp.txt
  net = Path( '/proc/net/tcp' ).read_text( ).strip( )
  lines = net.split( "\n" )[ 1: ]
  for line in lines:
    t = line.split( )
    ipv4 = t[1]
    ip, port = [ hex2dot( x ) for x in ipv4.split( ":" ) ]
    print( f"IP: {ip} => PORT: {port}" )
    #rem = t[2]
    #print( hex2dot( rem.split( ":" )[0] ) )
  # cat </dev/tcp/time.nist.gov/13 # get time
  # /proc/net/fib_trie
  #/proc/net/route
  #/proc/net/tcp


  def netstats( self ):
    netstats = {
      'local': {
        'ip':    set( ),
        'ports': set( )
      },
      'remote': set( )
    }

    def netstat( ):
      net = Path( '/proc/net/tcp' ).read_text( ).strip( ).split( "\n" )[ 1: ]
      for conn in net:
        conn = conn.split( )

        local_addr, local_port = [ hex2dot( x ) for x in conn[ 1 ].split( ":" ) ]
        netstats[ 'local' ][ 'ip'    ].add( local_addr )
        netstats[ 'local' ][ 'ports' ].add( local_port )

        remote_addr, remote_port = [ hex2dot( x ) for x in conn[ 2 ].split( ":" ) ]
        netstats[ 'remote' ].add( f'{local_addr}:{port} <=> {remote_addr}:{remote_port}' )
      print( netstats  )
    
    netstat( )
'''

