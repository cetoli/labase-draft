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
#import yaml
#import PyRSS2Gen
import datetime
import xml.dom.minidom

from xml.dom.minidom import Node

__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author$"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2007/03/04 $Date$"

XMI_ID= 'xmi.id'
XMI_IDREF= 'xmi.idref'
MOF_PARENT = 'mof.parent'
class MOFTypeElement(dict):
  references = {}
  def register(self,model,parentkey):
    if self.has_key(XMI_ID): self.references[self[XMI_ID]]=self
    if model.has_key(parentkey) :
      className=self.__class__.__name__
      parent = model[parentkey]
      if not parent.has_key(className): parent[className]=[]
      parent[className].append(self)
      self[MOF_PARENT]=parent
  def aggregate(self):
    if self.has_key(XMI_IDREF): 
      className=self.__class__.__name__
      if self.has_key(MOF_PARENT): className=self[MOF_PARENT].__class__.__name__
      referree = self.references[self[XMI_IDREF]]
      refClassName=referree.__class__.__name__
      if not self.has_key(refClassName): self[refClassName]=[]
      self[refClassName].append(referree)
      if not referree.has_key(className): referree[className]=[]
      referree[className].append(self)
    
class MofDom:
  
  MOFTypes = ['Model','Stereotype','Association','AssociationEnd'
    ,'ModelElement.stereotype','Association.connection'
    ,'AssociationEnd.multiplicity','Multiplicity','Multiplicity.range'
    ,'MultiplicityRange','AssociationEnd.participant','Namespace.ownedElement','Class'
  ]


  def __init__(self):
    g = globals()
    for t in self.MOFTypes:
      if t not in g.keys():
        clazzname=self.makeMofTypeName(t)
        g[clazzname] = type(clazzname, (MOFTypeElement,), {})

  def makeMofTypeName(self, name): return 'Mof' + name.replace('.','_')

  def makeMofTypeInstance(self, element): 
    createinstance = '%s()'%self.makeMofTypeName(element._get_localName())
    instance = eval(createinstance)
    instance.update(
     (name,attribute) for name,attribute in element.attributes.items()
    )
    instance.mofType=element._get_localName()
    return instance
  
    
  def load(self, aventura="crowpitcher.xmi"):
    return xml.dom.minidom.parse(aventura)
  
  def parse(self, dom):
    model = {}
    nameSpace = 'org.omg.xmi.namespace.UML'
    [ model.update({element:self.makeMofTypeInstance(element)}) 
      or model[element].register(model,element.parentNode)
      for moftype in self.MOFTypes
      for element in dom.getElementsByTagNameNS(nameSpace,moftype) 
    ]
    [ element.aggregate() 
      for element in model.values()
    ]
    return model
    
  def make(self):
    self.root = self.parse(self.load())
    return self

if __name__ == '__main__':
  mofDom = MofDom().make()
  print [key['name'] for key in mofDom.root.values() 
  if key.mofType == 'Class' and key.has_key('name')]
  clz={}
  clz.update((value['name'],value) for value in mofDom.root.values() 
  if value.mofType == 'Class' and value.has_key('name'))
  print clz['Valley']
  print clz['River']
  print clz['Fly']


