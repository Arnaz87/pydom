import re

class Node():
  pass

class ElementNode(Node):
  def __init__(self, tag, attrs = [], children = []):
    self.tag_name = tag
    self.attributes = attrs
    self.children = children

class TextNode(Node):
  def __init__(self, text = ""):
    self.text = text

class Parser():
  def __init__(self, inp = ""):
    self.pos = 0
    self.input = inp

  def char(self):
    return self.input[self.pos]

  def next_char(self):
    return self.input[self.pos + 1]

  def consume_char(self):
    self.pos += 1
    return self.input[self.pos-1]

  def starts_with(self, query):
    return self.input.startswith(query, self.pos)

  def eof(self):
    return self.pos >= len(self.input)

  def consume_while(self, test):
    result = ""
    while not self.eof() and test(self.char()):
      result += self.consume_char()
    return result

  def consume_pattern(self, pattern):
    return self.consume_while(lambda c: bool(re.match(pattern, c)))

  def consume_space(self):
    return self.consume_while(lambda c: c in (" ", "\n", "\t", "\r"))

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

