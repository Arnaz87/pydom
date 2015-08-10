import re

class Dimension():
  def __init__(self):
    self.content = Rect()
    self.padding = Edge()
    self.border = Edge()
    self.margin = Edge()
  def get_height(self):
    return self.content.height + self.margin.get_height() + \
           self.border.get_height() + self.padding.get_height()

class Rect():
  def __init__(self):
    self.x = 0
    self.y = 0
    self.width = 0 # width
    self.height = 0 # height
  def get_string(self):
    return "x:" + str(self.x) + ", y:" + str(self.y) + ", w:" + \
           str(self.width) + ", h:" + str(self.height)

class Edge():
  def __init__(self):
    self.left = 0
    self.right = 0
    self.top = 0
    self.bottom = 0
  def set_all(self, x):
    self.left = x
    self.right = x
    self.top = x
    self.bottom = x
  def get_height(self):
    return self.top + self.bottom
  def get_string(self):
    return "l:" + str(self.left) + ", r:" + str(self.right) + \
           ", t:" + str(self.top) + ", d:" + str(self.bottom)

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
  # Container es una instancia de Rect
  def layout_box(self, container):
    pass
  def print_node(self, ident = 0):
    space = "  " * ident
    print space + self.__class__.__name__
    space = "  " * (ident + 1)
    print space + self.dimension.content.get_string()
    print space + "margin = " + self.dimension.margin.get_string()
    print space + "border = " + self.dimension.border.get_string()
    print space + "padding = " + self.dimension.padding.get_string()
    print space + "children:"
    for child in self.children:
      child.print_node(ident + 2)

def to_px(x, container = None):
  if x == "auto":
    return 0
  return int(x)

def get_edges(style, name):
  edge = Edge()
  edge.left = style.try_get([name + "_left", name], 0)
  edge.right = style.try_get([name + "_right", name], 0)
  edge.up = style.try_get([name + "_up", name], 0)
  edge.down = style.try_get([name + "_down", name], 0)


class BlockBox(Box):
  # Container es una instancia de Rect
  def layout_box(self, container):
    self.calculate_width(container)
    self.calculate_position(container)
    self.layout_children()
    self.calculate_height()

  def calculate_width(self, container):
    margin_left = self.style.try_get(["margin_left", "margin"], 0)
    margin_right = self.style.try_get(["margin_right", "margin"], 0)
    border_left = self.style.try_get(["border_left", "border"], 0)
    border_right = self.style.try_get(["border_right", "border"], 0)
    padding_left = self.style.try_get(["padding_left", "padding"], 0)
    padding_right = self.style.try_get(["padding_right", "padding"], 0)
    width = self.style.get("width", "auto")

    # Tamano minimo requerido para mostrar todo el contenido
    total = sum(map(lambda x: to_px(x, container), [
      margin_left, margin_right, border_left, border_right,
      padding_left, padding_right, width]))

    # Pixeles que faltan para ocupar todo el espacio del contenedor.
    # Si es negativo, este Bloque es mas ancho que el contenedor.
    underflow = container.width - total

    # Si underflow es negativo, el contenido es mas grande que el contenedor.
    if underflow < 0:
      margin_right = underflow
    elif width == "auto":
      width = underflow
    elif margin_left == margin_right == "auto":
      margin_left = margin_right = underflow/2
    elif margin_left == "auto":
      margin_left = underflow
    elif margin_right == "auto":
      margin_right = underflow
    else:
      margin_right = to_px(margin_right) + underflow

    d = self.dimension
    d.margin.right = to_px(margin_right)
    d.margin.left = to_px(margin_left)
    d.border.right = to_px(border_right)
    d.border.left = to_px(border_left)
    d.padding.right = to_px(padding_right)
    d.padding.left = to_px(padding_left)
    d.content.width = width

  def calculate_position(self, container):
    d = self.dimension
    d.margin.top = to_px(self.style.try_get(["margin_top", "margin"], 0))
    d.margin.bottom = to_px(self.style.try_get(["margin_bottom", "margin"], 0))
    d.border.top = to_px(self.style.try_get(["border_top", "border"], 0))
    d.border.bottom = to_px(self.style.try_get(["border_bottom", "border"], 0))
    d.padding.top = to_px(self.style.try_get(["padding_top", "padding"], 0))
    d.padding.bottom = to_px(self.style.try_get(["padding_bottom", "padding"], 0))

    d.x = container.x + d.margin.left + d.border.left + d.padding.left
    d.y = container.y + container.height + \
          d.margin.top + d.border.top + d.padding.top

  def layout_children(self):
    for child in self.children:
      child.layout_box(self.dimension.content)
      self.dimension.content.height += child.dimension.get_height()

  def calculate_height(self):
    height = self.style.get("height", "auto")
    if height != "auto":
      self.dimension.height = to_px(height)


class InlineBox(Box):
  pass

class AnonymousBox(BlockBox):
  def layout_box(self, container):
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
