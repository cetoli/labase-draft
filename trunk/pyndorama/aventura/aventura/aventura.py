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

__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: carlo $"
__version__ = "1.0 $Revision: 1.18 $"[10:-1]
__date__    = "2006/04/24 $Date: 30/06/2006 16:18:46 $"

MAPA_MUNDI={}
CANNOT_FIND_OBJECT='Nao vejo necas de %s aqui'
CANNOT_PERFORM_ACTION='Nao deu certo essa de %s'
ACTION_IS_USELESS='Nada acontece caso voce %s'
YOU_CAN_SEE='\nVoce pode ver:' 
class UselessAction(Exception):
  pass
class Thing(object):
    """Anything whatsoever - Uma coisa qualquer."""
    def __init__(self,value,*args):
        if len(value) <2 : value.append('')
        self.key = value[0] and str(value[0])[:4] or value[0]
        self.value = self.wrap_long_text_to_fixed_width(value[-1])
        self.following = None
        self.finalizer = lambda: None
    def setNext(self,next):
        self.following= next
    def additself(self,target):
      """Double-dispatch response during initialization
      -- Resposta do double dispatch de inicializacao."""
      target.append(self)
    def perform(self,statement,place=None):
      return self.value + '\n'+ self.following.perform(statement,place)
    def invoke_finalizer_hook_from_outer_application(self):
      self.finalizer()
    def normalize(self,key):
      """converte unicode, limita tamanho e muda para caixa alta."""
      return util.latin1_to_ascii(key[:4].upper())
    def wrap_long_text_to_fixed_width(self,description):
      """Quebra texto longo em linhas menores"""
      words = description.split(' ')
      self.count = 0
      def break_when_past_end(self, word):
        wordcount = sum([letter.isupper() and 3 or 2 for letter in word])+2
        self.count += wordcount
        if self.count > 100:
          self.count = wordcount
          return "\n"+word
        return word
      wrap_text = ' '.join([break_when_past_end(self, word) for word in words])
      #Strip blanks from the end of lines:
      return '\n'.join([ line.strip() for line in wrap_text.split('\n')])

class Things(Thing):
    """Coletivos."""
    def __init__(self,value,*args):
        Thing.__init__(self,value,args)
        self.contents={}
        self.args = args[:][0]
        if len(self.args) and isinstance(self.args[0],list):
          self.args = self.args[0]
        self.active = False
        for coisa in self.args:
            coisa.additself(self)
    def append(self,athing):
      """adiciona na colecao"""
      if isinstance(athing.key,list):
        for key in athing.key:self.contents[key]=athing
      else:
        self.contents[athing.key]=athing
    def pop(self,athing):
      """remove da colecao"""
      self.contents.pop(athing.key)
    def find(self,key):
      """procura na colecao"""
      return self.contents[self.normalize(key)]
    def has(self,key):
      """verifica se tem na colecao"""
      return self.contents.has_key(self.normalize(key))
    def __repr__(self):
      return "<%s>"%self.key
    def parse(self,statement,place):
      if not (statement[0:] and statement[0] ):return self.show()
      for noum in statement:
        if self.has(noum):
          statement.pop(statement.index(noum)) 
          return self.find(noum).perform(statement,place)
      return None
    def show(self):
        """mostra o conteudo da localizacao"""
        return self.value
      
class ChainEnd(Thing):
  """Objeto nulo para fechar o fim da chain"""
  def perform(self,statement,place=None):
    return ''
CHAIN_END=ChainEnd(['END'])

class Chain(Thing):
    """O conteudo eh uma Chain of Responsibility."""
    def __init__(self,value,*args):
        Thing.__init__(self,value,args)
        arguments=args[:][0]
        if len(arguments) and isinstance(arguments[0],list):
          arguments = arguments[0]
        self.contents = CHAIN_END
        for item in arguments:
            self.contents ,self.contents.following = item,self.contents


class Local(Things):
    """Representa um Inventario com varios objetos."""
    def __init__(self,value,*args):
      Things.__init__(self,value,args)
      MAPA_MUNDI[self.key]=self
    def perform(self,statement,place):
      return self.parse(statement,place)
    def show(self):
      """mostra o conteudo da localizacao"""
      response = self.value + YOU_CAN_SEE
      for item in self.contents.values():
          if item.value: response += '\n\t'+ item.value
      if not self.contents.values():
          response += '\n\tNADA AQUI'
      return response
      
