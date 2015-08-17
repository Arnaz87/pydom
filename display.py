from gi.repository import Gtk, Gdk, cairo

class Renderer(Gtk.DrawingArea):
  def __init__(self, draw_list):
    Gtk.DrawingArea.__init__(self)
    self.set_size_request(200, 200)
    self.draw_list = draw_list
    self.connect("draw", self.draw_func)

  # cr is Cairo Context
  def draw_func(self, widget, cr):
    size = 0
    for cmd in self.draw_list:
      cmd.draw(cr)


class MyWindow(Gtk.Window):
  def __init__(self, draw_list):
    Gtk.Window.__init__(self, title = "Ventana")
    self.app = Renderer(draw_list)
    self.add(self.app)
    self.connect("delete-event", Gtk.main_quit)

def CreateWindow(draw_list):
  win = MyWindow(draw_list)
  win.show_all()
  Gtk.main()