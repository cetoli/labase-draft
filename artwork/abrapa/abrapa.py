#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
Abrapa: Logo em 3d Para a Abrapa
===================================================

Copyright (c) 2008
Carlo E.T. Oliveira et all 
(see U{http://labase.nce.ufrj.br/info/equipe.html})

Licensed under the GNU GPL v3 - http://www.gnu.org/licenses/gpl.html
This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""
__author__  = "Carlo E. T. Oliveira (carlotolla-labase@yahoo.com.br) $Author: carlo $"
__version__ = "1.0 $Revision$"[10:-1]
__date__    = "2008/05/14 $Date$"

from visual import *
gold=(255,215,0)
ht=8
class prism:
    "Esse eu fiz para vocês: um prisma triangular que representa um telhado"
    def __init__(self, fram=frame(), size=10., c= color.white):
        '''ontogênese: assim que é criado, o bloco se desenha'''
        self.estrutura=frame(frame=fram)#faz nascer um novo frame e apelida de estrutura
        self.e= self.estrutura
        self.size=size
        self.cor_dos_detalhes= c #estabelece a cor dos detalhes
        self.desenha_as_partes_do_bloco()#invoca operações para desenhar o bloco
    def desenha_as_partes_do_bloco(self):
        '''cria um objeto convexo que passa por seis pontos no espaço'''
        s=self.size/2
        fr,ns=(self.estrutura,(-s,s))
        convex(pos =([
                (x,ht*z/self.size,y)for x in ns for y in ns for z in ns if x-y or x-s
            ]),color=self.cor_dos_detalhes,frame=self.estrutura)
class rhomb(prism):
    def desenha_as_partes_do_bloco(self):
        '''cria um objeto convexo que passa por seis pontos no espaço'''
        s=self.size/2
        fr,ns=(self.estrutura,(-s,s))
        convex(pos =([
                (x,ht*z/self.size,y+x)for x in ns for y in ns for z in ns 
            ]),color=self.cor_dos_detalhes,frame=self.estrutura)
    
tf = frame()
box (frame= tf, pos=(70,0,0),length=10,width=150,height=10, color=color.blue)
box (frame= tf, pos=(-70,0,0),length=10,width=150,height=10, color=color.blue)
box (frame= tf, pos=(0,0,-70),length=150,width=10,height=10, color=color.blue)
box (frame= tf, pos=(0,0,70),length=150,width=10,height=10, color=color.blue)
box (frame= tf, pos=(0,-4,0),length=140,width=140,height=1, color=gold)
box (frame= tf, pos=(0,0,-30),length=96,width=5,height=10, color=color.blue)
box (frame= tf, pos=(0,0,20),length=96,width=5,height=10, color=color.blue)
box (frame= tf, pos=(0,10,-5),length=32,width=50,height=5, color=color.blue)
box (frame= tf, pos=(0,10,-27.5),length=32,width=5,height=16, color=color.white)
box (frame= tf, pos=(0,10,17.5),length=32,width=5,height=16, color=color.white)
'''boneco do meio'''
fr=frame(frame= tf)
prism(fram=fr ).e.pos=(5.5,14,-5)
braco=prism(fram=fr)
braco.e.pos=(-5.5,14,-5)
braco.e.rotate(angle=-pi/2, axis=(0,1,0))
r=rhomb(fram=fr, size=5)
r.e.pos=(1.5,14,5)
perna=prism(fram=fr, size=10./sqrt(2))
perna.e.pos=(-5,14,4)
perna.e.rotate(angle=-pi, axis=(0,1,0))
pet=prism(fram=fr, size=5)
pet.e.pos=(-10,14,7)
pef=prism(fram=fr, size=5)
pef.e.pos=(3,14,10)
pef.e.rotate(angle=pi/2, axis=(0,1,0))
box (frame=fr, pos=(0,14,-15),length=5,width=5,height=ht, color=color.white).rotate(angle=-pi/8, axis=(0,1,0))
fr.pos=(0,0,-2)
'''boneco esquerdo'''
b=color.blue
fr=frame(frame= tf)
tronco=prism(c=b, fram=fr )
tronco.e.pos=(1.5,14,0)
tronco.e.rotate(angle=-pi, axis=(0,1,0))
coxa=prism(c=b, fram=fr)
coxa.e.pos=(2.5,14,-13)
coxa.e.rotate(angle=pi/2, axis=(0,1,0))
r=rhomb(c=b, fram=fr, size=5)
r.e.pos=(1.5,14,8)
r.e.rotate(angle=-pi/2, axis=(0,1,0))
perna=prism(c=b, fram=fr, size=10./sqrt(2))
perna.e.pos=(3,14,-3)
#perna.e.rotate(angle=pi/2, axis=(0,1,0))
pet=prism(c=b, fram=fr, size=5)
pet.e.pos=(-3.5,14,-17)
pet.e.rotate(angle=pi/4, axis=(0,1,0))
pef=prism(c=b, fram=fr, size=5)
pef.e.pos=(3,14,10)
pef.e.rotate(angle=pi, axis=(0,1,0))
box (frame=fr, pos=(-4.5,14,1),length=5,width=5,height=ht, color=b).rotate(angle=-pi/4, axis=(0,1,0))
fr.pos=(-32,-14,-2)

'''boneco direito'''
b=color.blue
fr=frame(frame= tf)
tronco=prism(c=b, fram=fr )
tronco.e.pos=(10,14,0)
tronco.e.rotate(angle=pi/4, axis=(0,1,0))
coxa=prism(c=b, fram=fr)
coxa.e.pos=(2.5,14,8)
coxa.e.rotate(angle=-pi/4, axis=(0,1,0))
r=rhomb(c=b, fram=fr, size=5)
r.e.pos=(15,14,-10)
r.e.rotate(angle=-pi/2, axis=(0,1,0))
ombro=prism(c=b, fram=fr, size=10./sqrt(2))
ombro.e.pos=(5,14,-8)
ombro.e.rotate(angle=3*pi/4, axis=(0,1,0))
pet=prism(c=b, fram=fr, size=5)
pet.e.pos=(-3.5,14,12)
pet.e.rotate(angle=7*pi/8, axis=(0,1,0))
pef=prism(c=b, fram=fr, size=5)
pef.e.pos=(12,14,14)
pef.e.rotate(angle=3*pi/8, axis=(0,1,0))
box (frame=fr, pos=(2.5,14,-13),length=5,width=5,height=ht, color=b).rotate(angle=-5*pi/8, axis=(0,1,0))
fr.pos=(30,-14,-4)
from visual.text import *
#tf=frame()
tf.rotate(angle=pi/2, axis=(1,0,0))
tht,twd=6,5.5
text(pos=(0,40,0), axis=(1,0,0), string='ABRAPA', color=b, depth=0.4, width=16,height=18, justify='center')
text(pos=(0,-35,0), axis=(1,0,0), string='ASSSOCIACAO BRASILEIRA', color=b, depth=0.4, width=twd,height=tht, justify='center')
text(pos=(0,-45,0), axis=(1,0,0), string='DE PROBLEMAS', color=b, depth=0.4, width=twd,height=tht, justify='center')
text(pos=(0,-55,0), axis=(1,0,0), string='DE APRENDIZAGEM', color=b, depth=0.4, width=twd,height=tht, justify='center')