class I(Thing):
    """Descreve a tela inicial."""
    def __init__(self,value):
        self.key = value[0]
        
class D(Thing):
    """Descreve uma coisa."""
    def __init__(self,value):
        self.key = value[0]
        self.value = value[1]
    def additself(self,target):
      target.value += '\n'+self.value

class L(Local):
    """Representa um Lugar com varios objetos."""
    def __init__(self,value,*args):
      Things.__init__(self,value,args)
      MAPA_MUNDI[self.key]=self
    def perform(self,statement,place):
      question = statement[:]
      try:
        found = inventario.perform(statement,place)
        if found: return found
        found = self.parse(statement,place)
        if found: return found
        if statement[1:]:
          return CANNOT_FIND_OBJECT % statement[-1]
        raise KeyError
      except KeyError:
        return CANNOT_PERFORM_ACTION % (' '.join(question))
      except UselessAction:
        return ACTION_IS_USELESS % (' '.join(question))
    def find(self,key):
      """procura na colecao"""
      if inventario.has(key):
        return inventario.find(key)
      return self.contents[self.normalize(key)]

inventario = Local(['INVE', 'Voce examina o seu inventario.'])
playadventure = True

class Z(Things):
    """Representa o mundo."""
    def __init__(self,value,*args):
      Things.__init__(self,value,args)
      self.currentPlace = self.args[-1] # the last place is the beginning
      #print self.currentPlace
      self.response = self.perform([])
      self.can=True
      self.prompt = '\nO que devo fazer agora?\n'
      self.actions = {
      'QUIT':lambda self= self: self.dismiss(),
      'INVE':lambda self= self: self.report(),
      'OLHE':lambda self= self: self.show()
      }
      
    def play(self):
      """Continua a aventura enquanto pode."""
      #print 'Aventura'
      while playadventure:
        self.perform(self.question(self.forSituation()))
      print self.response
    def forSituation(self):
      """Concatena a resposta com uma nova pergunta"""
      return self.response +self.prompt
    def question(self,query):
      """Imprime a resposta e pede o novo comando"""
      ## query = util.latin1_to_ascii(query)
      #query = query.encode('latin1')
      query = query.encode('utf8')
      return raw_input(query).decode('utf8').split(' ')
#      return util.latin1_to_ascii(raw_input(query)).split(' ')
##      return raw_input(query).split(' ')
    def processaQuery(self,query):
        query=query.encode('utf8').split(' ')
        return self.perform(query).decode('utf8')   
    def getImage(self):
        return '/static/images/' + self.currentPlace.key + '.gif'
    
    def publicaRSSQuery(self,query):
        rss = PyRSS2Gen.RSS2(
             title = "Pyndorama RSS",
             link = "",
             description = "Comandos do jogador da aventura",

             lastBuildDate = datetime.datetime.now(),

             items = [
                      PyRSS2Gen.RSSItem(
                      title = "RSS comando",
                      link = "",
                      description = query)
                      ])

        rss.write_xml(open("pyrss2gen.xml", "w"))
        return rss
    def dismiss(self):
      """finaliza aventura"""
      global playadventure
      playadventure=False
      self.response= 'XXX --- ACABOU A SUA AVENTURA !!! --- XXX'
      self.invoke_finalizer_hook_from_outer_application()
      return self.response
    def report(self):
      return inventario.show()
    def show(self):
      self.response= self.currentPlace.show()
      return self.response
    def perform(self,statement,place=None):
      here=self.currentPlace
      self.response=self.parse(statement,self)
      if not self.response :
        self.response=here.perform(statement,self)
      return self.response
    def parse(self,statement,place):
      verb=''
      if not (statement[0:] and statement[0] ):return self.show()
      verb=statement[0]
      if statement[1:]:
        return None
      if (not self.actions.has_key(verb[:4].upper())):
        return None
      return self.actions[verb[:4].upper()]()
    def pop(self,athing):
      """remove da colecao"""
      if not inventario.has(athing.key): return
      self.currentPlace.append(athing)
      inventario.pop(athing)
    def push(self,athing):
      """remove da colecao"""
      if not self.currentPlace.has(athing.key): return
      self.currentPlace.pop(athing)
      inventario.append(athing)
    def finish(self):
      """finaliza aventura"""
      self.can = False
    def goto(self,place):
      """move para um lugar"""
      location = MAPA_MUNDI[place[:4].upper()]
      self.currentPlace = location
      return self.currentPlace
    def find(self,key):
      """procura na colecao"""
      if inventario.has(key):
        return inventario.find(key)
      return self.currentPlace.find(key)
    
