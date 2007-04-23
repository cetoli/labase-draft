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
from random import randint

IDEAL_GRID,IDEAL_CELL = 12,50
IS_ZERO = 0
STOCK_ACTOR = "actor.png"
BABY_PURPLE = '#EED7F4'
GREEK_VASE = '#FEE6D5'
PITCH_DARK = '#000000'
CELL_SIZE = 50 # cell size in pixels
ENV_SIZE = 12 # cell size in pixels
SZ = ["s","l"]; # sizes small, large
TK = ["s","f"]; # Thickness slim, fat
CL = ["r","g","b","y"]; # Colous red, green, blue, yellow
SP = ["c","t","s","p"]; # Shapes circle, triangle, square, pentagon
SHAPES = [ a+b+c+d for a in SZ for b in TK for c in CL for d in SP];  

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
    self.already_painted= False
    self.blocks = SHAPES[:]
    self.populate_world_with_blocks()
    
  def populate_world_with_blocks(self):
    '''load block shape images from disk
    >>> my_little_world = Vygotsky_World(2)
    >>> random_shapes = []
    >>> def show(x): random_shapes.append( x.image_face)
    >>> my_little_world.add_actor = lambda a, x=0,y=0, s=None: show(a)
    >>> my_little_world.populate_world_with_blocks()
    >>> sum([1 for this_shape in SHAPES if this_shape+".png" in random_shapes])
    64
    '''
    self.remove_actors()
    self.blocks = SHAPES[:]
    def pick_a_random_block():
      return Coloured_Shaped_Block(
        self.blocks.pop(randint(0,len(self.blocks)-1)) + ".png"
      )
    a_side = range(2,10)
    [self.add_actor(pick_a_random_block(),x,y) for x in a_side for y in  a_side]
    #[self.add_actor(pick_a_random_block()) for x in SHAPES]

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
    def draw_Background(given_canvas):
      bg = given_canvas;
      BABY_PURPLE_COLOUR = bg.pixmap.get_colormap().alloc_color(BABY_PURPLE)
      bg.gc.set_foreground(BABY_PURPLE_COLOUR)
      width, height = [12*CELL_SIZE]*2
      bg.pixmap.draw_rectangle(bg.gc, True, 0, 0,width, height)
      GREEK_VASE_COLOUR = bg.pixmap.get_colormap().alloc_color(GREEK_VASE)
      bg.gc.set_foreground(GREEK_VASE_COLOUR)
      bg.pixmap.draw_rectangle(
        bg.gc, True, 2*CELL_SIZE, 2*CELL_SIZE, 8*CELL_SIZE, 8*CELL_SIZE)
      BLACK_CORNERS = [(0,0),(1,1),(10,10),(11,11),(1,10),(0,11),(10,1),(11,0),]
      PITCH_DARK_COLOUR = bg.pixmap.get_colormap().alloc_color(PITCH_DARK)
      bg.gc.set_foreground(PITCH_DARK_COLOUR)
      def paint_boxes(x,y):
        bg.pixmap.draw_rectangle(
          bg.gc, True, x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
      [paint_boxes(x,y) for x,y in BLACK_CORNERS]
      for i in range(ENV_SIZE):
        bg.pixmap.draw_line(
          bg.gc, i * CELL_SIZE, 0, i * CELL_SIZE, ENV_SIZE * CELL_SIZE);
        bg.pixmap.draw_line(
          bg.gc, 0, i * CELL_SIZE, ENV_SIZE * CELL_SIZE, i * CELL_SIZE);
      if not self.already_painted : 
        bg.do_draw()
        self.already_painted= True
      
      '''
      bg.fillRect(2*CELL_SIZE,2*CELL_SIZE,8*CELL_SIZE,8*CELL_SIZE);
      bg.setColor(Color.BLACK);
      bg.fillRect(0*CELL_SIZE,0*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      bg.fillRect(1*CELL_SIZE,1*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      bg.fillRect(10*CELL_SIZE,10*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      bg.fillRect(11*CELL_SIZE,11*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      bg.fillRect(10*CELL_SIZE,1*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      bg.fillRect(11*CELL_SIZE,0*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      bg.fillRect(1*CELL_SIZE,10*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      bg.fillRect(0*CELL_SIZE,11*CELL_SIZE,CELL_SIZE,CELL_SIZE);
      '''
    draw_Background(given_canvas)
    

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
    Actor.__init__(self, set_image)
    #self.image_face = set_image

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

