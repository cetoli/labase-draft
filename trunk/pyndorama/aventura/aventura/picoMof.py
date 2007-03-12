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
class MOFTypeElement(dict):pass

XMI_ID= 'xmi.id'
XMI_IDREF= 'xmi.idref'
MOF_PARENT = 'mof.parent'
MOF_NONE = MOFTypeElement()
MOF_NONE['name']= '<<MOFNONE>>'
NONES= [MOF_NONE]
class MOFTypeElement(dict):
  references = {}
  def register(self,model,parentkey):
    self.contents=[]
    if self.has_key(XMI_ID): self.references[self[XMI_ID]]=self
    if model.has_key(parentkey) : 
      #self.crossassociate(model[parentkey],key=MOF_PARENT)
      parent = model[parentkey]
      self.associate(parent,MOF_PARENT)
  def associate(self,other,key=None):
      if key : self.update({key:other})
      else: 
        key = other.__class__.__name__
        if not self.has_key(key):  self.update({key:[other]})
        else: self[key].append(other)
  def crossassociate(self,other,key=None):
      self.associate(other,key);other.associate(self)
  def navigate(self,arc,ends='MofClass'):
    associationEnd=[end for end in arc[ends] if end !=self]
    return associationEnd and associationEnd[0] or None
  def composite(self,arcs='MofAssociation'
    ,matches= lambda link,self:self.navigate(arc)):
      for arc in self[arcs]:
        match=matches(arc,self)
        if  self.navigate(arc) and matches(arc,self):
          self.contents.append(match) 
  def aggregate(self):
    daddy = lambda me:(me.has_key(MOF_PARENT) and me[MOF_PARENT]) or me
    if self.has_key(XMI_IDREF): 
      parent = daddy(daddy(self))
      if parent.mofType == 'AssociationEnd':
        #if  (parent['isNavigable']!='true'): return
        parent = daddy(daddy(parent))
      referree = self.references[self[XMI_IDREF]]    
      parent.crossassociate(referree)
      
class MofVerbAction(dict):
  mof = {}
  actionMatchers = {
      'move':{'subject':'actor','target':'location'}
      , 'take':{'subject':'object','target':'location'}
      , 'pick':{'subject':'object','target':'actor'}
      , 'activating':{'certificate':'object'}
      , 'blocking':{'uncertificate':'object'}
      , 'refutal':{'unassertive':'object'}
      , 'submission':{'assertive':'object'}
  }
  def __init__(self,action=None,actionPattern=[],name='<<NONO>>'):
    self['name']=name
    self.contents=self.buildActionTree(action,actionPattern)
    self.clz={}
    #self.mof = MofDom.mofmodel
  def buildActionTree(self,action,actionPattern):
    '''
    >>> roletree = ['submission', 'take']
    >>> mof=MofVerbAction();node={'name':'ACTION'}
    >>> mof.buildActionTree(node,roletree)
    {'name': 'takeACTION'}
    '''
    if not actionPattern: return []
    name = actionPattern.pop()+action['name']
    action = MofVerbAction(action,actionPattern,name)
    self.mof[name]=action
    return action
    
  def matchEach(self,matcher,roletree):
    '''
    >>> roletree = {'assertive':'object','hold':'object'}
    >>> matcher  = {'assertive':'object'}
    >>> MofVerbAction().matchEach(matcher,roletree)
    True
    '''
    return  not False in [
        roletree.has_key(part) and roletree[part] == value for part, value in matcher.items() 
    ]
    pass

  def actionMatched(self,node,roletree):
    '''
    >>> roletree = {'assertive':'object','hold':'object'}
    >>> mof=MofVerbAction();node={'name':'ACTION'}
    >>> mof.actionMatched(node,roletree)
    {'name': 'submissionACTION'}
    >>> roletree = {'assertive':'object','hold':'object','subject':'object','target':'location'}
    >>> mof.actionMatched(node,roletree)
    {'name': 'takeACTION'}
    '''
    self.actionKeys=[
      matchkey for matchkey, matcher in self.actionMatchers.iteritems()#]
      if self.matchEach(matcher,roletree)
    ]
    if self.actionKeys:
      return self.buildActionTree(node,self.actionKeys)
    return self.actionKeys
    
  def match(self,arcs,node):
    self.action=node
    return arcs.has_key('MofStereotype') and self.actionMatched(node,dict([
      (arcRole['name'],nodeRole['name']) for arcRole in arcs['MofStereotype'] 
      for nodeRole in node.navigate(arcs)['MofStereotype']
    ]))
    
  def buildTree(self,mofDom):
    '''
    >>> verb = MofVerbAction()
    >>> root = verb.buildTree(MofDom().make())
    >>> tuples = lambda cont: [cc['name'] for cc in cont if cc.has_key('name')]
    >>> clazzes = dict([(c['name'],tuples(c.contents)) for c in verb.clz.values() if c.has_key('name')])
    >>> [ a in [u'Valley', u'Pebble'] for a in clazzes['River']]
    [True, True]
    >>> clazzes
    []
    '''
    self.mof = mofDom.root
    self.clz.update(
      (value['name'],value) for value in mofDom.root.values()
      if value.mofType == 'Class' and value.has_key('name')
    )
    stereotypes=['world','location','object','action']
    matchrole = lambda arcs,role,self:arcs.has_key('MofStereotype') and role in [
      arole['name'] for arole in arcs['MofStereotype'] 
    ] and self.navigate(arcs)
    matchFactory=MofVerbAction()
    
    matchers={
      'world':lambda arc,self:self.navigate(arc)
      ,'location':lambda node,self=self:matchrole(node,role='hold',self=self)
      ,'object':lambda node,self=self:matchrole(node,role='imply',self=self)
      ,'action':lambda arc,node,fact=matchFactory:fact.match(arc,node)
    }
    def createChildren(holder,role):
      holder.composite(matches=matchers[role])
    [createChildren(container,stereotype) for stereotype in stereotypes for container in self.clz.values()
      if container ['MofStereotype'][0]['name'] == stereotype]
    return [root for root in self.clz.values() if 'world' == root['MofStereotype'][0]['name']][0]
    
    
