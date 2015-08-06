import dom
import css
import style
import layout

def print_tree(node, ident = 0):
  print "  "*ident + node.__class__.__name__
  if hasattr(node, 'children'):
    for child in node.children:
      print_tree(child, ident+1)

html_text = '''
<span class="rojo"><a>enlace</a>rojo</span>
<span class="azul">azul</span>
<span id="cosa">COSA!!</span>
<p>Parrafo con <a>un enlace</a></p>
<span>OTRA</span>
'''

css_text = '''
p {color:black;}
a {sub:true;display:none;}
span {display:inline;}
span.rojo {color:rojo;}
.azul{color:azul;}
#cosa{unique:true;}
'''

dom_tree = dom.parse(html_text)
css_tree = css.parse(css_text)

style_tree = style.get_style_tree(dom_tree, css_tree)

layout_tree = layout.build_layout_tree(style_tree)

print_tree(layout_tree)