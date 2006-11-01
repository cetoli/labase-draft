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
__date__    = "2006/10/14 $Date: 15/10/2006 18:51:55 $"

import unittest
from router import Wire

class Test_Router(unittest.TestCase):
  """
  Testa o Roteador.
  """
  def setUp(self):
    self.rt = Wire()

  def tearDown(self):
      pass

  def test_wiring_mode(self):
    matcher=Wire((0,0),(0,0)).mode
    self.assertEquals(Wire.CIS_POS,matcher,
      "deveria ser justaposto mas foi %s"%matcher)
    matcher=Wire((0,0),(9,0)).mode
    self.assertEquals(Wire.CIS_NON,matcher,
      "deveria ser cis mas foi %s"%matcher)
    matcher=Wire((2,0),(0,1)).mode
    self.assertEquals(Wire.TRANS_POS,matcher,
      "deveria ser tranposed mas foi %s"%matcher)
    matcher=Wire((0,1),(9,0)).mode
    self.assertEquals(Wire.TRANS_NON,matcher,
      "deveria ser trans mas foi %s"%matcher)
      
  def test_wiring_route(self):
    matcher=Wire((0,0),(0,0)).makeCoordinates(0)
    self.assertEquals(((0,0),(4,0)),matcher,
      "deveria ser justaposto mas foi "+ str(matcher))
    matcher=Wire((0,0),(8,1)).makeCoordinates(1)
    self.assertEquals(((4,0),(4,1)),matcher,
      "deveria ser cis mas foi  "+ str(matcher))
    matcher=Wire((2,0),(0,1)).makeCoordinates(2)
    self.assertEquals(((7,0),(2,0)),matcher,
      "deveria ser tranposed mas foi  "+ str(matcher))
    matcher=Wire((0,1),(9,0)).makeCoordinates(0)
    self.assertEquals(((0,1),(4,1)),matcher,
      "deveria ser trans mas foi  "+ str(matcher))


