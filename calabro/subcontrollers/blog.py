from turbogears import controllers, expose, flash, identity
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

class BlogController(controllers.RootController):
    
    
    @expose(template="genshi:calabro.templates.blog")
    def index(self):
        site=get_current_site()
        posts = Posts.find(site=site, top=site.posts_per_page)
        
        return dict(posts=posts,
                    site=site,
                    archive_posts= Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    posts_widget=widgets.posts_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)

    @expose(template='genshi:calabro.templates.blog')
    def archives(self, year, month):
        archives = '/'.join((year, month))
        site=get_current_site()
        posts = Posts.find_all_archived(archives=archives, site=site)
        return dict(posts=posts,
                    site=site,
                    archive_posts=Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    posts_widget=widgets.posts_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)
                    
    @expose(template='genshi:calabro.templates.archives')
    def archived(self):
        site=get_current_site()
        return dict(site=site,
                    archive_posts=Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    posts_widget=widgets.posts_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)
                                    
    @expose(template='genshi:calabro.templates.blog')
    def tags(self, name):
        site=get_current_site()
        tag = Tags.find_by(name=name, site=site)
        if tag == None:
            redirect_to_home()
            
        posts = Posts.find_by_tag(tag=tag, site=site)
        return dict(posts=posts,
                    site=site,
                    archive_posts=Posts.find_archive_count(site=site),
                    archives_widget=widgets.archives_widget,
                    tags_widget=widgets.tags_widget,
                    posts_widget=widgets.posts_widget,
                    pages_widget=widgets.pages_widget,
                    pages=Pages.find_all(site=site),
                    tags=Tags.find_all(site=site),
                    admin_widget=widgets.admin_widget,
                    badge_widget=widgets.badge_widget,
                    recent_comments=Comments.find_recent(),
                    recent_comments_widget=widgets.recent_comments_widget)   

    @expose(fragment=True)
    def search(self, query, *args, **kv):
        site=get_current_site()
        posts = Posts.find_by_query(query=query, site=site)
        return widgets.posts_widget.render(posts=posts, site=site)       

    @expose(template='genshi:calabro.templates.post')
    def post(self, year, month, day, title):
        permalink = '/'.join((year, month, day, title))
        site=get_current_site()
        try:
            post = Posts.find_by_permalink(permalink=permalink, site=site)
        except SQLObjectNotFound:
                flash("Sorry, post could not be found!")
                raise controllers.redirect('/')
                
        return dict(post=post,
                   site=site,
                   comment_widget=widgets.comment_widget,
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
    
                
    @expose(template='genshi:calabro.templates.new_post')
    @identity.require(identity.in_group("admin"))
    def new_post(self):
        user = identity.current.user
        site=get_current_site()
        return dict(user=user,
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
                   
    @expose(template='genshi:calabro.templates.edit_post')
    @identity.require(identity.in_group("admin"))
    def edit_post(self,year, month, day, title):
        permalink = '/'.join((year, month, day, title))
        site=get_current_site()
        post = Posts.find_by_permalink(permalink=permalink, site=site)
        return dict(post=post,
                   site=site,
                   comment_widget=widgets.comment_widget,
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
    def create_post(self, title, text, user_id, tags):
        t = datetime.now()
        site=get_current_site()
        user = User.get(user_id)
        cleaned = remove_special_char(title)
        permalink = "/".join((t.strftime('%Y/%m/%d'), cleaned.strip()))
        post = Posts(title=title, 
                     text=text, 
                     user=user, 
                     site=site,
                     created=t,
                     updated=None,
                     archives=(t.strftime('%Y/%m')),
                     permalink=permalink)
                     
        tag_list = Tags.parse(tags)
        for tag_name in tag_list:
            tag = Tags.find_or_create(name=tag_name, site=site)
            tag.count = tag.count + 1
            post.addTags(tag)
                
        redirect_to_home()
        
    @expose()
    def update_post(self, post_id, title, text, user_id, tags):
        t = datetime.now()
        site=get_current_site()
        user = User.get(user_id)
        post = Posts.get(post_id)
        post.set(title=title,
                 text=text,
                 user=user,
                 updated=t)
        
        tag_list = Tags.parse(tags)
        for tag_name in tag_list:
            tag = Tags.find_or_create(name=tag_name, site=site)
            if tag not in post.tags:
                tag.count = tag.count + 1            
                post.addTags(tag)
                              
        redirect_to_home()
    
        
    @expose(fragment=True)
    def create_comment(self, post_id, name, web_site, email, text):
        
        #sanitize input...
        post = Posts.get(post_id)
        comments = list(post.comments)
        comment = Comments(post=post, name=name, web_site=web_site, email=email, text=text, created=datetime.now())
        comments.append(comment)
        return widgets.comment_widget.render(comment=comment)
        
    @expose()
    def comment_count(self, post_id):
        post = Posts.get(post_id)
        return post.number_of_comments();
    
