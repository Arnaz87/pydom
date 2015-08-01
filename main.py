import dom


p = dom.Parser('Documento de prueba<span id="nombre">Este es un span y tiene un<span color="red">Rojo</span></span> y al final no tiene nada.')

print p.input
print "\n"
dom.print_nodes(p.parse_nodes())