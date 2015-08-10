import re

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
    self.style = None
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

def to_px(x):
  return int(x)


class BlockBox(Box):
  def layout_block(self, container):
    self.calculate_width(container)
    self.calculate_position(container)
    self.layout_children()
    self.calculate_height()

  def calculate_width(self, container):
    margin = self.style.get("margin", 0)
    border = self.style.get("border-width", 0)
    padding = self.style.get("padding", 0)

    minimum = sum(map(lambda x: to_px(x, container), [margin, border, padding]))

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
  box.style = node
  return box
