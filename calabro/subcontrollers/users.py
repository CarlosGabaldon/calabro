from turbogears                     import controllers, expose, flash, identity
from datetime                       import datetime, timedelta
from calabro.model                  import Posts
from calabro.model                  import Comments
from calabro.model                  import User
from calabro.widgets                import widgets
from calabro.model                  import Sites
from calabro.model                  import Tags
from calabro.model                  import Pages
from calabro.model                  import Group
from blog                           import BlogController
from cherrypy                       import request, response
from calabro.helpers                import *

class UsersController(controllers.RootController):
    
    @expose(template="genshi:calabro.templates.users")
    def index(self):
        """docstring for index"""
        site=get_current_site()
        users = User.find_all(site=site)
        return dict(site=site,
                    archive_posts=Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    users=users,
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)
    
    @expose(template="genshi:calabro.templates.new_user")
    @identity.require(identity.in_group("admin"))
    def new(self):
        """docstring for new"""
        site=get_current_site()
        return dict(site=site,
                    archive_posts=Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    groups=Group.find_all(site=site),
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)
    
    @expose()
    @identity.require(identity.in_group("admin"))
    def create(self, user_name, email_address, display_name, password, groups):
        """docstring for create"""
        site=get_current_site()
        user = User(user_name=user_name,
                    email_address=email_address, 
                    display_name=display_name, 
                    password=password)
        site.addUser(user)
        
        for group in groups:
            Group.find_by_id(id=group, site=site).addUser(user)
        
        redirect_to_users()
        
    @expose(template="genshi:calabro.templates.edit_user")
    @identity.require(identity.in_group("admin"))    
    def edit(self):
        """docstring for edit"""
        pass
    
    @expose()
    @identity.require(identity.in_group("admin"))    
    def update(self):
        """docstring for update"""
        pass
    
    @expose()   
    def destroy(self):
        """docstring for destroy"""
        pass
        
    
