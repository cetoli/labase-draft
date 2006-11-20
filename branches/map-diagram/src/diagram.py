#! /usr/bin/env python
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
import gtk
from gtk.gdk import GC, Color
from mof import Diagram


class GtkGui:
  """
  GUI usando Gtk.
  """
  def __init__(self,client):
      self.screen = None
      self.client=client
      window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      window.set_title("Diagrama")
      window.connect("destroy", lambda w: gtk.main_quit())
      self.area = gtk.DrawingArea()
      self.area.set_size_request(800, 600)
      window.add(self.area)
      self.area.set_events(gtk.gdk.POINTER_MOTION_MASK |
                           gtk.gdk.POINTER_MOTION_HINT_MASK )
      self.area.connect("expose-event", self.area_expose_cb)
      self.area.connect("configure_event", self.configure_event)

      self.pixmap = None
      self.area.show()
      window.show()
      gtk.main()

  def configure_event(self,widget, event):
    global pixmap
    
    win = widget.window
    width, height = win.get_size()
    self.pixmap = gtk.gdk.Pixmap(win, width, height)
    self.pixmap.draw_rectangle(widget.get_style().white_gc, True,
              0, 0, width, height)
    
    red = gtk.gdk.color_parse("red")
    red_gc = self.pixmap.new_gc()    
    red_gc.set_foreground(self.pixmap.get_colormap().alloc_color(65535,0,0))
    
    self.pal={" ":self.area.get_style().white_gc,
      "*":self.area.get_style().black_gc,
      "$":red_gc}
    return True
    
  def area_expose_cb(self, widget, event):
    x, y, width, height = event.area
    gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
    widget.window.draw_drawable(gc, self.pixmap, x, y, x, y, width, height)
    self.pixmap.draw_rectangle(widget.get_style().white_gc, True,
              0, 0, width, height)
    self.client.draw(self)
    return False
  def do_draw(self):
    self.area.queue_draw()
  def draw(self,where,target):
    gc = self.pal[target]
    self.pixmap.draw_rectangle(gc, True, where[0]*10-30, where[1]*10-5 , 60, 10)
  def linker(self,link):
    self.link(link[0],link[1])
  def link(self,froms,where):
    gc = self.pal['*']
    self.pixmap.draw_line(gc,
      froms[0]*10, froms[1]*10 ,
      where[0]*10, where[1]*10 )
  
class Main:      
  def __init__(self):
      self.diagram=Diagram()
      GtkGui(self.diagram)



if __name__ == '__main__':
  Main()