class O(Things):
    """Representa um Objeto que suporta varias acoes"""
    def __init__(self,value,*args):
      Things.__init__(self,value,args)
    def perform(self,statement,place=None):
      found = self.parse(statement,place)
      if found : return found
      if statement.count("olhe"):
        return self.value
      raise UselessAction
class V(Chain):
    """Representa um verbo com variantes de acoes sobre objetos"""
    def __init__(self,value,*args):
      Chain.__init__(self,value,args)
    def perform(self,statement,place=None):
      try:
        if self.value:
          return self.value +'\n'+ self.contents.perform(statement,place)
        return self.contents.perform(statement,place)
      except KeyError:
        return CANNOT_PERFORM_ACTION %(' '.join(statement)) +' ..'
    
class P(Thing):
    """Pega objeto e poe no inventario"""
    def __init__(self,value,*args):
      Thing.__init__(self,value,args)
    def perform(self,statement,place=None):
      obj = place.find(self.key)
      try:
        place.push(obj)
        return self.value + '\n'+ self.following.perform(statement,place)
      except KeyError:
        return CANNOT_PERFORM_ACTION %(' '.join(statement)) +' ...'
    
class T(Thing):
    """Pega objeto e tira do inventario"""
    def __init__(self,value,*args):
      Thing.__init__(self,value,args)
    def perform(self,statement,place=None):
      obj = place.find(self.key)
      try:
        place.pop(obj)
        return self.value + '\n'+ self.following.perform(statement,place)
      except KeyError:
        return CANNOT_PERFORM_ACTION %(' '.join(statement)) +' ...'
  
class A(Thing):
    """Ativa objeto"""
    def perform(self,statement,place=None):
      obj = place.find(self.key)
      obj.active = True
      return self.value + '\n'+ self.following.perform(statement,place)
class B(Thing):
    """Bloqueia objeto"""
    def perform(self,statement,place=None):
      obj = place.find(self.key)
      obj.active = False
      return self.value + '\n'+ self.following.perform(statement,place)
    
class E(Thing):
    """Ativa objeto, trocando a sua descricao"""
    def perform(self,statement,place=None):
      obj = place.find(self.key)
      obj.active = True
      obj.value = self.value
      return self.following.perform(statement,place)
class U(Thing):
    """Bloqueia objeto, trocando a sua descricao"""
    def perform(self,statement,place=None):
      obj = place.find(self.key)
      obj.active = False
      obj.value = self.value
      return self.following.perform(statement,place)

class S(Thing):
    """testa se objeto estah ativo"""
    def perform(self,statement,place=None):
      try:
        obj = place.find(self.key)
        if not obj.active:
          return self.value
        else:
          return self.following.perform(statement,place)
      except KeyError:
        return self.value
class R(Thing):
    """testa se objeto estah bloqueado"""
    def perform(self,statement,place=None):
      try:
        obj = place.find(self.key)
        if obj.active:
          return self.value
        else:
          return self.following.perform(statement,place)
      except KeyError:
        return self.value
class M(Thing):
    """Move para o lugar"""
    def perform(self,statement,place=None):
      return self.value + '\n'+ place.goto(self.key).show() + '\n'+ self.following.perform(statement,place)
    #def perform(self,statement,place=None):
     # return self.value + '\n'+ place.goto(self.key).show()
class F(Thing):
    """Finaliza a aventura"""
    def perform(self,statement,place=None):
      return self.value + '\n'+ place.dismiss()

g = globals()

for t in range (ord('A'),ord('Z')):
  if chr(t) not in g.keys():
    g[chr(t)] = type(chr(t), (Thing,), {})
  
def load(aventura='ave.yaml'):
  return load_yaml(yaml.load(file(aventura, 'r'))[0])
  '''return load_yaml(yaml.load(file('/home/livia/labase-draft/pyndorama/aventura/aventura/'+aventura, 'r'))[0])'''
def load_yaml(thing):
  global g
  thing_name = thing.keys()[0]
  thing_definition = thing.pop(thing_name)
  thing_value = thing_definition[0]
  thing_contents = [load_yaml(athing) for athing in thing_definition[1:]]
  #print thing_name, ' > ' ,thing_contents
  if thing_contents:
    return g[thing_name](thing_value,thing_contents)
  else:
    return g[thing_name](thing_value)

if __name__ == '__main__':
  load().play()


