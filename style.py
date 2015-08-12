import dom
import css

class Node():
  def __init__(self, dom = None, values = [], children = []):
    self.dom = dom
    self.values = values
    self.children = children
  def get(self, key, val = None):
    return self.values.get(key, val)
  def try_get(self, key_g, fallback = None):
    for key in key_g:
      val = self.values.get(key, None)
      if val:
        return val
    return fallback
  def display(self):
    return self.values.get("display", "block")
  def print_node(self, ident = 0):
    space = "  "*ident
    print(space + "<" + self.dom.tag_name + ">" + str(self.values))
    for child in self.children:
      child.print_node(ident+1)


def matches_selector(node, selector):
  if selector.tag_name and selector.tag_name != node.tag_name:
    return False
  if selector.class_ and selector.class_ not in node.classes():
    return False
  if selector.id and selector.id != node.id():
    return False
  return True

def find_rules(node, rules):
  matched = []
  for rule in rules:
    if matches_selector(node, rule.selectors[0]):
      matched.append(rule)
  return matched

def get_values(node, rules):
  matched = find_rules(node, rules)
  values = {}
  for rule in matched:
    for attr in rule.declarations:
      values[attr.name] = attr.value
  return values

def get_style_tree(node, rules):
  if not isinstance(node, dom.ElementNode):
    return None
  values = get_values(node, rules)
  children = []
  for child in node.children:
    ch = get_style_tree(child, rules)
    if ch:
      children.append(ch)
  return Node(node, values, children)
