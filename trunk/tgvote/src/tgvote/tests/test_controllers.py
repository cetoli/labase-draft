from turbogears import testutil
from tgvote.controllers import Root
import cherrypy

cherrypy.root = Root()

def test_method():
    "the index method should return a string called now"
    import types
    result = testutil.call(cherrypy.root.index)
    assert type(result["use_case"]) == types.StringType

def test_indextitle():
    "The mainpage should have the right title"
    testutil.createRequest("/")
    assert "<TITLE>Cadastro de Pleito</TITLE>" in cherrypy.response.body[0]
def test_mainmenu():
    "The mainmenu should be a data grid with links"
    testutil.createRequest("/main_menu")
    assert "mostra_eleicao" in cherrypy.response.body[0]
