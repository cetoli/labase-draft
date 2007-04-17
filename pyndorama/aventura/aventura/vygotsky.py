#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
Pyndorama: An adventure trip around the world.
Pyndorama: Uma viagem de aventura ao redor do mundo
===================================================

Vygotsky: a game to match blocks according many rules.
Vygotsky: um jogo para agrupar blocos segundo várias regras.

Copyright (c) 2002-2007
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author$"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2007/4/16 $Date$"

from graphic_world import World, Actor

IDEAL_GRID,IDEAL_CELL = 12,50
IS_ZERO = 0
STOCK_ACTOR = "actor.png"

class Cell_Painter:
  '''tester class to paint a cell'''
  def enter_world(self, given_world): pass
  def draw_canvas(self, given_canvas,pos_x,pos_y):
    given_canvas.draw_feature(('me',pos_x,pos_y))
  def __repr__(self): return 'me'
class Drawing_Reporter:
  '''tester class to report drawing'''
  def draw_feature(self, given_feature): print given_feature

class Vygotsky_World (World):
  '''
  Create a world with a grid and size
  >>> my_little_world = World(10,40)
  >>> my_little_world.grid_size, my_little_world.cell_size
  (10, 40)
  '''
  def __init__(self, set_grid= IDEAL_GRID, set_cell= IDEAL_CELL):
    '''
    Create a world with all ideal values
    >>> my_little_world = World(2)
    >>> my_little_world.cell_grid[1][1]
    nun
    '''
    World.__init__(self)

  def draw_world(self, given_canvas):
    '''
    Draw in a canvas the customized contents of the world
    >>> my_little_world = World(2)
    >>> my_little_world.add_actor(Cell_Painter(),1)
    >>> my_little_world.draw_world = lambda  cnvs, x=0: cnvs.draw_feature('hi')
    >>> my_little_world.draw_canvas(Drawing_Reporter())
    hi
    ('me', 1, 0)
    '''
    pass
    
  def populate(self):
    '''
    Create a collection of Coloured shapes
    '''
    pass
    
class Coloured_Shaped_Block(Actor):
  '''
  Create a actor with a given image
  >>> my_little_actor = Actor("me")
  >>> my_little_actor.image_face
  'me'
  '''
  def __init__(self, set_image= STOCK_ACTOR):
    '''
    Create a actor with a given image or a stock image
    >>> my_little_actor = Actor()
    >>> my_little_actor.image_face
    'actor.png'
    '''
    self.image_face = set_image

  def move_actor(self,  position_x= IS_ZERO, position_y= IS_ZERO):
    '''
    Remove the actor from its place and put in a new Position
    >>> my_little_world = World(2)
    >>> my_little_actor = Actor("me")
    >>> my_little_world.add_actor(my_little_actor)
    >>> my_little_actor.move_actor(1,1)
    >>> my_little_world.draw_canvas(Drawing_Reporter())
    ('me', 1, 1)
    '''
    the_current_world=self.actor_world
    the_current_world.remove_actor(self)
    the_current_world.add_actor(self, position_x, position_y)
    
    
def _run_all_the_tests_in_the_documention():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
  _run_all_the_tests_in_the_documention()

