import logging

import cherrypy

import turbogears
from turbogears import controllers, expose, validate, redirect
from turbogears.widgets import Widget, CSSLink, static

from tgvote import json
from turbogears import widgets, validators,url
from urllib import urlencode
from elementtree import ElementTree as ET
from turbogears.widgets.datagrid import DataGrid as DG
pleito = []
cidadao = []
candidato = {}
menu = [{'Eleicao':'index'
                ,'Pleitos':'mostra_pleitos'
                ,'Eleitores':'mostra_eleitores'
                }]

def add_custom_stdvars(vars):
  omenu = lambda : [(menu[0][key],key) for key in menu[0].keys()]
  return vars.update({"main_menu": omenu})

turbogears.view.variable_providers.append(add_custom_stdvars)


class MostraListagem(widgets.DataGrid):
#  css=[widgets.CSSLink(static, "grid.css")]
#  LocalMenu=widgets.Label(default="Vazio")
#  Displayer=widgets.Label(default="")
#  Displayer1=widgets.Label(default="")
  def renderit(self,*args,**kwargs):
    return [item() for item in self.list]
  def display(self, value=None, **params):
    return super(MostraListagem,self).display(value,**params),self.list[0].display(value,**params)
  def monta(self,title,acao,conteudo):
    self.list=[widgets.Label(default=""),widgets.Label(default="")]
    x= widgets.TableForm("TableForm",fields=[],action=acao, submit_text=acao)
    self.list[0] = x
    if conteudo: 
      self.list[1] = self #Dados().monta(conteudo)
      self.list[0] = x
    if not conteudo: conteudo = [{}]
    return dict(form= self #Dados().monta(conteudo)#self #.renderit
                ,use_case=title)

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
                                 action="/salva_candidato")
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
    legenda = dados and dados[0] or {}
    return widgets.DataGrid(
        fields=self.formalinha(legenda),
        default= dados)
        #default=[linha.values() for linha in dados])
  def fields(self,dados):
    legenda = dados and dados[0] or {}
    return self.formalinha(legenda)
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
      href = "/mostra_%s?chave=%s"
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
      titulo="Tela Principal"
      log.debug("Tela Principal")
      acao='adiciona_pleito'
      pl= pleito or [{}]
      campos=Dados().fields(pl)
      return MostraListagem(fields=campos,default=pl).monta(titulo,acao,pl)
    @expose(template="tgvote.templates.main")
    def mostra_eleitores(self):
      titulo="Listagem dos Eleitores"
      log.debug(titulo)
      acao='adiciona_eleitor'
      rol= cidadao or [{}]
      campos=Dados().fields(rol)
      return MostraListagem(fields=campos,default=rol).monta(titulo,acao,rol)
    @expose(template="tgvote.templates.main")
    def adiciona_pleito(self):
        log.debug("Adiciona Pleito")
        return dict(
                    form=cadastra_pleito_form
                    ,use_case='Cadastro de Pleito')
    @expose(template="tgvote.templates.main")
    def mostra_Pleito(self,chave): #*args,**kwargs):
      log.debug("Cadastro de Candidaturas - chave: "+chave)
      titulo='Cadastro de Candidaturas'
      acao='adiciona_candidato?chave='+chave
      rol= candidato and candidato[int(chave)] or [{}]
      campos=Dados().fields(rol)
      return MostraListagem(fields=campos,default=rol).monta(titulo,acao,rol)
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
    def main_menu(self):
      menu = [{'Eleicao_':'mostra_eleicao'
                ,'Pleitos_':'mostra_pleitos'
                ,'Eleitores_':'mostra_eleitores'
                }]
      return dict(
                    form=Dados().monta(menu)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Listagem dos Pleitos')
    @expose(template="tgvote.templates.main")
    def adiciona_candidato(self,chave):
      tb = candidato
      pleito = int(chave)
#      candidatosAoPleito= tb and tb.get(pleito) or [tb.__setitem__(pleito,[])] and tb[pleito]
      return dict(
                    form=CadastroDeCandidatura().monta(chave)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Cadastro De Candidatura ao Pleito'+chave)
    @expose(template="tgvote.templates.main")
    def salva_candidato(self,Candidato,Campanha,Pleito):
      tb = candidato
      pleito = int(chave)
      candidatosAoPleito= tb and tb.get(pleito) or [tb.__setitem__(pleito,[])] and tb[pleito]
      candidatosAoPleito += [{'Candidato':Candidato,'Campanha':Campanha}]
      log.debug("Candidato: %s,Campanha: %s,Pleito: %s"%(Candidato,Campanha,Pleito))
      return dict(
                    form=Dados().monta(tb)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Listagem dos Candidatos ao Pleito'+chave)
    @expose(template="tgvote.templates.main")
    def salva_pleito(self,descricao,data_inicio,data_fim):
      pl = pleito
      pl += [{'Pleito_':""+str(len(pl)),'Descricao':descricao,'Inicio':data_inicio, 'Fim':data_fim}]
      log.debug("Salva Pleito:" + str(pl))
      return dict(
                    form=Dados().monta(pl)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Listagem dos Pleitos')
    @expose(template="tgvote.templates.main")
    def adiciona_eleitor(self):
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
