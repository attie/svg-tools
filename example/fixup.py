#!/usr/bin/env python3.6

from lxml import etree

with open('logo_font.svg', 'rb') as f:
    doc = f.read()

tree = etree.fromstring(doc)
ns = { 'x': 'http://www.w3.org/2000/svg' }

from svg_tools.translate import SvgTranslate

for glyph in tree.xpath('/x:svg/x:font/x:glyph', namespaces=ns):
    code = glyph.xpath('./@unicode', namespaces=ns)[0]
    path = glyph.xpath('./@d', namespaces=ns)[0]

    if code == 'a':
        print('code: a')
        t = SvgTranslate(translate=(0,-121), scale=(1,-1))
        glyph.attrib['d'] = ''.join(t.parse(path))
        del t

with open('logo_font_fixed.svg', 'wb') as f:
    etree.ElementTree(tree).write(f, pretty_print=True)
