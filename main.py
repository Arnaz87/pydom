import dom
import css
import style
import layout
import draw
import display

def print_tree(node, ident = 0):
  print("  " * ident + node.__class__.__name__)
  if hasattr(node, 'children'):
    for child in node.children:
      print_tree(child, ident+1)

def print_list(lst):
  for node in lst:
    node.print_node()

html_text = '''
<div>
  <header></header>
  <section>
    <span></span><span></span>
  </section>
  <section>
    <span></span><span></span>
  </section>
</div>
<div>
<section>
<span></span>
</section>
<span></span>
</div>
'''

css_text = '''
body {bg-color:white;}
div {bg-color:yellow;padding:5;border:1;}
section {padding:10;bg-color:cyan;height:20;border:1;}
span {display:inline;height:20;border:1;}
header {margin:10;color:black;height:30;border:1;}
'''

dom_tree = dom.parse(html_text)
css_tree = css.parse(css_text)

style_tree = style.get_style_tree(dom_tree, css_tree)

layout_tree = layout.build_layout_tree(style_tree)

window = layout.Rect()
window.width = 200
window.height = 0

layout_tree.layout_box(window)

print("LAYOUT TREE")
layout_tree.print_node()

dl = draw.get_draw_list(layout_tree)
print("DRAWING LIST")
print_list(dl)

display.CreateWindow(dl)