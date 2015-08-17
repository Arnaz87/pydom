class DrawCommand():
  def draw(cairo_context):
    pass

class BlockDraw(DrawCommand):
  def __init__(self, node):
    cont = node.dimension.content
    self.x = cont.x
    self.y = cont.y
    self.w = cont.width
    self.h = cont.height
    color = node.style.get("color")
    if color == "red":
      self.set_color(1,0,0)
    elif color == "green":
      self.set_color(0,1,0)
    elif color == "blue":
      self.set_color(0,0,1)
    elif color == "gray":
      self.set_color(0.5,0.5,0.5)
    elif color == "black":
      self.set_color(0,0,0)
    else:
      self.set_color(1,1,1)
  def set_color(self, r, g, b, a = 1):
    self.r = r
    self.g = g
    self.b = b
    self.a = a
  def draw(self, cr):
    cr.set_source_rgba(self.r, self.g, self.b, self.a)
    cr.rectangle(self.x, self.y, self.w, self.h)
    cr.fill()
  def print_node(self):
    print("draw_rect:")
    print("  r:" + str(self.r) + ", g:" + str(self.g) + \
          ", b:" + str(self.b) + ", a:" + str(self.a))
    print("  x:" + str(self.x) + ", y:" + str(self.y) + \
          ", w:" + str(self.w) + ", h:" + str(self.h))

def get_draw_list(node, lst = []):
  if node.style != None:
    lst.append(BlockDraw(node))
  for child in node.children:
    get_draw_list(child, lst)
  return lst