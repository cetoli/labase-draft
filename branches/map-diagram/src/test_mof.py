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
from mof import Clazz, Link,Diagram

class Test_Clazz(unittest.TestCase):
  """
  Testa o MOF.
  """
  def setUp(self):
    Clazz.clazzid =0
    Link.linkid =0
    self.clazz = Clazz()
    Diagram.damp = 8

  def tearDown(self):
      pass

  def test_clazz_id(self):
    self.assertEquals(0,self.clazz.idc,
      "deveria ter limpado mas foi %s"%self.clazz.idc)
    self.clazz = Clazz()
    self.assertEquals(1,self.clazz.idc,
      "deveria ter incrementado mas foi %s"%self.clazz.idc)

  def test_inner_link(self):
    link = self.clazz.getLink(self.clazz)
    self.assertEquals(0,link.x(),
      "deveria ter limpado mas foi %s"%link.x())
    self.clazz = link.clazz
    self.clazz.x = 1
    self.assertEquals(1,link.x(),
      "deveria ter incrementado mas foi %s"%link.x)

  def test_inner_link_count(self):
    link_count=len(self.clazz.link)
    self.assertEquals(1,link_count,
      "deveria ter um no primeiro mas foi %s"%link_count)
    link_count=Link.linkid
    self.assertEquals(1,link_count,
      "deveria ter um no total mas foi %s"%link_count)
    fromclazz = Clazz()
    link_count=len(fromclazz.link)
    self.assertEquals(1,link_count,
      "deveria ter um no segundo mas foi %s"%link_count)
    link_count=Link.linkid
    self.assertEquals(2,link_count,
      "deveria ter dois no total mas foi %s"%link_count)

  def test_move_clazz(self):
    fromclazz = Clazz()
    link = self.clazz.getLink(fromclazz)
    fromclazz.add(link)
    self.clazz.relax(fromclazz)
    posx= self.clazz.x
    self.assertEquals(1,posx,
      "deveria ter movido origem mas foi %s"%posx)
    posx= self.clazz.x
    self.assertEquals(1,fromclazz.x,
      "deveria ter movido destino mas foi %s"%fromclazz.x)

  def test_move_far_clazz(self):
    fromclazz = Clazz((20,20))
    link = self.clazz.getLink(fromclazz)
    fromclazz.add(link)
    link.relax()
    posx= self.clazz.x
    self.assertEquals(8,posx,
      "deveria ter movido origem mas foi %s"%posx)
    posx= self.clazz.x
    self.assertEquals(12,fromclazz.x,
      "deveria ter movido destino mas foi %s"%fromclazz.x)

if __name__ == "__main__":
    unittest.main()
    