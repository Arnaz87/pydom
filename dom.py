import re
import shared

indent_spaces = 2

class Node():
  pass

class ElementNode(Node):
  def __init__(self, tag, attrs = [], children = []):
    self.tag_name = tag
    self.attributes = attrs
    self.children = children
  def print_node(self, indent):
    space = " " * indent_spaces * indent
    space_d = " " * (indent_spaces * (indent + 1))
    print space + "<" + self.tag_name + ">"
    for key in self.attributes:
      print space_d + key + "=" + self.attributes[key]
    print space_d + "children :"
    for node in self.children:
      node.print_node(indent + 2)


class TextNode(Node):
  def __init__(self, text = ""):
    self.text = text
  def print_node(self, indent):
    space = " " * indent_spaces * indent
    print space + "TEXT:" + self.text


class Parser(shared.Parser):
  def parse_tag_name(self):
    return self.consume_pattern("[a-zA-Z0-9]")

  def parse_text_node(self):
    return TextNode( self.consume_while(lambda c: c != "<") )

  def parse_open_tag(self):
    assert self.consume_char() == "<"
    name = self.parse_tag_name()
    attrs = self.parse_attributes()
    assert self.consume_char() == ">"
    return name

  def parse_close_tag(self):
    assert self.consume_char() == "<"
    assert self.consume_char() == "/"
    name = self.parse_tag_name()
    assert self.consume_char() == ">"
    return name

  def parse_attribute(self):
    name = self.parse_tag_name()
    assert self.consume_char() == "="

    quote = self.consume_char()
    assert(quote in ("'", "\""))
    value = self.consume_while(lambda c: c != quote)
    assert(self.consume_char() == quote)
    return (name, value)


  def parse_attributes(self):
    attrs = {}
    while True:
      self.consume_space()
      if self.eof() or self.char() == '>':
        break
      name, value = self.parse_attribute()
      attrs[name] = value
    return attrs

  def parse_element_node(self):
    assert self.consume_char() == "<"
    tag_name = self.parse_tag_name()
    attrs = self.parse_attributes()
    assert self.consume_char() == ">"

    content = self.parse_nodes()

    assert self.consume_char() == "<"
    assert self.consume_char() == "/"
    assert self.parse_tag_name() == tag_name
    assert self.consume_char() == ">"

    return ElementNode(tag_name, attrs, content)

  def parse_node(self):
    if self.char() == "<":
      return self.parse_element_node()
    return self.parse_text_node()

  def parse_nodes(self):
    nodes = []
    while True:
      if self.eof() or self.starts_with("</"):
        break
      nodes.append(self.parse_node())
    return nodes

def print_nodes(nodes, indent = 0):
  for node in nodes:
    node.print_node(indent)

def parse(inp):
  parser = Parser(inp)
  return parser.parse_nodes();
