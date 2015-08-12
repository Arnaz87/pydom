from gi.repository import Gtk, Gdk, cairo

class Renderer(Gtk.DrawingArea):
  def __init__(self):
    Gtk.DrawingArea.__init__(self)
    self.set_size_request(200, 200)
    self.connect("draw", self.draw_func)

  # cr is Cairo Context
  def draw_func(self, widget, cr):
    cr.set_source_rgba(0,0,1,1)
    cr.rectangle(10, 10, 50, 50)
    cr.fill()


class MyWindow(Gtk.Window):
  def __init__(self):
    Gtk.Window.__init__(self, title = "Ventana")
    self.app = Renderer()
    self.add(self.app)
    self.connect("delete-event", Gtk.main_quit)


win = MyWindow()
win.show_all()
Gtk.main()