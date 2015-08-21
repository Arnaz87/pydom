from gi.repository import cairo

class DrawCommand():
  def draw(cairo_context):
    pass

class Color():
  def __init__(self, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
    if arg1 != None: # Tenemos argumentos!
      if arg2 == None: # Tenemos solo 1 argumento!
        self.set_by_name(arg1)
      else:
        self.set_by_values(arg1, arg2, arg3, arg4)
    else: # Sin ningun argumento
      self.set_by_values(0,0,0,1)
  def set_by_name(self, arg):
    if arg == "red":
      self.set_by_values(1,0,0)
    elif arg == "green":
      self.set_by_values(0,1,0)
    elif arg == "blue":
      self.set_by_values(0,0,1)
    elif arg == "gray":
      self.set_by_values(0.5,0.5,0.5)
    elif arg == "black":
      self.set_by_values(0,0,0)
    else:
      self.set_by_values(1,1,1)
  def set_by_values(self, r, g, b, a = None):
    if a == None:
      a = 1
    self.r = r
    self.g = g
    self.b = b
    self.a = a


class BlockDraw(DrawCommand):
  def __init__(self, node):
    cont = node.dimension.content
    bg = node.dimension.get_padding_rect()
    self.x = bg.x
    self.y = bg.y
    self.w = bg.width
    self.h = bg.height
    color = node.style.get("color")
    self.set_color(Color(color))
  def set_color(self, c):
    self.color = c
    self.r = c.r
    self.g = c.g
    self.b = c.b
    self.a = c.a
  def draw(self, cr):
    if self.a == 0:
      return
    cr.set_source_rgba(self.r, self.g, self.b, self.a)
    cr.rectangle(self.x, self.y, self.w, self.h)
    cr.fill()
  def print_node(self):
    print("draw_rect:")
    print("  r:" + str(self.r) + ", g:" + str(self.g) + \
          ", b:" + str(self.b) + ", a:" + str(self.a))
    print("  x:" + str(self.x) + ", y:" + str(self.y) + \
          ", w:" + str(self.w) + ", h:" + str(self.h))

class BorderDraw(DrawCommand):
  def __init__(self, node):
    self.internal = node.dimension.get_padding_rect()
    self.external = node.dimension.get_border_rect()


  def draw(self, cr):
    cr.set_source_rgba(0,0,0,1)
    cr.rectangle(self.external.x, self.external.y, \
                self.external.width, self.external.height)
    cr.rectangle(self.internal.x, self.internal.y, \
                self.internal.width, self.internal.height)

    # el 1 significa cairo.FILL_RULE_EVEN_ODD.
    # TODO: ver como usar la constante de cairo en vez del número.
    cr.set_fill_rule(1)

    cr.fill()

  def print_node(self):
    print("draw_border:")
    print("  X: x:" + str(self.external.x) + ", y:" + str(self.external.y) + \
          ", w:" + str(self.external.width) + ", h:" + str(self.external.height))
    print("  I: x:" + str(self.internal.x) + ", y:" + str(self.internal.y) + \
          ", w:" + str(self.internal.width) + ", h:" + str(self.internal.height))


def get_draw_list(node, lst = []):
  if node.style != None:
    if node.has_borders():
      lst.append(BorderDraw(node))
    lst.append(BlockDraw(node))
  for child in node.children:
    get_draw_list(child, lst)
  return lst