import logging

import cherrypy

import turbogears
from turbogears import controllers, expose, validate, redirect

from tgvote import json
from turbogears import widgets, validators


class CadastroDePleito(widgets.WidgetsList):
    descricao = widgets.TextField(validator=validators.NotEmpty(),attrs={'size':80})
    data_inicio = widgets.CalendarDatePicker('data_inicio')
    data_fim = widgets.CalendarDatePicker('data_fim')

cadastra_pleito_form = widgets.TableForm(fields=CadastroDePleito(),
                                 action="cadastra_pleito")


log = logging.getLogger("tgvote.controllers")

class Root(controllers.RootController):
    @expose(template="tgvote.templates.main")
    def index(self):
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(
                    form=cadastra_pleito_form
                    ,next_text='Cadastra Eleitor'
                    ,use_case='Cadastro de Pleito')
    @expose(template="tgvote.templates.main")
    def cadastra_pleito(self,descricao,data_inicio,data_fim):
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(
                    form=cadastra_pleito_form
                    ,next_text='Cadastra Eleitor'
                    ,use_case='Cadastro de Pleito')
