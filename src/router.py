"""
Diagram - self layout diagram.
===================================

Copyright (c) 2002-2006
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""

__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: carlo $"
__version__ = "1.0 $Revision: 1.4 $"[10:-1]
__date__    = "2006/10/15 $Date: 15/10/2006 18:51:55 $"

class Wire:
  '''
    0##-+1           1+-##4    ###-+   +-###    
        |2            |2           |   |        
       3+-##4   0####-+3      ###--+   +--##### 
    cis-dis     trans-dis     cis-jus trans_jus  
  '''
  CIS_DIS = ((0,1),(2,1),(2,3),(4,3))
  TRANS_DIS = ((0,3),(2,3),(2,1),(4,1))
  CIS_JUS = ((0,1),(2,1),(2,3),(4,3))
  TRANS_JUS = ((0,3),(2,3),(2,1),(4,1))
  BLOCK_SIZE = 6
  CIS_NON = 0
  TRANS_NON = 1
  CIS_POS = 2
  TRANS_POS = 3
  WIRE_MODE= [CIS_DIS,TRANS_DIS,CIS_JUS,TRANS_JUS]
  def __init__(self,one=(0,0),another=(0,0),wire=None):
    if wire: 
      self.makeWire(wire[0],wire[1])
    else:
      self.makeWire(one,another)
   
  def makeWire(self,one,another):
    top = min(one[1],another[1])
    bottom = max(one[1],another[1])
    left = min(one[0],another[0])
    right = max(one[0],another[0])
    middle = (left+right)/2
    if one[1] > another[1]:
      one,another=(another,one)
    self.mode = Wire.CIS_NON
    if abs(one[0] - another[0]) < Wire.BLOCK_SIZE:
      self.mode = Wire.CIS_POS
      middle += abs(left-right) + 4
    if (one[0] > another[0]):
      self.mode += 1
    self.coordinates = (left,top,middle,bottom,right)
  def makeCoordinates(self, index):
    wire = Wire.WIRE_MODE[self.mode]
    coord = self.coordinates
    fro,to = (index,index+1)
    x,y = (0,1)
    return (coord[wire[fro][x]],coord[wire[fro][y]]) \
         , (coord[wire[to ][x]],coord[wire[to ][y]])
           
  def draw(self,cg):
    [cg.linker(self.makeCoordinates(i)) for i in range(0,3)]
    