class MofDom:
  
  MOFTypes = ['Model','Association','Association.connection','AssociationEnd'
    ,'AssociationEnd.multiplicity','Multiplicity','Multiplicity.range'
    ,'MultiplicityRange','AssociationEnd.participant'
    ,'Class','ModelElement.stereotype','Stereotype', 'Namespace.ownedElement'
  ]
  
  mofmodel = {}


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
    model = self.mofmodel
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

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
  _test()

  domMof = MofDom()
  mofDom = domMof.make()
 
  #print [key['name'] for key in mofDom.root.values() 
  #if key.mofType == 'Class' and key.has_key('name')]
  claz={}
  claz.update((value['name'],value) for value in mofDom.root.values() 
  if value.mofType == 'Class' and value.has_key('name'))
  '''
  print claz ['Valley']['MofStereotype'][0]['name']
  print [world for world in claz.values() if world ['MofStereotype'][0]['name'] == 'world'][0]['name']
  print [world['name'] for world in claz.values() if world ['MofStereotype'][0]['name'] == 'location']
  print [world['name'] for world in claz.values() if world ['MofStereotype'][0]['name'] == 'object']
  print [world['name'] for world in claz.values() if world ['MofStereotype'][0]['name'] == 'verb']
  print [world['name'] for world in claz.values() if world ['MofStereotype'][0]['name'] == 'action']
  print claz['Valley'].keys()
  valleyarcs = claz['Valley']['MofAssociation']
  print valleyarcs[0]['MofClass'][0]['name']
  print valleyarcs[0].keys()
  ST='MofStereotype'
  #print [(node['name'],[(clz['Valley'].navigate(arc)['name'],arc.has_key(ST) and arc[ST][0]['name'] or 'nono') for arc in node['MofAssociation']]) for node in clz.values()]
  print [node['name']+"==>"+str([(node.navigate(arc)['name'],arc.has_key(ST) and arc[ST][0]['name'] or 'nono') for arc in node['MofAssociation'] if node.navigate(arc)])+ '\n\n' for node in claz.values()]
  root = MofVerbAction().buildTree(mofDom)
  #print dict([(c['name'],[cc['name'] for cc in c.contents]) for c in claz.values()])
  '''

