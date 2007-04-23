#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
Gtk Graphics Front End
===================================

Copyright (c) 2002-2006
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""

__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author$"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2006/10/14 $Date$"


import gtk
from gtk.gdk import GC, Color
from vygotsky import Vygotsky_World

TARGET_TYPE_MOVE_ELEMENT = 80
TARGET_TYPE_SELECT= 81

fromElement = [ ( "element_move"   , 0, TARGET_TYPE_MOVE_ELEMENT   ),]
fromCanvas  = [ ( "select_box"     , 0, TARGET_TYPE_SELECT         ),]

toCanvas    = [ ( "element_move"   , 0, TARGET_TYPE_MOVE_ELEMENT   ),
                ( "select_box"     , 0, TARGET_TYPE_SELECT         ),]

class GtkGui:
  """
  GUI usando Gtk.
  """
  def __init__(self,client,title="Editor"):
      self.EltList = []
      self.screen = None
      self.client=client
      window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      window.set_title(title)
      window.connect("destroy", lambda w: gtk.main_quit())
      # Create the layout
      self.layout = gtk.Layout()
      self.layout.set_size_request(600, 600)
      self.layout.show()
      self.area = gtk.DrawingArea()
      self.area.set_size_request(600, 600)
      self.layout.add(self.area)
      #window.add(self.area)
      window.add(self.layout)
      self.area.set_events(gtk.gdk.POINTER_MOTION_MASK |
                           gtk.gdk.POINTER_MOTION_HINT_MASK )
      self.area.connect("expose-event", self.area_expose_cb)
      self.area.connect("configure_event", self.configure_event)
      self.layout.connect("drag_data_received", self.receiveCallback)
      self.layout.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
                                  gtk.DEST_DEFAULT_HIGHLIGHT |
                                  gtk.DEST_DEFAULT_DROP,
                                  toCanvas, gtk.gdk.ACTION_COPY)
      
      self.client.configure_world(self)


      self.pixmap = None
      self.area.show()
      self.layout.show()
      window.show()
      gtk.main()

  def create_element(self,feature):
    icon,x,y= feature
    new_element = Element(icon=icon,canvas=self,x=x,y=y)
    self.EltList.append(new_element)
    return new_element
    
  def configure_event(self,widget, event):
    win = widget.window
    width, height = win.get_size()
    self.pixmap = gtk.gdk.Pixmap(win, width, height)
    self.pixmap.draw_rectangle(widget.get_style().white_gc, True,
              0, 0, width, height)
    red_gc = self.pixmap.new_gc()    
    red_gc.set_foreground(self.pixmap.get_colormap().alloc_color(65535,0,0))
    
    self.pal={" ":self.area.get_style().white_gc,
      "*":self.area.get_style().black_gc,
      "$":red_gc}
    #self.client.configure_world(self)
        
    return True
    
  def area_expose_cb(self, widget, event):
    x, y, width, height = event.area
    gc = self.gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
    widget.window.draw_drawable(gc, self.pixmap, x, y, x, y, width, height)
    self.pixmap.draw_rectangle(widget.get_style().white_gc, True,
              0, 0, width, height)
    self.client.draw_canvas(self)
    return False
  def receiveCallback(self, 
    widget, context, x, y, selection, targetType,  time):
      if targetType == TARGET_TYPE_MOVE_ELEMENT:
        self.do_drop(x,y,selection.data)
  def do_drop(self,x,y,selection):
    pass
  def do_draw(self):
    #self.area.queue_draw()
    self.layout.queue_draw_area(0, 0, 600, 600)
  def draw_feature(self,where):
    gc = self.pal['$']
    face,x,y= where
    self.pixmap.draw_rectangle(gc, True, x, y , 10, 10)
    ''' 
    image = gtk.gdk.pixbuf_new_from_file('images/'+face);
    background,mask= image.render_pixmap_and_mask();
    self.pixmap.draw_drawable(gc, background, 0, 0, x, y, 50, 50)
    del image
    del background, mask
    ''' 

  
class Element(object):
    """ This class stand for a element
    Currently, it's only an icon and a name.
    """

    NODESIZE  = 38
    LABELSIZE = 80
    DX = 5
    DY =  10

    counter = 1

    def __init__(self, icon, name=None,Type='Name ',canvas=None, x=50, y=50):
        self.x    = int(x)
        self.y    = int(y)
        self.canvas = canvas
        self.icon = icon
        self.__class__.counter += 1
        # Create an Eventbox and an Image for the icon of the element
        self.Image_EventBox = gtk.EventBox()
        self.Image_EventBox.set_border_width(0)
        canvas.layout.put(self.Image_EventBox, self.x, self.y)

        self.Image  = gtk.Image()
        self.Image.set_from_file('images/'+icon)
        self.Image.show()
        self.Image_EventBox.add(self.Image)
        self.image = gtk.gdk.pixbuf_new_from_file('images/'+icon);
        #background,mask= image.render_pixmap_and_mask( 255 );
        self.Image_EventBox.shape_combine_mask(self.image.render_pixmap_and_mask()[1], 0, 0)
        self.Image_EventBox.show()

        # Signals and Drag'n'drop
        self.Image_EventBox.connect("drag_begin", self.drag_begin_cb)
        self.Image_EventBox.connect("drag_data_get", self.drag_data_get_cb)
        self.Image_EventBox.connect("button-release-event", self.button_release_cb)

        self.Image_EventBox.drag_source_set(gtk.gdk.BUTTON1_MASK,fromElement,
                               gtk.gdk.ACTION_COPY)
        
    def drag_begin_cb(self, widget, context):
      widget.drag_source_set_icon_pixbuf(self.image)
      return True

    def drag_data_get_cb(self, widget, context, selection, targetType, time):
      if targetType == TARGET_TYPE_MOVE_ELEMENT:
        selection.set(selection.target, 8, self.get_data())
      return True

    def get_data(self):
        return "%d"%id(self)

    def button_release_cb(self, widget, event):
        return True

    def move(self, x,y):
        self.x = int(x)
        self.y = int(y)
        self.canvas.layout.move(self.Image_EventBox, self.x   , self.y)

    def delete(self):
        self.canvas.EltList.remove(self)
        self.canvas.layout.remove(self.Image_EventBox)
        self.canvas.layout.remove(self.Name_EventBox)
        self.Image_EventBox.destroy()

    def __repr__(self):
        return self.name


#-------------------------------------------------------------------------------

class Main:      
  def __init__(self):
      self.diagram=Vygotsky_World()
      GtkGui(self.diagram, "Vygotsky")



if __name__ == '__main__':
  Main()

