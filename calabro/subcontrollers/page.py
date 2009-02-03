from turbogears                     import controllers, expose, flash, identity
from datetime                       import datetime, timedelta
from calabro.model                  import Posts
from calabro.model                  import Comments
from calabro.model                  import User
from calabro.widgets                import widgets
from calabro.model                  import Sites
from calabro.model                  import Tags
from calabro.model                  import Pages
from calabro.helpers                import *

class PageController(controllers.RootController):
    @expose(template="genshi:calabro.templates.page")
    def default(self, name, *args, **kwargs):
        site=get_current_site()
        page = Pages.find_by_name(name=name,
                                  site=site)
        if page == None:
            raise controllers.redirect('/new_page?name=' + name)

        return dict(page=page,
                    site=site,
                    archive_posts= Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)
    
    
    @expose(template="genshi:calabro.templates.new_page")
    @identity.require(identity.in_group("admin"))
    def new_page(self, name=""):
        site=get_current_site()
        return dict(name=name,
                   site=site,
                   archive_posts= Posts.find_archive_count(site=site),
                   archives_widget=widgets.archives_widget,
                   tags_widget=widgets.tags_widget,
                   pages_widget=widgets.pages_widget,
                   pages=Pages.find_all(site=site),
                   tags=Tags.find_all(site=site),
                   admin_widget=widgets.admin_widget,
                   badge_widget=widgets.badge_widget,
                   recent_comments=Comments.find_recent(),
                   recent_comments_widget=widgets.recent_comments_widget)


    @expose(template="genshi:calabro.templates.edit_page")
    @identity.require(identity.in_group("admin"))
    def edit_page(self, name):
        site=get_current_site()
        page = Pages.find_by_name(name=name, 
                                  site=site)
        
        if page == None:
            raise controllers.redirect('/%s/new_page?name=%s' %(site.name, name))
           
        return dict(page=page,
                   site=site,
                   archive_posts= Posts.find_archive_count(site=site),
                   archives_widget=widgets.archives_widget,
                   tags_widget=widgets.tags_widget,
                   pages_widget=widgets.pages_widget,
                   pages=Pages.find_all(site=site),
                   tags=Tags.find_all(site=site),
                   admin_widget=widgets.admin_widget,
                   badge_widget=widgets.badge_widget,
                   recent_comments=Comments.find_recent(),
                   recent_comments_widget=widgets.recent_comments_widget)


    
    
    @expose()
    @identity.require(identity.in_group("admin"))
    def create_page(self, name, title, body):
        page_name = name.replace(' ', '_')
        site = get_current_site()
        page = Pages(name=page_name,
                     title=title, 
                     body=body,
                     site=site)
        raise controllers.redirect(page_name)
        


    @expose()
    @identity.require(identity.in_group("admin"))
    def update_page(self, page_id, name, title, body):
        page_name = name.replace(' ', '_')
        page = Pages.get(page_id)
        page.set(name=page_name,
                 title=title,
                 body=body)
        raise controllers.redirect(page_name)        
    
       
        
        