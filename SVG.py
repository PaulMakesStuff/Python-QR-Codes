#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SVG:
    
    xml = ''   

    def add_rect(self, x, y):
        self.xml += '<rect x="'+str(80 + x)+'" y="'+str(80 + y)+'" width="20" height="20" style="fill:rgb(0,0,0);stroke:none"/>'
    
    def add_coloured_rect(self, x, y, colour):
        self.xml += '<rect x="'+str(80 + x)+'" y="'+str(80 + y)+'" width="20" height="20" style="fill:' + colour + ';stroke:none"/>'
        
    def prep_for_drawing(self, width, height):
        self.xml += '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(width)+'" height="'+str(height)+'" style ="fill:none;">'
        self.xml += '<style>.svg_txt{font-size:20px;}.glyph{stroke:#000000;stroke-width:1;stroke:1;}</style>'
        
    def save(self, filename):
        self.xml += '</svg>'
        f = open(filename,'w')
        f.write(self.xml)
        f.close()
        