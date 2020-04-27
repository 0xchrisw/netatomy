#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode=True;
# https://graphviz.readthedocs.io/en/stable/api.html#digraph
# https://graphviz.readthedocs.io/en/stable/examples.html
# https://www.graphviz.org/doc/info/shapes.html


from graphviz import Digraph, nohtml, Source

dot = Digraph( 'companies',
  edge_attr={ 'weight':    '1',
              'fontsize':  '11',
              'fontcolor': 'black',
              'len':       '4' },
  graph_attr={ 'fixedsize': 'false',
              #'bgcolor':   'transparent' 
               'bgcolor':   'white' },
  node_attr={ 'shape': 'plaintext' },
  directory='gv',
  filename='map',
  format='png'
)
#dot.attr(bgcolor='blue')
dot.attr(layout="neato")

dot.attr(nodesep='3')
dot.attr(ranksep='3')
dot.attr(size='5000,5000')


dot.node('h1', '''<
<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr><td port="0">wlan0<br/>192.168.1.163<br/>DC:A6:32:27:D8:01<br/>Raspberry Pi Trading Ltd</td><td port="hostname" rowspan="2">raspberrypi</td><td port="1">lo<br/>127.0.0.1<br/>00:00:00:00:00:00<br/>XEROX CORPORATION</td></tr><tr><td port="2">eth0<br/>None<br/>DC:A6:32:27:D7:FF<br/>Raspberry Pi Trading Ltd</td><td port="3"></td></tr></table>
>''')



nodes = ['<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.218<br/>18:cf:5e:56:d7:22<br/>Unknown</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.205<br/>d4:11:a3:81:3f:8f<br/>Unknown</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.146<br/>38:1a:52:28:32:e0<br/>Unknown</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.143<br/>d8:31:34:88:9e:34<br/>Unknown</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.1<br/>c2:56:27:c9:f2:d8<br/>Unknown</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.210<br/>08:05:81:c1:8f:49<br/>Roku, Inc.</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.160<br/>60:01:94:74:77:2a<br/>Espressif Inc.</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.198<br/>d8:6c:63:40:ef:62<br/>Unknown</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.208<br/>5e:aa:ad:16:a0:97<br/>Unknown</td></tr></table>', '<table ALIGN="CENTER" BORDER="0" CELLBORDER="1" CELLSPACING="0"><tr port="0"><td>192.168.1.246<br/>c4:9d:ed:0e:b6:a0<br/>Unknown</td></tr></table>']



i = 0
for node in nodes:
  dot.node( f'n{i}', f'<{node}>' )
  i += 1




edges = [('h1:0', 'n0:0'), ('h1:0', 'n1:0'), ('h1:0', 'n2:0'), ('h1:0', 'n3:0'), ('h1:0', 'n4:0'), ('h1:0', 'n5:0'), ('h1:0', 'n6:0'), ('h1:0', 'n7:0'), ('h1:0', 'n8:0'), ('h1:0', 'n9:0')]
#edges = [('h1', 'n0:0'), ('h1', 'n1:0'), ('h1', 'n2:0'), ('h1', 'n3:0'), ('h1', 'n4:0'), ('h1', 'n5:0'), ('h1', 'n6:0'), ('h1', 'n7:0'), ('h1', 'n8:0'), ('h1', 'n9:0')]

dot.edges( edges )


#print(dot.source)
#Source(dot.source).render('map.gv', view=True)
dot.view()
#feh -R 2 map.png





'''
e = (2, 3)
G.add_edge(*e)  # unpack edge tuple*


c.attr(fontcolor='white')
c.attr('node', shape='circle', style='filled', fillcolor='white:black',
       gradientangle='360', label='n9:360', fontcolor='black')
'''
