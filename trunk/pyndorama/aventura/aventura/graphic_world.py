#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
Pyndorama: An adventure trip around the world.
Pyndorama: Uma viagem de aventura ao redor do mundo
===================================================

A graphic world with actors to be a living scenario by the text.
Um mundo gráfico com atores formando um cenário vivo junto ao texto.

Copyright (c) 2002-2007
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author$"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2007/4/16 $Date$"

IDEAL_GRID,IDEAL_CELL = 12,50
IS_ZERO = 0
STOCK_ACTOR = "actor.png"

"""Helper classes for the doctest, not used in production"""
class Gui_Stub:
  '''Empty graphic element stub'''
  def move(self,x,t):pass
class Cell_Painter:
  '''tester class to paint a cell'''
  gui= Gui_Stub()
  def configure_actor(self, given_canvas, x, y): pass
  def enter_world(self, given_world): pass
  def draw_canvas(self, given_canvas,pos_x,pos_y):
    given_canvas.draw_feature(('me',pos_x,pos_y))
  def __repr__(self): return 'me'
class Drawing_Reporter:
  '''tester class to report drawing'''
  def draw_feature(self, given_feature): print given_feature
  def create_element(self, given_actor): return Gui_Stub()

"""Graphic World classes used in production"""

class World:
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
    class No_Cell_Here:
      '''Use it where there is no cell'''
      gui= Gui_Stub()
      def configure_actor(self, given_canvas, x, y): pass
      def enter_world(self, given_world): pass
      def draw_canvas(self,x,*args): pass
      def drop_hit(self, given_actor,pos_x,pos_y):pass
      def __repr__(self): return 'nun'
    self.NoCell = No_Cell_Here()
    self.grid_size,self.cell_size = set_grid, set_cell
    self.cell_grid = []
    self.remove_actors()


  def configure_world(self, given_canvas):
    '''
    Configure each actor into the world grid
    >>> my_little_world = World(2)
    >>> ge= my_graphic_element = Drawing_Reporter()
    >>> my_graphic_element.create_element= lambda n,self=ge:self.draw_feature(n) or Gui_Stub()
    >>> my_little_world.add_actor(Actor('me'))
    >>> my_little_world.add_actor(Actor('you'),0,1)
    >>> my_little_world.configure_world(my_graphic_element)
    ('me', 0, 0)
    ('you', 0, 50)
    >>> my_graphic_element.do_drop(55,55,"0 0")
    >>> my_little_world.cell_grid[1][1]
    me
    '''
    #### -> this shoud be moved to application
    CELL_SIZE=self.cell_size
    self.NoCell.drop_hit= lambda actor_d,x,y,self=self: actor_d.move_actor(x,y)
    def find_actor_originating_drag(given_actor):
      actor_position_x,actor_position_y= [
        int(coordinate) for coordinate in given_actor.split()]
      return self.cell_grid[actor_position_x][actor_position_y]
    given_canvas.do_drop=lambda x,y,given_actor,self=self: \
      self.cell_grid[x/CELL_SIZE][y/CELL_SIZE].drop_hit(
        find_actor_originating_drag(given_actor), x/CELL_SIZE, y/CELL_SIZE
      )
    #### -> end of part to be moved
    [ each_actor.configure_actor(given_canvas, CELL_SIZE * x, CELL_SIZE * y) 
      for x,each_row in enumerate(self.cell_grid) 
      for y,each_actor in enumerate(each_row)]
    
  def reset(self, action):pass
  
  def drop_hit(self, given_actor,pos_x,pos_y):
    '''
    Do something when drag and drop upon the actor
    >>> my_little_world = World(2)
    >>> my_little_world.drop_hit(Cell_Painter(),0,0)
    
    '''
    pass
    
  def add_actor(self, given_actor, position_x= IS_ZERO, position_y= IS_ZERO):
    '''
    Put an actor into the world grid
    >>> my_little_world = World(2)
    >>> my_little_world.add_actor(Cell_Painter())
    >>> my_little_world.cell_grid[0][0]
    me
    '''
    self.cell_grid[position_x][position_y] = given_actor
    given_actor.enter_world(self)
    given_actor.gui.move(position_x*self.cell_size, position_y*self.cell_size)
      
  def remove_actors(self):
    '''
    Remove all actors from the world grid
    >>> my_little_world = World(2)
    >>> my_great_actor = Cell_Painter()
    >>> my_little_world.add_actor(my_great_actor)
    >>> my_little_world.remove_actors()
    >>> my_little_world.cell_grid[0][0]
    nun
    '''
    [actor.enter_world(None) for row in self.cell_grid for actor in row ]
    self.cell_grid = []
    for i in range(self.grid_size):
      self.cell_grid.append([self.NoCell]*self.grid_size)
      
  def remove_actor(self, given_actor):
    '''
    Remove an actor from the world grid
    >>> my_little_world = World(2)
    >>> my_great_actor = Cell_Painter()
    >>> my_little_world.add_actor(my_great_actor)
    >>> my_little_world.remove_actor(my_great_actor)
    >>> my_little_world.cell_grid[0][0]
    nun
    '''
    def replace_actor_for_NoCell(in_a_row):
      try:
        actor_whereabouts= in_a_row.index(given_actor)
        in_a_row[actor_whereabouts] = self.NoCell
        given_actor.enter_world(None)
      except:
        pass
    [ replace_actor_for_NoCell(in_a_row) for in_a_row in self.cell_grid]
    
  def find_actor_coordinates(self, given_actor):
    '''
    Find an actor coordinates in the world grid
    >>> my_little_world = World(2)
    >>> my_great_actor = Cell_Painter()
    >>> my_little_world.add_actor(my_great_actor,1)
    >>> my_little_world.find_actor_coordinates(my_great_actor)
    (1, 0)
    '''
    for  position_x, this_column in enumerate(self.cell_grid):
      if given_actor in this_column : 
        position_y = this_column.index(given_actor)
        return (position_x,position_y)
    return (-1,-1)
    
  def draw_canvas(self, given_canvas):
    '''
    Draw in a canvas the contents of the world
    >>> my_little_world = World(2)
    >>> my_little_world.add_actor(Cell_Painter(),1)
    >>> my_little_world.draw_canvas(Drawing_Reporter())
    ('me', 50, 0)
    '''
    self.draw_world(given_canvas)
    [cell_to_paint.draw_canvas(given_canvas, x*self.cell_size, y*self.cell_size) 
       for x,row_to_paint in enumerate(self.cell_grid) 
       for y,cell_to_paint in enumerate(row_to_paint)]

  def draw_world(self, given_canvas):
    '''
    Draw in a canvas the customized contents of the world
    >>> my_little_world = World(2)
    >>> my_little_world.add_actor(Cell_Painter(),1)
    >>> my_little_world.draw_world = lambda  cnvs, x=0: cnvs.draw_feature('hi')
    >>> my_little_world.draw_canvas(Drawing_Reporter())
    hi
    ('me', 50, 0)
    '''
    pass
    
