#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
###############################################
ActivUFRJ - A rede Social Acadêmica da UFRJ
###############################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2009/08/08  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `LABASE <http://labase.nce.ufrj.br/>`__
:Copyright: ©2009, `GPL <http://is.gd/3Udt>__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2009/08/08 $Date$"
from xml.dom import minidom

KEYS=dict(
       style="style"
       ,width="width"
       ,height="height"
       ,x="x"
       ,y="y"
       )
KEYS['inkscape:label']="classname"
CSSOUT='''
%(classname)s {
  position: absolute;
  text-align: left;
  left: %(x)spx;
  top: %(y)spx;
  margin-top: 5px;
  width: %(width)spx;
  height: %(height)spx;
  margin-left: 0;
  margin-right: 0;
  background: %(style)s;
}

'''

CSSTEMPLATE='''
* .grandContainer {
  position: relative;
  position: absolute;
  text-align: left;
  left: 100px;
  height: 600px;
  width: 1000px;
  border: 2px solid black;
}
* .parent {
  margin: 10px;
  padding: 10px;
  padding-top: 0;
  border: 1px solid black;
}
* .common {
  margin: 10px;
  padding: 5px;
  background-color: gold;
}

%s
'''

TEMPLATE="""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>ActivUFRJ</title>
<meta http-equiv="content-type" content="text/html;charset=utf-8" />

<meta name="generator" content="labase.nce.ufrj.br" />
<style type="text/css">
%s
</style>

<link rel="stylesheet" href="activ.css" type="text/css" />
</head>
<body>
%s
</body>
</html>
"""
DIV='<div id ="%(classname)s" class="common"><h1>Sessão: %(classname)s</h1><b>Profile views:</b>Since Feb 06: 1,144<br/></div>'


class Svg2Css:
    """create css from svg xml"""

    def make_css(self, source):
        """load XML input source, return parsed XML document"""
        sock = file(source, 'r')
        xmldoc = minidom.parse(sock).documentElement
        sock.close()
        return self.scan(xmldoc)

    def scan(self, node, sub={}):
        self.boxes=boxes=[dict((KEYS[key],e.attributes[key].value.encode('utf-8')) for  key in KEYS if e.hasAttribute(key))                        
            for e in node.getElementsByTagName("rect")
            if e.hasAttribute("inkscape:label") ]
        for box in boxes:
            style = box['style']
            style = dict(item.split(":") for item in style.split(";"))
            box['style']= style['fill']
        body = "\n".join(CSSOUT%box for box in self.boxes)
        self.css = CSSTEMPLATE%body
        #print self.css
        return self.css
    def make_html(self, source):
        style = self.make_css(source)
        body = "\n".join(DIV%box for box in self.boxes)
        self.html = TEMPLATE%(style, body)
        print self.html
    
def loadSVG(input_file):
    return Svg2Css().make_html(input_file)

if __name__ == '__main__':
    loadSVG('carlocard.svg')

