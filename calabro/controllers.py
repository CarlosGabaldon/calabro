from turbogears import controllers, expose, identity, flash, config
import cherrypy
from subcontrollers.site import SiteController
from cherrypy import request, response
from calabro.model import Sites
import siterouter


class Root(controllers.RootController):
    
    @expose()
    def default(self, site_name, *path, **params):
        return siterouter.route(site_name, *path, **params)
            
    @expose()
    def index(self, *args, **kw):
        raise controllers.redirect(config.get('calabro.default_site'))
       
        
        