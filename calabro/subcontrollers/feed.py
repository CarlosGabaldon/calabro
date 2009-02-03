from turbogears.feed import FeedController as FC
from turbogears import controllers, expose
from datetime import datetime, timedelta
from calabro.model import Posts
from calabro.model import Comments
from calabro.model import User
from calabro.widgets import widgets
from calabro.model import Sites
from textile import textile
from cgi import escape
from calabro.helpers import *

class FeedController(FC):
    
    
    def get_feed_data(self):
        site=get_current_site()
        posts = Posts.find_all(site=site)
        entries = []
        for post in posts:
            entry = {}
            entry["updated"]   = post.created
            entry["title"]     = post.title
            entry["link"]      = "%s/%s/blog/post/%s" % (site.url, site.name, post.permalink)
            entry["published"] = post.created
            entry["author"]    = post.user.display_name
            entry["summary"]   = textile(escape(post.text).encode('utf-8'), encoding='utf-8', output='utf-8') #post.text[:50]
            entries.append(entry)
        
        return dict(title=site.title,
                    link=site.url,
                    author= {"name": site.title, "email": site.email},
                    id=site.url,
                    subtitle=site.subtitle,
                    entries=entries)