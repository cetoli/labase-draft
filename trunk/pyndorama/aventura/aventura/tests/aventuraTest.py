#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
Dedalus - a Platform for P2P distributed computing.
===================================================

Copyright (c) 2002-2004
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""

__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: carlo $"
__version__ = "1.0 $Rev: 226 $"[10:-1]
__date__    = "2006/04/24 $Date: 23/06/2006 07:23:55 $"

import unittest
import doctest
from aventura import *

loaded_adventure=  Z( ['zz', 'www'],
 I( [''] ),
 I( ['VENICE GARDEN SOFT APRESENTA'] ),
 L( ['APAR', 'VOCE ESTA EM SEU APARTAMENTO NA'],
      D( ['x', 'CIDADE, LOUCA PARA IR AO SITIO'] ),
      O( ['CHAV', 'UM MOLHO DE CHAVES'],
       V( ['PEGU'],
        P( ['CHAV', 'OK PEGUEI AS CHAVES!'] ) ),
       V( ['LARG'],
        T( ['CHAV', 'A CHAVE FICA LARGADA POR AI']  ) ),
       V( ['OLHE', 'XI! SAO DA MAMAE!'] ),
       V( ['MOSTR'],
        M( ['APAR', 'SUA MAE FICOU DE FORA.. VAMOS!'] ),
        N( ['PAI', 'NINGUEM SE INTERESSOU POR ELAS'] ) ) ) 
     )
 )


class TestAventura(unittest.TestCase):
  """
  Container is a tree of adventure sites.
  """
  def setUp(self):
    self.z = loaded_adventure

  def tearDown(self):
    self.z = None

  def test_adventureStart(self):
    """just the splash"""
    key = self.z.key
    value = self.z.contents
    self.assertEqual(
      key ,"zz"
      ,"Did not return the locus but "+'%s'%key)
    self.assertTrue(
      value.has_key('APAR') 
      ,"Did not return the container but "+'%s'%value)

  def test_adventureLocator(self):
    """if MAPA_MUNDI works"""
    loc=MAPA_MUNDI
    value = loc['APAR'].find('CHAV').value
    self.assertTrue(
      value.startswith('UM MOLHO') 
      ,"Did not return the container but "+'%s'%value)
    value = loc['APAR'].value
    self.assertTrue(
      value.startswith('VOCE ESTA') 
      ,"Did not return the container but "+'%s'%value)

  def test_locusShow(self):
    """if locus can show itself"""
    loc=MAPA_MUNDI
    value = loc['APAR'].perform([''],loc)
    value = loc['APAR'].show()
    value = self.z.perform([])
    self.assertTrue(
      value.endswith('UM MOLHO DE CHAVES') 
      ,"Did not return the container but "+'%s'%value)
    value = loc['APAR'].value

  def test_QueryforSituation(self):
    """if query and forSituation works"""
    value = self.z.forSituation()
    self.assertTrue(
      value.endswith('O que devo fazer agora?\n') 
      ,"Did not return the container but "+'%s'%value)

  def no_test_failVerb(self):
    """if verb fails gracefully"""
    loc=MAPA_MUNDI
    verbs = loc['APAR'].find('CHAV')
    value =     verbs.perform(['PEG','CHOV'])
    self.assertTrue(
      value.endswith('essa de PEG CHOV .') 
      ,"Did not return the verb value but "+'%s'%value)

  def test_manageInventary(self):
    """if can put and take from inventory"""
    loc=MAPA_MUNDI
    obj = loc['APAR'].find('CHAV')
    inventario.append(obj)
    #value =     verbs.perform('PEG','CHOV')
    value = inventario.show()
    value = self.z.perform(['inve'])
    self.assertTrue(
      value.endswith('UM MOLHO DE CHAVES') 
      ,"Did not return chave in inventory but "+'%s'%value)
    inventario.pop(obj)
    value = inventario.show()
    self.assertTrue(
      value.endswith('NADA AQUI') 
      ,"Did not return empty inventory but "+'%s'%value)
    value = self.z.perform(['PEGU','CHAV'])
    value = inventario.show()
    self.assertTrue(
      value.endswith('UM MOLHO DE CHAVES') 
      ,"Did not put chave in inventory but "+'%s'%value)
    value = self.z.perform(['LARG','CHAV'])
    self.assertTrue(
      value.startswith('A CHAVE FICA LARGADA POR AI') 
      ,"Did not remove chave from inventory but "+'%s'%value)
    value = inventario.show()
    self.assertTrue(
      value.endswith('NADA AQUI') 
      ,"Did not remove chave from inventory but "+'%s'%value)
    value = self.z.perform([''])
    self.assertTrue(
      value.endswith('UM MOLHO DE CHAVES') 
      ,"Did not put chave in inventory but "+'%s'%value)

  def test_performVerb(self):
    """if perform action works"""
    loc = self.z.goto('apartamento')
    verbs = loc.find('chav').contents['PEGU']
    value =     verbs.perform(['PEGU','CHAV'],self.z)
    self.assertTrue(
      value.startswith('OK PEGUEI') 
      ,"Did not return the verb value but "+'%s'%value)
    value =  loc.perform(['PEGU','CHOV'],self.z)
    self.assertTrue(
      value.startswith('Nao vejo necas de CHOV') 
      ,"Did not fail the verb for location value but said"+'%s'%value)
    value = loc.find('chav').perform(['largue','chaves'],self.z)
    self.assertTrue(
      value.startswith('A CHAVE FICA LARGADA') 
      ,"Did not return the verb value but "+'%s'%value)
    value = self.z.perform(['pegue','chaves'])
    self.assertTrue(
      value.startswith('OK PEGUEI') 
      ,"Did not return the verb for location value but "+'%s'%value)
    
  def test_InitialScreen(self):
        resposta = self.z.perform('olhe'.split(' '))
        self.assertTrue(
          resposta.startswith('VOCE ESTA EM SEU'),
        "Did not returned "+'%s'%resposta)
        

  
if __name__ == '__main__':
  unittest.main()
  #runner = unittest.TextTestRunner()
  #runner.run(getTestSuite())

