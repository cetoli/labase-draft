import gtk
from gazpacho.loader.loader import ObjectBuilder

wt = ObjectBuilder('ex.glade')
wt.signal_autoconnect(globals())
wt.toplevels[0].show_all()

textview1 = wt.get_widget('textview1')
textview2 = wt.get_widget('textview2')
buffer =  gtk.TextBuffer()
buffer.set_text('felipe',False)
print (textview1.get_buffer())    
textview2.set_buffer(buffer)
gtk.main()