import shared

class Rule():
  def __init__(self, sel = [], dec = []):
    self.selectors = sel
    self.declarations = dec
  def print_rule(self):
    print "{"
    for sel in self.selectors:
      print "  [tag:" + sel.tag_name + "]"
      print "  [id:" + sel.id + "]"
      print "  [class:" + sel.class_ + "]"
    for decl in self.declarations:
      print "  " + decl.name + ":" + decl.value
    print "}"

class Selector():
  def __init__(self):
    self.tag_name = ""
    self.id = ""
    self.class_ = ""

class Declaration():
  def __init__(self, name = "", value = None):
    self.name = name
    self.value = value

class Parser(shared.Parser):
  def parse_identifier(self):
    return self.consume_pattern("[a-zA-Z0-9]")

  def parse_rules(self):
    rules = []
    while not self.eof():
      rules.append(self.parse_rule())
      self.consume_space()
    return rules

  def parse_rule(self):
    selectors = self.parse_selectors()
    assert self.consume_char() == "{"
    self.consume_space()
    decl = []
    while self.char() != "}":
      decl.append(self.parse_declaration())
      self.consume_space()
    self.consume_char()
    return Rule(selectors, decl)

  def parse_declaration(self):
    name = self.parse_identifier()
    assert self.consume_char() == ":"
    value = self.parse_identifier()
    assert self.consume_char() == ";"
    return Declaration(name, value)

  def parse_selectors(self):
    selector = Selector()
    while True:
      self.consume_space()
      if self.char() == "{":
        break
      if self.char() == ".":
        self.consume_char()
        selector.class_ = self.parse_identifier();
      elif self.char() == "#":
        self.consume_char()
        selector.id = self.parse_identifier();
      else:
        selector.tag_name = self.parse_identifier();
        assert len(selector.tag_name) > 0
    return [selector]

def parse(inp):
  parser = Parser(inp)
  return parser.parse_rules();

def print_rules(rules):
  for rule in rules:
    rule.print_rule()