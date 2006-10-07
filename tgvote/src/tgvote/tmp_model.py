from sqlobject import *
from datetime import datetime
from turbogears.database import PackageHub
from turbogears.identity.soprovider import TG_User, TG_Group, TG_Permission

hub = PackageHub("tgvote")
__connection__ = hub

class Eleicao(SQLObject):
    pleitos = MultipleJoin("Pleito",joinColumn='eleicao_id')
    cidadaos = MultipleJoin("Cidadao",joinColumn='registrado_id')


class Cidadao(SQLObject):
    nome = StringCol(length=100,unique=True,notNone=True)
    registrado = ForeignKey("Eleicao")
    voto = MultipleJoin("Voto",joinColumn='eleitor_id')
    candidaturas = MultipleJoin("Candidatura",joinColumn='candidato_id')
    comparecimentos = MultipleJoin("Comparecimento",joinColumn='cidadao_id')
    senha = StringCol(length=20)


class Pleito(SQLObject):
    descricao = StringCol(varchar=True)
    data_inicio = DateCol()
    data_fim = DateCol()
    eleicao = ForeignKey("Eleicao")
    votos = MultipleJoin("Voto",joinColumn='pleito_id')
    candidaturas = MultipleJoin("Candidatura",joinColumn='pleito_id')
    comparecimentos = MultipleJoin("Comparecimento",joinColumn='pleito_id')


class Voto(SQLObject):
    pleito = ForeignKey("Pleito")
    eleitor = ForeignKey("Cidadao")
    candidatura = ForeignKey("Candidatura")


class Candidatura(SQLObject):
    pleito = ForeignKey("Pleito")
    votos = MultipleJoin("Voto",joinColumn='candidatura_id')
    campanha = StringCol(length=150)
    candidato = ForeignKey("Cidadao")


class Comparecimento(SQLObject):
    cidadao = ForeignKey("Cidadao")
    pleito = ForeignKey("Pleito")



