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
from random import randint
from time import sleep
from router import Wire

class Clazz:
    clazzid = 0
    def __init__(self, origin=(0,0)):
      self.x ,self.y = origin
      self.idc = Clazz.clazzid
      Clazz.clazzid += 1
      self.link =[]
      self.getLink(self)
    def add(self, link):
      self.link +=[link]
    def getLink(self, froms):
      link = Link(self,froms)
      self.add(link)
      return link
    def linkTo(self,clazz):
      self.link += [clazz.getLink(self)]
    def move(self, x, y):
      self.x = min( abs(self.x + x), Diagram.sz)
      self.y = min( abs(self.y + y), Diagram.sz)
      return self.x,self.y
    def pos(self):
      return self.x, self.y
    def relax(self,froms):
      'Tenta manter as classes separadas por uma distancia de oito'
      len_x = self.x - froms.x or 1
      len_y = self.y - froms.y or 1
      distance = (abs(len_x)+abs(len_y)) or 1
      if distance >= 8: return
      force = 2*(distance -8)/distance
      desired_dx = (len_x * force)/Diagram.damp
      desired_dy = (len_y *force)/Diagram.damp
      self.move(-desired_dx,-desired_dy)
      froms.move(desired_dx,desired_dy)

class Link:
    linkid = 0
    def __init__(self, clazz, froms =None):
      self.idl = Link.linkid
      Link.linkid += 1
      self.clazz = clazz
      self.froms = froms
    def x(self):
      return self.clazz.x
      
    def move(self, x, y):
      self.move = lambda x,y: None
      self.clazz.move(x,y)
    def relax(self):
      'Tenta aproximar as classes ligadas para uma distancia de 8'
      len_x = self.clazz.x - self.froms.x
      len_y = self.clazz.y - self.froms.y
      distance = (abs(len_x)+abs(len_y)) or 1
      force = 4*(distance -8)/distance
      desired_dx = (len_x * force)/Diagram.damp 
      desired_dy = (len_y *force)/Diagram.damp 
      #print 'id:%d x:%d y: %d dx:%d dy: %d fx:%d rx:%d ry: %d dis: %d'%(self.idl, self.clazz.x, self.clazz.y, len_x, len_y, force, desired_dx, desired_dy, distance) 
      self.clazz.move(-desired_dx,-desired_dy)
      self.froms.move(desired_dx,desired_dy)

    def linker(self):
      return self.froms.pos(),self.clazz.pos()

class Diagram:
  damp = 4
  sz = 60
  def __init__(self):
    sz = Diagram.sz
    MAX_CLAZZES = 20
    MAX_LINKS = 30
    M_T = 20
    self.t = M_T
    self.anneal= 0
    def rnf():
      return randint(0,sz),randint(0,sz)
    def makeLink(clazzes):
      max_clazz = len(clazzes)-1
      origin = randint(0,max_clazz)
      target = randint(0,max_clazz)
      #if origin == target: return
      link = clazzes[origin].getLink(clazzes[target])
      clazzes[target].add(link)
      return link
    self.clazzes = [Clazz(rnf()) for clazzes in range (0,MAX_CLAZZES)]
    self.links = [makeLink(self.clazzes) for links in range(0,MAX_LINKS)]
  
  def draw(self,gc=None):
    x,y=(0,0)
    if self.t > 0:
      x,y = randint(-self.t,self.t),randint(-self.t,self.t)
      self.clazzes[self.anneal].move(x,y)
      self.anneal +=1
      if self.anneal >= len(self.clazzes):
        self.anneal =0
        self.t -= 1
        Diagram.damp +=1
    [link.relax() for link in self.links]
    [[clazz.relax(froms) for froms in self.clazzes] for clazz in self.clazzes]
    [gc.draw(clazz.pos(),'*') for clazz in self.clazzes]
    #[gc.linker(link.linker()) for link in self.links] # em linha reta
    [Wire(wire=link.linker()).draw(gc) for link in self.links] #em angulos retos
    gc.do_draw()
    sleep(0.6)


