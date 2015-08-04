import dom
import css

class Node():
  def __init__(self, dom = None, values = []):
    self.dom = dom
    self.values = values
  def display(self):
    return self.dom.display()


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

def get_style_tree(nodes, rules):
  tree = add_style_tree([], nodes, rules)
  return tree

def add_style_tree(tree, nodes, rules):
  for node in nodes:
    if not isinstance(node, dom.ElementNode):
      continue
    values = get_values(node, rules)
    tree.append(Node(node, values))
    #tree.append(node)
    if len(node.children) > 0:
      tree = add_style_tree(tree, node.children, rules)
  return tree
