#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
Pyndorama: An adventure trip around the world.
Pyndorama: Uma viagem de aventura ao redor do mundo
===================================================

A text based adventure that can be programmed.
Uma aventura baseada em texto que pode se programada.

Copyright (c) 2002-2007
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author$"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2007/01/11 $Date$"

import gtk
import aventura


class Pyndorama:
  """Pyndorama Adventure - Aventura Pyndorama"""
  def __init__(self,adventure="ave.yaml"):
    "Load adventure from disk - Carrega a Aventura do disco"
    self.pindorama = aventura.load(adventure)
    self.pindorama.finalizer = lambda self=self :self.finalizer()
    self.action = self.query_and_post_back
  def query_and_post_back(self, query, canvas):
    '''Receive a query and post back results 
    -- Recebe uma ordem e envia resultados de volta'''
    canvas.write(self.pindorama.processaQuery(query))
    canvas.paint('.'+self.pindorama.getImage())
  def reset_adventure(self, query, canvas):
    '''Reset the screen to original state 
    -- Reestabelece o estado original da tela'''
    canvas.reset()
  def finalizer(self):
    '''Instruct pyndorama to finalize the game on next action
    -- Indica ao pyndorama para finalizar o jogo na próxima ação'''
    self.action = self.reset_adventure
    
class TextImagePanel(gtk.TextView):
  "A panel that draws text and image - Um painel que desenha texto e imagem"
  def __init__(self):
    self.buff = gtk.TextBuffer()
    gtk.TextView.__init__(self, self.buff)
    self.unset_flags(gtk.CAN_FOCUS)
  def config(self):
    self.area = self.get_window(gtk.TEXT_WINDOW_TEXT)
    self.set_cursor_visible(False)
    self.set_editable(False)
    self.set_border_width(0)
  def write(self, text):
    self.buff.set_text(text)
  def paint(self,picfile):
    image = gtk.gdk.pixbuf_new_from_file(picfile);
    width, height =(250, 200)
    scaled_buf = image.scale_simple(width, height, gtk.gdk.INTERP_BILINEAR)
    del image
    background,mask= scaled_buf.render_pixmap_and_mask( 255 );
    del scaled_buf
    self.area.set_back_pixmap( background, False)
    del background
    return width, height
  def stamp(self, picfile):
    wid,hei = self.paint(picfile)
    self.set_size_request(wid, hei)
    self.queue_draw()

class BookWindow(gtk.Window):
  """Main window showing an open book 
  -- Janela principal mostrando um livro aberto"""
  def __init__(self):
    gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
    self.set_title("Pyndorama")
    self.connect("destroy", lambda w: gtk.main_quit())
    self.set_border_width(10)
    self.set_app_paintable(True)
    self.resize(400, 500)
    self.realize()

  def paint(self, picfile):
    image = gtk.gdk.pixbuf_new_from_file(picfile);
    background,mask= image.render_pixmap_and_mask( 255 );
    width, height = background.get_size()
    del image
    self.resize(width, height)
    self.window.set_back_pixmap(background, False)
    del background

class GtkGui:
  """Assembles the graphic window -- Monta a janela gráfica."""
  def write(self, text):
    self.text.write(text)
  def paint(self, image):
    self.picture.stamp(image)
  def reset(self):
    self.request = self.request_adventure
    self.text.write('Benvindo ao Pindorama!\nEscreva na caixa a aventura\nque você quer jogar:\n  - ave\n  - labirinto')
    self.picture.stamp("static/images/pindorama.png")

  def __init__(self, client):
      self.pixmap = None
      self.client=client
      self.text = TextImagePanel()
      self.picture= TextImagePanel()
      self.action = gtk.Entry()
      self.button = gtk.Button("OK!")

      window= BookWindow()
      window.paint("static/images/book.jpg")

      vbox = gtk.HBox(1, 2)
      left = gtk.Fixed()
      right = gtk.Fixed()
      vbox.add(left)
      vbox.add(right)
      left.put(self.text, 70, 130)
      right.put(self.picture, 30, 110)
      left.set_border_width(0)
      left.put(self.action, 150, 350)
      left.set_focus_chain((self.button,))
      left.put(self.button, 320, 350)
      
      window.add(vbox)
      window.show_all()
      
      self.picture.config()
      self.text.config()
      self.text.paint("static/images/paper.jpg")
      self.reset()
      gtk.main()
      
  def button_request(self, *args):
    self.request()
  def request_adventure(self, *args):
    self.client = Pyndorama(self.action.get_text()+".yaml")
    self.request = self.perform_command
    self.client.action("", self)

  def perform_command(self, *args):
    self.client.action(self.action.get_text(), self)

class Main:      
  def __init__(self):
      self.pindorama=Pyndorama()
      GtkGui(self.pindorama)

if __name__ == '__main__':
  Main()

