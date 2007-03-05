#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
Pyndorama: An adventure trip around the world.
Pyndorama: Uma viagem de aventura ao redor do mundo
===================================================

A text based adventure that can be programmed.
Uma aventura baseada em texto que pode se programada.

Copyright (c) 2002-2007
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""
import util
import yaml
#import PyRSS2Gen
import datetime
import xml.dom.minidom

from xml.dom.minidom import Node

__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author$"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2007/03/04 $Date$"

class MOFTypeElement(dict):
  references = {}
  def aggregate(self,element):
    className=element.__class__.__name__
    if element.has_key(XMI_ID): references[element[XMI_ID]]=element
    if not self.has_key(className): self[className]=[]
    self[className].append(element)
  
MOFTypes=['Class','Stereotype','Association','AssociationEnd','Model'
,'ModelElement.stereotype','Association.connection','AssociationEnd'
,'AssociationEnd.multiplicity','Multiplicity','Multiplicity.range'
,'MultiplicityRange','AssociationEnd.participant','Namespace.ownedElement']

g = globals()

def makeMofTypeName(name): return 'Mof' + name.replace('.','_')

def makeMofType(element): 
  createinstance = '%s()'%makeMofTypeName(element.name)
  instance = eval(createinstance)
  instance.update(element.attributes)
  return 

for t in MOFTypes:
  if t not in g.keys():
    g[t] = type(makeMofTypeName(t), (MOFTypeElement,), {})
  
def load(aventura="crowpitcher.xmi"):
  return xml.dom.minidom.parse(aventura)

def parse(dom):
  model = {}
  nameSpace = 'org.omg.xmi.namespace.UML'
  [ model.put(element,makeMofType(element)) 
    and model[element.parentNode].aggregate(model[element]) 
    for element in dom.getElementsByTagNameNS(nameSpace,moftype) 
    for moftype in MOFTypes
  ]
  return model

if __name__ == '__main__':
  parse(load())


