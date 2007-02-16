#! /usr/bin/env python
"""
Settlers of Catan.

Copyright (c) 2002-2004
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""

__author__ = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: carlo $"
__version__ = " 1.0 $Rev: 226 $"[11:-2]

import os, sys

class values:
  def __init__(self): self.values = []
  def get(self): return self.values
class consumer(values):
  def receive(self,product):
    self.get()+=[product]
class notifier(values):
  def notify(self,sendmessage):
    [each.sendmessage() for each in self.get()]

class composite(values):
  def add(self,item):
    self.get()+=[product]
  def iterate(self,request):
    for item in self.get(): item.request()


class publishing(consumer,notifier):
  
class board:
    
class terrain(consumer):
  pass

class vertex:
  pass

    
class colonize:
  
