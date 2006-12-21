import logging

import cherrypy
import aventura
import turbogears
from turbogears import controllers, expose, validate, redirect, widgets
from turbogears.widgets.base import JSLink , CoreWD
from turbogears.widgets.forms import SingleSelectField

#from aventura import json

log = logging.getLogger("aventura.controllers")

#pyndorama=aventura.load()

def makeForm(campos):
  adventure =  SingleSelectField("adventure",options= campos[0])
  return widgets.TableForm(
         fields=[adventure]
         ,submit_text="Selecionar Aventura",action="iniciar"
     )
     
class Root(controllers.RootController):
    #pyndorama = None
    @expose(template="aventura.templates.principal")
    def iniciar(self, adventure):
        # Session variable initialization (or recall if exists)
        cherrypy.session['pindorama'] = aventura.load(adventure) 
     
        # Variable assignment
        pyndorama= cherrypy.session['pindorama']
        log.debug("Happy TurboGears Controller Responding For Duty")
        #pyndorama=aventura.load()
        return dict(text=pyndorama.perform(''),
            image=pyndorama.getImage())
            
    @expose(template="aventura.templates.menu")
    def index(self):
        aventuras = [('ave.yaml','A gralha e o jarro'),('labirinto.yaml','Labirinto')]
        enviair_form = makeForm([aventuras])
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(form=enviair_form)
    
    @expose(template="aventura.templates.principal")
    def acao(self,query):
        #return dict(text=pyndorama.perform(''))
        pyndorama= cherrypy.session['pindorama']
        return dict(text=pyndorama.processaQuery(query),
            image=pyndorama.getImage())
            
            
    
    
        