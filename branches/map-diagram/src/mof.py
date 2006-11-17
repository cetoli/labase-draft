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

class NullNode:
  'Null Node used as parent of root class'
  def pos(self): return (0,0)
  def parent(self): return self
class Clazz:
    clazzid = 0
    def __init__(self, origin=(0,0),parent=NullNode()):
      self.x ,self.y = origin
      self.idc = Clazz.clazzid
      Clazz.clazzid += 1
      self.link =[]
      self.dimension = 1
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
    def getDimension(self):
      return self.dimension
    def redimension(self):
      suppressed_redimension_method= self.redimension
      self.redimension= lambda self=self: 0
      self.dimension = sum([link.redimension() for link in self.link])or 1
      self.redimension=suppressed_redimension_method
      return self.dimension
    def insert(self,node):
      self.getLink(node)
      self.redimension()
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
  def draw(self,gc=None,offset=(0,0)):
    suppressed_draw_method= self.draw
    self.draw= lambda self=self,gc,offset: 0
    gc.draw(self.pos(),'*')
    nextoffset=(offset[0]+1,offset[1]-self.dimension/2)
    def calculate_and_draw(node):
      node.draw(gc,offset=nextoffset)
      nextoffset=(nextoffset[0],nextoffset[1]+node.getDimension)
    [calculate_and_draw(node) for node in self.link]
    self.draw=suppressed_draw_method

class Link:
    linkid = 0
    def __init__(self, clazz, froms =None):
      self.idl = Link.linkid
      Link.linkid += 1
      self.clazz = clazz
      self.froms = froms
    def x(self):
      return self.clazz.x
    def redimension(self):
      return self.froms.redimension()
      
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
    def draw(self,gc=None,offset=(0,0)):
      Wire(wire=link.linker()).draw(gc)
      self.froms.draw(gc,offset)


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
    self.current = Clazz()
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
  def insert(self):
    self.current = self.current.insert(Clazz(parent=self.current))
    
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


