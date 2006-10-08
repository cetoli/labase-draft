import logging

import cherrypy

import turbogears
from turbogears import controllers, expose, validate, redirect

from tgvote import json
from turbogears import widgets, validators,url
from urllib import urlencode
from elementtree import ElementTree as ET
pleito = []
cidadao = []
candidato = []

class CadastroDePleito(widgets.WidgetsList):
    descricao = widgets.TextField(validator=validators.NotEmpty(),attrs={'size':80})
    data_inicio = widgets.CalendarDatePicker('data_inicio')
    data_fim = widgets.CalendarDatePicker('data_fim')
class CadastroDeCandidatura(widgets.WidgetsList):
    NumPleito = widgets.Label(default="Sample Label")
    Pleito = widgets.Label(default="Sample Label")
    Candidato = widgets.TextField(default="Sample Label")
    Campanha = widgets.TextField(attrs={'size':80})
    def monta(self,pleito):
      self[0] = widgets.Label(default="Pleito: "+str(pleito))
      self[1] = widgets.HiddenField(name="Pleito",default=str(pleito))
      self[2]= widgets.SingleSelectField("Cidadao", 
                   options=[(-1, "NenhumEleitor_")]
                   +[(indice, candidato["Eleitor_"]) for indice,candidato in enumerate(cidadao)],
                                   default=0)
      return widgets.TableForm(fields=self,
                                 action="http://localhost:8080/adiciona_candidato")
class CadastroDeEleitor(widgets.WidgetsList):
    nome = widgets.TextField(validator=validators.NotEmpty(),attrs={'size':80})
    senha = widgets.TextField(validator=validators.NotEmpty(),attrs={'size':20})
    def monta(self):
      return widgets.TableForm(fields=CadastroDeEleitor(),
                                 action="salva_eleitor")

cadastra_pleito_form = widgets.TableForm(fields=CadastroDePleito(),
                                 action="salva_pleito")

class Dados:
  def monta(self,dados):
    return widgets.DataGrid(
        fields=self.formalinha(dados[0]),
        default= dados)
        #default=[linha.values() for linha in dados])
  def formalinha(self,linha):
    return [(label.strip('_'), self.formacoluna(label)) for label in linha.keys()]
  def formacoluna(self,coluna):
    return eval('lambda linha,self=self:self.formalink(linha,"%s")'%coluna)
    #return eval('lambda cadalinha:cadalinha["%s"]'%coluna)
  def formalink(self,entidade,chave):
    valor = entidade[chave]
    if chave.endswith('_'):
      #href = "<a href='/edita_%s?%s'>%s</a>"
      href = "/edita_%s?chave=%s"
      #href = href%(chave[:-1],urlencode({'chave':valor}))
      href = href%(chave[:-1],valor)
      return self.makeLink(url=href,title=valor)
    return valor

  def makeLink(self,url,title):
     link = ET.Element('a', href=url)
     link.text = title
     return link

    

log = logging.getLogger("tgvote.controllers")

class Root(controllers.RootController):
    @expose(template="tgvote.templates.main")
    def index(self):
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(
                    form=cadastra_pleito_form
                    ,next_text='Cadastra Eleitor'
                    ,next_url='cadastra_eleitor'
                    ,use_case='Cadastro de Pleito')
    @expose(template="tgvote.templates.main")
    def edita_Pleito(self,chave): #*args,**kwargs):
        log.debug("chave: "+chave)
#        chave=args[0]
        return dict(
                    form=CadastroDeCandidatura().monta(chave)
                    ,next_text='Executa Pleito'
                    ,next_url='executa_pleito'
                    ,use_case='Cadastro de Candidaturas')
    @expose(template="tgvote.templates.main")
    def adiciona_candidato(self,Candidato,Campanha,Pleito):
      tb = candidato
      pleito = int(Pleito)
      tb[pleito] += [{'Candidato':Candidato,'Campanha':Campanha}]
      log.debug("Candidato: %s,Campanha: %s,Pleito: %s"%(Candidato,Campanha,Pleito))
      return dict(
                    form=Dados().monta(tb)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Listagem dos Pleitos')
    @expose(template="tgvote.templates.main")
    def salva_pleito(self,descricao,data_inicio,data_fim):
      pl = pleito
      pl += [{'Pleito_':""+str(len(pl)),'Descricao':descricao,'Inicio':data_inicio, 'Fim':data_fim}]
      log.debug("Happy TurboGears Controller Responding For Duty")
      return dict(
                    form=Dados().monta(pl)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Listagem dos Pleitos')
    @expose(template="tgvote.templates.main")
    def cadastra_eleitor(self):
        log.debug("Cadastra Eleitor")
        return dict(
                    form=CadastroDeEleitor().monta()
                    ,next_text='Escolha de Pleito'
                    ,next_url='cadastra_eleitor'
                    ,use_case='Cadastro de Eleitor')
    @expose(template="tgvote.templates.main")
    def salva_eleitor(self,nome,senha):
      lista = cidadao
      lista += [{'Eleitor_':nome,'Senha':senha}]
      log.debug("Salva Eleitor: " + str(lista))
      return dict(
                    form=Dados().monta(lista)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Listagem dos Eleitores')
