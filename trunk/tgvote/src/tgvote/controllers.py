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
pleitos = []
cidadao = []
candidato = []
menu = [{'Eleicao':'index'
                ,'Eleitores':'mostra_eleitores'
                ,'Candidatos':'mostra_candidaturas'
                }]

def add_custom_stdvars(vars):
  omenu = lambda : [(menu[0][key],key) for key in menu[0].keys()]
  return vars.update({"main_menu": omenu})

def format_action(action):
  action = ('?' in action) and action[:action.index('?')] or action
  return ' '.join([word.capitalize() for word in action.split('_')])

turbogears.view.variable_providers.append(add_custom_stdvars)


class MostraListagem(widgets.DataGrid):
  def renderit(self,*args,**kwargs):
    return [item() for item in self.list]
  def display(self, value=None, **params):
    return super(MostraListagem,self).display(value,**params),self.list[0].display(value,**params)
  def monta(self,title,acao,conteudo):
    self.list=[widgets.Label(default=""),widgets.Label(default="")]
    x= widgets.TableForm("TableForm",fields=[],action=acao, submit_text=format_action(acao))
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
class CadastraCandidatura(widgets.WidgetsList):
#    pleito = widgets.SingleSelectField("pleito",options=[(-1, "NenhumPleito_")])
#    candidato = widgets.SingleSelectField("cidadao",options=[(-1, "NenhumEleitor_")])
    candidato = widgets.TextField(attrs={'size':2})
    pleito = widgets.TextField(attrs={'size':2})
    campanha = widgets.TextField(attrs={'size':80})
    def monta(self):
      return widgets.TableForm(fields=self,
                                 action="salva_candidato")
class CadastroDeCandidatura(widgets.WidgetsList):
    NumPleito = widgets.Label(default="Sample Label")
    pleito = widgets.Label(default="Sample Label")
    candidato = widgets.TextField(default="Sample Label")
    campanha = widgets.TextField(attrs={'size':80})
    def monta(self,opleito ='',ocidadao ='-1'):
      if int(opleito)>= 0:
        self[0] = widgets.Label(default="Pleito: "+str(opleito))
        self[1] = widgets.HiddenField(name="pleito",default=str(opleito))
        self[2]= widgets.SingleSelectField("cidadao", 
                   options=[(-1, "NenhumEleitor_")]
                   +[(indice, umcandidato["Eleitor_"]) for indice,umcandidato in enumerate(cidadao)],
                                   default=0)
      else:
        self[0] = widgets.Label(default="Cidadao: "+str(ocidadao))
        self[1] = widgets.SingleSelectField("pleito", 
                   options=[(-1, "NenhumPleito_")]
                   +[(num, umpleito["Descricao"]) for num,umpleito in enumerate(pleitos)],
                                   default=0)
        self[2] = widgets.HiddenField(name="cidadao",default=str(ocidadao))
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
      pl= pleitos or [{}]
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
    def mostra_candidaturas(self):
      titulo="Listagem das Candidaturas"
      log.debug(titulo)
      acao='cadastra_candidatura'
      rol= candidato or [{}]
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
      titulo='Pleito: '+pleitos[int(chave)]['Descricao']
      acao='adiciona_candidatura?cidadao=-1&pleito=%s'%chave
      #rol= candidato and candidato[int(chave)] or [{}]
      rol = [aopleito for aopleito in candidato if aopleito['Pleito_']== chave] or [{}]
      campos=Dados().fields(rol)
      return MostraListagem(fields=campos,default=rol).monta(titulo,acao,rol)
    @expose(template="tgvote.templates.main")
    def mostra_Cidadao(self,chave): #*args,**kwargs):
      log.debug("Cadastro de Candidaturas do Cidadao - chave: "+chave)
      titulo='Cidadao: '+ cidadao[int(chave)]['Eleitor_']
      acao='adiciona_candidatura?pleito=-1&cidadao=%s'%chave
      #rol= candidato and candidato[int(chave)] or [{}]
      rol = [doCidadao for doCidadao in candidato if doCidadao['Cidadao_']== chave] or [{}]
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
    def cadastra_candidatura(self):
      log.debug("candidatos: "+str([(n,c) for n,c in enumerate(cidadao)]))
      ''' '''
      opt_candidato = widgets.SingleSelectField("cidadao", 
                   options=[(-1, "NenhumEleitor_")]
                   +[(indice, candidate["Eleitor_"]) for indice,candidate in enumerate(cidadao)],
                                   default=0)
      ''' '''
      opt_pleito = widgets.SingleSelectField("pleito", 
                   options=[(-1, "NenhumPleito_")]
                   +[(num, opleito["Descricao"]) for num,opleito in enumerate(pleitos)],
                                   default=0)
      ''' '''
      frm =CadastraCandidatura()
      frm.candidato = opt_candidato
      frm[0] = opt_candidato
      frm[1] = opt_pleito
      return dict(
                    form=frm.monta()
                    ,use_case='Cadastro De Candidatura')
    @expose(template="tgvote.templates.main")
    def adiciona_candidatura(self,cidadao,pleito):
      tb = candidato
      return dict(
                    form=CadastroDeCandidatura().monta(pleito,cidadao)
                     ,use_case='Cadastro De Candidatura')

    @expose(template="tgvote.templates.main")
    def salva_candidato(self,cidadao,campanha,pleito):
#    def salva_candidato(self, **data):
      tb = candidato
      if (int(pleito) >= 0) and (int(cidadao) >= 0) :
        tb += [{'Pleito_':pleito,'Campanha':campanha,'Cidadao_':cidadao}]
      tb = tb or [{}]
      #candidatosAoPleito= tb and tb.get(pleito) or [tb.__setitem__(pleito,[])] and tb[pleito]
      #candidatosAoPleito += [{'Candidato':Candidato,'Campanha':Campanha}]
      #log.debug("Candidato: " + str(data))
      log.debug("Candidato: cidadao %s,campanha %s,opleito %s" %(cidadao,campanha,pleito))
      return dict(
                    form=Dados().monta(tb)
                    ,next_text='Cadastra Pleito'
                    ,next_url='index'
                    ,use_case='Listagem dos Candidatos')
    @expose(template="tgvote.templates.main")
    def salva_pleito(self,descricao,data_inicio,data_fim):
      pl = pleitos
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
