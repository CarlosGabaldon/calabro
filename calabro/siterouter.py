
from subcontrollers.blog import BlogController
from subcontrollers.page import PageController
from subcontrollers.feed import FeedController
from subcontrollers.site import SiteController
from subcontrollers.users import UsersController
from subcontrollers.error import ErrorController

def route(site_name, *path, **params):
    """
       The front controller for routing all requests through a site name.
       Parameters:
           site_name => the identifier of the site, which is used to lookup the site configuration details.
           path => tuple that contains the Controller, Action, and any additional path values.
           params => dict that contains any key/value querystring or form field values.
       Conventions:
           controller name in path = is the class with capitalized first letter with the word Controller appended to end:
           /blog/ = BlogController()
           /users/ = UsersController()
           ect..
     """ 
    if not path:
        # If there are no path elements
        # then default to calling
        # the BlogController
        return get_controller('blog').index()
    elif len(path) == 1:
        # If only the Controller is in the path
        # then we call the index method of 
        # that controller.
        try:
            return get_controller(path[0]).index()
        except Exception:
            return get_controller('error').index()
    else:
        # The first element in the path is the Controller name
        # and the second element is the method or action to 
        # invoke on that controller.
        try:
            action = getattr(get_controller(name=path[0]), path[1])
        except AttributeError:
            return get_controller(path[0]).default(path[1])
        # Pass any remaining elements in the path 
        # and any params to the controller method
        # use * and ** to expand the values out
        # into individual parameters to the method.
        return action(*path[2:], **params)


def get_controller(name):

    controller_name = '%sController()' % name.capitalize()
    return eval(controller_name)
            
    




def main():
	pass


if __name__ == '__main__':
	main()

