from turbogears import controllers, expose, flash, identity, config
from datetime import datetime, timedelta
from sqlobject  import SQLObjectNotFound
from calabro.model  import Posts
from calabro.model  import Comments
from calabro.model  import User
from calabro.widgets import widgets
from calabro.model  import Sites
from calabro.model  import Tags
from calabro.model  import Pages
from textile        import textile
from calabro.helpers import *

class ErrorController(controllers.RootController):
    
    
    @expose(template="genshi:calabro.templates.error")
    def index(self):
        site=get_current_site()
        home_url=config.get('calabro.default_site')
        
        return dict(home_url=home_url,
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

        