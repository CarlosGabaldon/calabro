from turbogears                                 import controllers, expose, identity, flash
from cherrypy                                   import request, response
from calabro.model                              import Sites
import cherrypy


def get_current_site():
    path = cherrypy.request.path.split('/')
    site_name = path[1]
    return Sites.get_current(name=site_name)
    

def redirect_to_home():
    site = get_current_site()
    raise controllers.redirect('/%s' % (site.name))
    


def redirect_to_site(site_name):
    raise controllers.redirect('../../%s' % (site_name))
    
    
def redirect_to_users():
    site = get_current_site()
    raise controllers.redirect('/%s/users' % (site.name))
    
     
def remove_special_char(string):
    string = string.strip().replace(' ', '_')
    string = string.replace("'", "")
    string = string.replace("$", "")
    string = string.replace("&", "")
    string = string.replace("<", "")
    string = string.replace(">", "")
    string = string.replace("*", "")
    string = string.replace("@", "")
    string = string.replace(".", "")
    string = string.replace(":", "")
    string = string.replace("|", "")
    string = string.replace("~", "")
    string = string.replace("`", "")
    string = string.replace("(", "")
    string = string.replace(")", "")
    string = string.replace("%", "")
    string = string.replace("#", "")
    string = string.replace("^", "")
    string = string.replace("?", "")
    string = string.replace("/", "")
    string = string.replace("{", "")
    string = string.replace("}", "")
    string = string.replace(",", "")
    string = string.replace(";", "")
    string = string.replace("!", "")
    string = string.replace("+", "")
    string = string.replace("=", "")
    string = string.replace("-", "_")
    return string
