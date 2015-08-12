class DrawCommand():
  def draw(cairo_context):
    pass

class BlockDraw(DrawCommand):
  def __init__(self, node):
    cont = node.dimension.content
    self.x1 = cont.x
    self.x2 = cont.x + cont.width
    self.y1 = cont.y
    self.y2 = cont.y + cont.height
    color = node.style.get("color")
    if color == "red":
      self.set_color(1,0,0)
    elif color == "green":
      self.set_color(0,1,0)
    else:
      self.set_color(1,1,1)
  def set_color(self, r, g, b, a = 1):
    self.r = r
    self.g = g
    self.b = b
    self.a = a
  def draw(cr):
    cr.set_source_rgba(self.r, self.g, self.b, self.a)
    cr.rectangle(self.x1, self.y1, self.x2, self.y2)
    cr.fill()
  def print_node(self):
    print("draw_rect:")
    print("  r:" + str(self.r) + ", g:" + str(self.g) + \
          ", b:" + str(self.b) + ", a:" + str(self.a))
    print("  x1:" + str(self.x1) + ", y1:" + str(self.y1) + \
          ", x2:" + str(self.x2) + ", y2:" + str(self.y2))

def get_draw_list(node, lst = []):
  if node.style != None:
    lst.append(BlockDraw(node))
  for child in node.children:
    get_draw_list(child, lst)
  return lst