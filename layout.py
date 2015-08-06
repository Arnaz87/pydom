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
    if len(self.children) < 1 or not isinstance(self.children[-1], AnonymousBox):
      self.children.append(AnonymousBox())
    return self.children[-1]
  def add_child(self, child):
    if isinstance(child, BlockBox):
      self.children.append(child)
    elif isinstance(child, InlineBox):
      anon = self.get_inline_box()
      anon.children.append(child)


class BlockBox(Box):
  pass

class InlineBox(Box):
  pass

class AnonymousBox(BlockBox):
  pass

def build_layout_tree(node):
  display = node.display()
  if display == "none":
    return None
  elif display == "inline":
    box = InlineBox()
  else:
    box = BlockBox()
  for child in node.children:
    box.add_child(build_layout_tree(child))
  return box
