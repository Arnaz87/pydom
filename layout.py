class Dimension():
  def __init__(self):
    self.content = Rect()
    self.padding = Edge()
    self.border = Edge()
    self.margin = Edge()

class Rect():
  def __init__(self):
    self.x = 0
    self.y = 0
    self.w = 0 # width
    self.h = 0 # height

class Edge():
  def __init__(self):
    self.left = 0
    self.right = 0
    self.top = 0
    self.bottom = 0

class Box():
  def __init__(self):
    self.dimension = Dimension()
    self.children = []
  def get_inline_box(self):
    if not isinstance(self.children[-1], AnonymousBox):
      self.children.append(AnonymousBox())
    return self.children[-1]
  def add_child(self, child):
    pass


class BlockBox(Box):
  pass

class InlineBox(Box):
  pass

class AnonymousBox(Box):
  pass

def build_layout_tree(node):
  display = node.display()
  if display == "block":
    box = BlockBox()
  elif display == "inline":
    box = InlineBox()
  else:
    return
  