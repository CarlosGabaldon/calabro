from turbogears                     import testutil
from calabro.controllers            import Root
import cherrypy
from calabro.model                  import Posts


cherrypy.root = Root()

def test_blog_index():
    "the index method should return a string called now"
    testutil.createRequest("/py_talk")
    assert "<title>Python Talk - Discussing Python</title>" in cherrypy.response.body[0]


