#! /usr/bin/env python
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


class GtkGui:
  """
  GUI usando Gtk.
  """
  def __init__(self,client,title="Editor"):
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

      self.pixmap = None
      self.area.show()
      window.show()
      gtk.main()

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
    return True
    
  def area_expose_cb(self, widget, event):
    x, y, width, height = event.area
    gc = self.gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
    widget.window.draw_drawable(gc, self.pixmap, x, y, x, y, width, height)
    self.pixmap.draw_rectangle(widget.get_style().white_gc, True,
              0, 0, width, height)
    self.client.draw_canvas(self)
    return False
  def do_draw(self):
    self.area.queue_draw()
  def draw_feature(self,where):
    gc = self.pal['$']
    face,x,y= where
    self.pixmap.draw_rectangle(gc, True, x, y , 10, 10)
    image = gtk.gdk.pixbuf_new_from_file('images/'+face);
    width, height =(50, 50)
    scaled_buf = image.scale_simple(width, height, gtk.gdk.INTERP_BILINEAR)
    del image
    background,mask= scaled_buf.render_pixmap_and_mask( 255 );
    self.area.draw_drawable(gc, self.pixmap, 0, 0, x, y, 50, 50)
    del background, mask

  
class Element(object):
    """ This class stand for a element
    Currently, it's only an icon and a name.
    """

    NODESIZE  = 38
    LABELSIZE = 80
    DX = (NODESIZE-LABELSIZE)/2
    DY =  40

    counter = 1

    def __init__(self,name=None,Type='Name ',canvas=None, x=50, y=50):
        self.Type = Type
        self.x    = int(x)
        self.y    = int(y)
        self.selected = False
        self.canvas = canvas
        self.name = name or "%s%d" % (Type,self.counter)
        self.__class__.counter += 1

        # Create an Eventbox and an Image for drawing the name of the Element
        # I choose to use an Image instead of a label because I need to change
        # the background color.
        self.Name_EventBox = gtk.EventBox()
        self.Name_EventBox.set_border_width(0)
        canvas.layout.put(self.Name_EventBox, self.x+self.DX, self.y+self.DY)
        self.Name_EventBox.show()

        self.NameBox = gtk.Image()
        self.draw_name()
        self.NameBox.show()
        self.Name_EventBox.add(self.NameBox)

        # Create an Eventbox and an Image for the icon of the element
        self.Image_EventBox = gtk.EventBox()
        self.Image_EventBox.set_border_width(0)
        canvas.layout.put(self.Image_EventBox, self.x, self.y)

        self.Image  = gtk.Image()
        self.Image.set_from_pixbuf(icon_normal)
        self.Image.show()
        self.Image_EventBox.add(self.Image)
        self.Image_EventBox.shape_combine_mask(icon_normal.render_pixmap_and_mask()[1], 0, 0)
        self.Image_EventBox.show()

        # Signals and Drag'n'drop
        self.Image_EventBox.connect("drag_begin", self.drag_begin_cb)
        self.Image_EventBox.connect("drag_data_get", self.drag_data_get_cb)
        self.Image_EventBox.connect("button-release-event", self.button_release_cb)

        self.Image_EventBox.drag_source_set(gtk.gdk.BUTTON1_MASK,fromElement,
                               gtk.gdk.ACTION_COPY)

    '''
    def drag_begin_cb(self, widget, context):
        # First we deselect all selected elts if the dragged element is not currently selelected
        if not self.selected :
            for n in self.canvas.EltList : n.deselect()
            self.select()

        widget.drag_source_set_icon_pixbuf(icon_normal)

        return True

    def drag_data_get_cb(self, widget, context, selection, targetType, time):
        if targetType == TARGET_TYPE_MOVE_ELEMENT:
            selection.set(selection.target, 8, "%d,%d,%d" % (self.x, self.y, id(self)))

        return True

    def button_release_cb(self, widget, event):
        if event.button == 1 and (event.x, event.y) != (0., 0.):
            # button #1 was released but not during a drop
            # -> select the element

            if event.state & gtk.gdk.SHIFT_MASK :
                self.select()

            elif event.state & gtk.gdk.CONTROL_MASK :
                if self.selected : self.deselect()
                else             : self.select()

            else :
                for n in self.canvas.EltList : n.deselect()
                self.select()

        return True
    '''

    def draw_name(self):
        """ Create two images representing element's name in normal and selected state. """
        # create a pango.Layout containing element name
        pango_gc = self.canvas.layout.get_pango_context()
        pangolayout = pango.Layout(pango_gc)
        pangolayout.set_text(self.name)
        pangolayout.set_width((self.LABELSIZE-2)*pango.SCALE)
        pangolayout.set_wrap(pango.WRAP_WORD)
        pangolayout.set_alignment(pango.ALIGN_CENTER)

        # Define the size of the box
        w = self.LABELSIZE
        h = pangolayout.get_pixel_size()[1]+2
        gc = self.canvas.gc

        # draw the box - selected state
        pixmap = gtk.gdk.Pixmap(None, w, h, 24)
        gc.set_foreground(self.canvas.COLOR['selected'])
        pixmap.draw_rectangle(gc, True, 0, 0, w, h)
        gc.set_foreground(self.canvas.COLOR['white'])
        pixmap.draw_rectangle(gc, False, 0, 0, w-1, h-1)
        pixmap.draw_layout(gc, 1, 1, pangolayout,
            background=None, foreground=self.canvas.COLOR['white'] )

        self.NameBox_selected = pixmap

        # draw the box - normal state
        pixmap = gtk.gdk.Pixmap(None, w, h, 24)
        gc.set_foreground(self.canvas.COLOR['bg'])
        pixmap.draw_rectangle(gc, True, 0, 0, w, h)
        gc.set_foreground(self.canvas.COLOR['txt'])
        pixmap.draw_rectangle(gc, False, 0, 0, w-1, h-1)
        pixmap.draw_layout(gc, 1, 1, pangolayout,
            background=None, foreground=self.canvas.COLOR['txt'] )

        self.NameBox_normal = pixmap
        self.NameBox.set_from_pixmap(pixmap, None)


    def select(self):
        if not self.selected :
            self.selected = True
            self.Image.set_from_pixbuf(icon_selected)
            self.NameBox.set_from_pixmap(self.NameBox_selected, None)

    def deselect(self):
        if self.selected :
            self.selected = False
            self.Image.set_from_pixbuf(icon_normal)
            self.NameBox.set_from_pixmap(self.NameBox_normal, None)

    def move(self, x,y):
        self.x = int(x)
        self.y = int(y)
        self.canvas.layout.move(self.Image_EventBox, self.x   , self.y)
        self.canvas.layout.move(self.Name_EventBox, self.x+self.DX, self.y+self.DY)

    def delete(self):
        self.canvas.EltList.remove(self)
        self.canvas.layout.remove(self.Image_EventBox)
        self.canvas.layout.remove(self.Name_EventBox)
        self.Image_EventBox.destroy()
        self.NameBox.destroy()

    def __repr__(self):
        return self.name


#-------------------------------------------------------------------------------

class Main:      
  def __init__(self):
      self.diagram=Vygotsky_World()
      GtkGui(self.diagram, "Vygotsky")



if __name__ == '__main__':
  Main()

