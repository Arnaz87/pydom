import dom
import css
import style

html_text = '''
<span class="rojo"><a>enlace</a>rojo</span>
<span class="azul">azul</span>
<span id="cosa">COSA!!</span>
<p>Parrafo con <a>un enlace</a></p>
'''

css_text = '''
p {color:black;}
a {sub:true;}
span.rojo {color:rojo;}
.azul{color:azul;}
#cosa{unique:true;}
'''

dom_tree = dom.parse(html_text)
css_tree = css.parse(css_text)

style_tree = style.get_style_tree(dom_tree, css_tree)