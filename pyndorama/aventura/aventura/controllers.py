import logging

import cherrypy
import aventura
import turbogears
from turbogears import controllers, expose, validate, redirect

#from aventura import json

log = logging.getLogger("aventura.controllers")

#pyndorama=aventura.load()

class Root(controllers.RootController):
    pyndorama = aventura.load()
    @expose(template="aventura.templates.principal")
    def index(self):
        import time
        log.debug("Happy TurboGears Controller Responding For Duty")
        #pyndorama=aventura.load()
        return dict(text=Root.pyndorama.perform(''),
            image=Root.pyndorama.getImage())
    
    @expose(template="aventura.templates.principal")
    def acao(self,query):
        #return dict(text=pyndorama.perform(''))
        return dict(text=Root.pyndorama.processaQuery(query),
            image=Root.pyndorama.getImage())
    
    
        