class Actor:
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
    self.gui = Gui_Stub()

  def configure_actor(self, given_canvas, x, y):
    self.gui = given_canvas.create_element((self.image_face,x,y))
    self.gui.get_data = lambda self=self: \
      "%d %d"%self.actor_world.find_actor_coordinates(self)
      
  def enter_world(self, set_world):
    '''
    Put the actor within a world
    >>> my_little_actor = Actor()
    >>> my_little_world = World(2)
    >>> my_little_actor.image_face
    'actor.png'
    '''
    self.actor_world = set_world

  def move_actor(self,  position_x= IS_ZERO, position_y= IS_ZERO):
    '''
    Remove the actor from its place and put in a new Position
    >>> my_little_world = World(2)
    >>> mga = my_great_actor = Actor("gme")
    >>> mla = my_little_actor = Actor("me")
    >>> mga.draw_canvas=lambda c,x,y,self= mga: c.draw_feature((self.image_face,x,y))
    >>> mla.draw_canvas=lambda c,x,y,self= mla: c.draw_feature((self.image_face,x,y))
    >>> my_little_world.add_actor(my_little_actor)
    >>> my_little_world.add_actor(my_great_actor)
    >>> my_little_actor.move_actor(1,1)
    >>> my_little_world.draw_canvas(Drawing_Reporter())
    ('gme', 0, 0)
    ('me', 50, 50)
    '''
    the_current_world=self.actor_world
    the_current_world.remove_actor(self)
    the_current_world.add_actor(self, position_x, position_y)
    
  def draw_canvas(self, given_canvas,pos_x,pos_y):
    '''
    paint itself within the given canvas
    >>> my_little_world = World(2)
    >>> my_little_actor = Actor("isme")
    >>> my_little_world.add_actor(my_little_actor,1)
    >>> my_little_world.draw_canvas(Drawing_Reporter())
    
    '''
    self.draw_actor(given_canvas)
    
  def drop_hit(self, given_actor,pos_x,pos_y):
    '''
    Do something when drag and drop upon the actor
    >>> my_little_actor = Actor("isme")
    >>> my_little_actor.drop_hit(my_little_actor,0,0)
    
    '''
    pass

  def draw_actor(self, given_canvas):
    '''
    paint itself within the given canvas with customization
    >>> my_little_world = World(2)
    >>> my_little_actor = Actor("me")
    >>> my_little_actor.draw_actor = lambda  cnvs, x=0: cnvs.draw_feature('hi')
    >>> my_little_world.add_actor(my_little_actor,1)
    >>> my_little_world.draw_canvas(Drawing_Reporter())
    hi
    '''
    pass
    
  def __repr__(self): return self.image_face
  
def _run_all_the_tests_in_the_documention():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
  _run_all_the_tests_in_the_documention()

