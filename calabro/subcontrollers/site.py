from turbogears                     import controllers, expose, flash, identity
from datetime                       import datetime, timedelta
from cherrypy                       import request, response
from calabro.model                  import Posts
from calabro.model                  import Comments
from calabro.model                  import User
from calabro.widgets                import widgets
from calabro.model                  import Sites
from calabro.model                  import Tags
from calabro.model                  import Pages
from calabro.model                  import Group
from calabro.model                  import Themes
from calabro.model                  import Badges
from blog                           import BlogController

from calabro.helpers                import *

class SiteController(controllers.RootController):
    
    
    @expose(template="genshi:calabro.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise controllers.redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            site=get_current_site()
            forward_url= request.headers.get("Referer", "/%s" % (site.name))

        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        site=get_current_site()
        redirect_to_home()
        
        
    @expose(template="genshi:calabro.templates.new_site")
    def new_site(self):
        sites = Sites.find_all()
        site = Sites.get(1)
        return dict(sites=sites,
                    groups=Group.find_all(site=site),
                    themes=Themes.find_all())

  
    @expose(template="genshi:calabro.templates.edit_site")
    @identity.require(identity.in_group("admin"))
    def edit_site(self):
        site=get_current_site()
        return dict(site=site,
                    archive_posts=Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    themes=Themes.find_all(),
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)
    
    
    
    @expose()
    def create_site(self, name, title, subtitle, about_image, email, posts_per_page, url, theme, description,
                    user_name, email_address, display_name, password, groups):
        site=Sites(title=title,
                  name=name.replace(' ', '_'),
                  subtitle=subtitle,
                  about_image=about_image,
                  email=email,
                  posts_per_page=int(posts_per_page),
                  url=url,
                  theme=theme,
                  description=description)
                  
        user = User(user_name=user_name,
                    email_address=email_address, 
                    display_name=display_name, 
                    password=password)
        site.addUser(user)

        for group in groups:
            Group.find_by_id(id=group, site=site).addUser(user)


        redirect_to_site(site.name)


    @expose()
    @identity.require(identity.in_group("admin"))
    def update_site(self, name, title, subtitle, about_image, email, posts_per_page, url, theme, description):
        site=get_current_site()
        site.set( title=title,
                  name=name.replace(' ', '_'),
                  subtitle=subtitle,
                  about_image=about_image,
                  email=email,
                  posts_per_page=int(posts_per_page),
                  url=url,
                  theme=theme,
                  description=description)
        flash("Site Updated!")
        redirect_to_home()


    @expose(fragment=True)
    def create_badge(self, site_id, name, html):
        site=get_current_site()
        badges = list(site.badges)
        badge = Badges(site=site, name=name, html=html)
        badges.append(badge)
        rendered_widget = "<li>%s</li>" % widgets.badge_widget.render(badge=badge)
        return rendered_widget

        