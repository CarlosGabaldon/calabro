from turbogears.database            import PackageHub
from sqlobject                      import *
from datetime                       import datetime, timedelta
import re
from turbogears                     import identity 
from turbogears.database            import set_db_uri



def get_current_site():
    import cherrypy
    path = cherrypy.request.path.split('/')
    site_name = path[1]
    return Sites.get_current(name=site_name)
    



hub = PackageHub("calabro")
__connection__ = hub


# todo.. modify model objects to be in scope to the Sites model

class Posts(SQLObject):
    title       = StringCol() 
    text        = StringCol()
    created     = DateTimeCol(default=datetime.now)
    updated     = DateTimeCol()
    comments    = MultipleJoin('Comments', joinColumn='post_id')
    user        = ForeignKey('User')
    permalink   = StringCol(length=255, alternateID=True)
    archives    = StringCol()
    site        = ForeignKey('Sites')
    tags        = RelatedJoin("Tags", 
                            intermediateTable="posts_tags",
                            joinColumn="post_id", 
                            otherColumn="tag_id")    
   
    
    def posted_date(self, format):
        return self.created.strftime(format)
        
    def posted_by(self):
        return "Posted by " + self.user.display_name
    
    def number_of_comments(self):
        number_of_comments = len(self.comments)
        if number_of_comments == 1:
            return str(number_of_comments) + " Comment"
        else:
            return str(number_of_comments) + " Comments"
    
    def tags_as_string(self):
        tags_string = ""
        for tag in self.tags:
            tags_string =  ' '.join((tags_string, tag.name))
        
        return tags_string
        
    @classmethod
    def find(cls, site, top=5):
        sql = "select posts.id from posts where posts.site_id = %s order by posts.created DESC LIMIT %s" % (site.id, top)
                 
        post_ids = Posts._connection.queryAll(sql)
        return [post for post_id in post_ids for post in Posts.select() if post.id == post_id[0]]
    
    @classmethod
    def find_all(cls, site):
        return Posts.select("posts.site_id= %s" % (site.id) , orderBy='-created')
    
    @classmethod
    def find_all_archived(cls, archives, site):
        return Posts.select("posts.archives= '%s' and posts.site_id= %s" % (archives, site.id), orderBy='-created')
        
    
    @classmethod
    def find_archive_count(cls, site):
        """Returns a tuple of rows, not a SQLSearchResults object """
        sql = """select *, count(archives) from posts 
                 where posts.site_id = %s  
                 group by archives having count(archives) >= 1 """ % (site.id)
        return Posts._connection.queryAll(sql)
       
       
       
    @classmethod
    def find_by_permalink(cls, permalink, site):
        posts = Posts.selectBy(permalink=permalink, site=site)
        return posts[0]
            
    @classmethod
    def find_by_tag(cls, tag, site):
        sql = """select posts.id from posts 
                 INNER JOIN posts_tags 
                 on posts.id = posts_tags.post_id 
                 INNER JOIN tags 
                 on posts_tags.tag_id = tags.id 
                 where tags.name =  '%s' 
                 and posts.site_id = '%s' 
                 order by posts.created DESC """ % (tag.name, site.id)
                 
        post_ids = Posts._connection.queryAll(sql)
        return [post for post_id in post_ids for post in Posts.select(orderBy='-created') if post.id == post_id[0]]
    
    @classmethod
    def find_by_query(cls, query, site):
        from string import Template
        template = Template("""select distinct posts.id from posts 
                               INNER JOIN posts_tags 
                               on posts.id = posts_tags.post_id 
                               INNER JOIN tags 
                               on posts_tags.tag_id = tags.id 
                               where ((posts.title like '%${item}%') 
                               or (posts.text like '%${item}%') 
                               or (tags.name like '%${item}%'))
                               and (posts.site_id = '${site_id}')
                               order by posts.created DESC """)
                               
        sql = template.substitute(item=query, site_id=str(site.id) )                 
        post_ids = Posts._connection.queryAll(str(sql))
        return [post for post_id in post_ids for post in Posts.select(orderBy='-created') if post.id == post_id[0]]
                             
                             
class Comments(SQLObject):
    text        = StringCol()
    name        = StringCol()
    email       = StringCol()
    web_site    = StringCol() 
    created     = DateTimeCol(default=datetime.now)
    post        = ForeignKey('Posts')    
    
    def posted_date(self, format):
        if self.created is None:
            return datetime.now().strftime(format)
        offset = self.created - timedelta(hours=7)
        return offset.strftime(format)
    
    @classmethod    
    def find_recent(cls):
        return Comments.select(orderBy='-created')[:5]
        
    def _short_text(self):
        text = "%s.." % self.text[:90]
        return text
    short_text = property(_short_text)
    
    
class Tags(SQLObject):
    name      = StringCol()
    site      = ForeignKey('Sites')
    posts     = RelatedJoin("Posts", 
                            intermediateTable="posts_tags",
                            joinColumn="tag_id", 
                            otherColumn="post_id")
    count    = IntCol(default=0)
    
    @classmethod
    def find_all(cls, site):
        return Tags.selectBy(site=site)
                            
    @classmethod
    def find_or_create(cls, name, site):        
         tag = Tags.find_by(name, site)
         if tag == None:
            return Tags(name=name, 
                        site=site)
                        
         return tag
    
    @classmethod
    def find_by(cls, name, site):
        tags = Tags.selectBy(name=str(name).strip(), site=site)
        if tags.count() == 0:
            return None
        return tags[0]
             
    @classmethod
    def parse(cls, tags):
     '''Parses a comma separated list of tags into 
        tag names handles all kinds of different tags. 
        (comma seperated, space seperated)
        Todo...Enhance to support more formats (in quotes)
     '''
     return re.split('[,\\s]+', tags)
  

class Sites(SQLObject):
    title               = StringCol()
    name                = StringCol()
    subtitle            = StringCol()
    email               = StringCol()
    posts_per_page      = IntCol()
    url                 = StringCol()
    description         = StringCol()
    about_image         = StringCol()
    theme               = StringCol()
    users               = RelatedJoin("User", 
                            intermediateTable="sites_users",
                            joinColumn="site_id", 
                            otherColumn="user_id")
    badges             = MultipleJoin('Badges', joinColumn='site_id')          
    
    @classmethod
    def get_current(cls, name):
        try:
            sites = Sites.selectBy(name=name)
        except SQLObjectNotFound:
            return None
        return sites[0]
        
    @classmethod
    def find_all(cls):
        return Sites.select()
        

class Badges(SQLObject):
    name      = StringCol()
    html      = StringCol()
    site      = ForeignKey('Sites')
    

class Themes(SQLObject):
    name = StringCol()        
    
    @classmethod
    def find_all(cls):
        return Themes.select()
        
class Pages(SQLObject):
    name                = StringCol()
    title               = StringCol()
    body                = StringCol()
    site                = ForeignKey('Sites')

    @classmethod
    def find_all(cls, site):
        return Pages.selectBy(site=site)

    @classmethod
    def find_by_name(cls, name, site):
        pages = Pages.selectBy(name=str(name).strip(), site=site)
        if pages.count() == 0:
            return None
        
        return pages[0]
    
# identity models.
class Visit(SQLObject):
    class sqlmeta:
        table = "visit"

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName="by_visit_key")
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)

class VisitIdentity(SQLObject):
    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName="by_visit_key")
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """

    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = "tg_group"

    group_name = UnicodeCol(length=16, alternateID=True,
                            alternateMethodName="by_group_name")
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = RelatedJoin("User", intermediateTable="user_group",
                        joinColumn="group_id", otherColumn="user_id")

    # collection of all permissions for this group
    permissions = RelatedJoin("Permission", joinColumn="group_id", 
                              intermediateTable="group_permission",
                              otherColumn="permission_id")
                              
    @classmethod
    def find_all(cls, site):
        return Group.select()

    @classmethod
    def find_by_id(cls, id, site):
        return Group.get(id)

class User(SQLObject):
    """
    Reasonably basic User definition. Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = "tg_user"

    user_name = UnicodeCol(length=16, alternateID=True)
                           #alternateMethodName="by_user_name")
                           
                           
    # ***********************************************
    # Custome hook into identity to restrict logins by site, 
    # pragmatic way, but not the most elegant way...
    # maybe after more understanding of TG.Identity 
    # can refactor a more OO way my overriding 
    # SqlObjectIdentityProvider 
    # ***********************************************
    @classmethod                       
    def by_user_name(cls, user_name):
        site=get_current_site()
        sql = """select tg_user.id from tg_user
                 INNER JOIN sites_users 
                 on tg_user.id = sites_users.user_id 
                 where tg_user.user_name = '%s'
                 and sites_users.site_id = %s""" % (user_name, site.id)
                 
                 
        user_id = User._connection.queryAll(sql)
        if len(user_id) == 0: raise SQLObjectNotFound
        return User.get(user_id[0][0])
        
    # ****************************
    # end hook
    #****************************
        
        
        
    email_address = UnicodeCol(length=255, alternateID=True,
                               alternateMethodName="by_email_address")
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)
    sites     = RelatedJoin("Sites", 
                            intermediateTable="sites_users",
                            joinColumn="user_id", 
                            otherColumn="site_id") 

    # groups this user belongs to
    groups = RelatedJoin("Group", intermediateTable="user_group",
                         joinColumn="user_id", otherColumn="group_id")

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)

    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password)

    @classmethod
    def find_all(cls, site):
        #return User.selectBy(site=site)
        return User.select()

class Permission(SQLObject):
    permission_name = UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName="by_permission_name")
    description = UnicodeCol(length=255)

    groups = RelatedJoin("Group",
                        intermediateTable="group_permission",
                         joinColumn="permission_id", 
                         otherColumn="group_id")



def populate_default_data():
    """Populates default data into a new database. 
       Run from shell: $ python calabro/model.py """
    
    #figure out why I have to set this manually, PackageHub can not seem to find the dev.cfg
    set_db_uri(dburi="mysql://root:@localhost:5432/calabro")
    
    user = User(user_name="Joe",
               email_address="joe@cox.net", 
                display_name="Joe John", 
                password="password")
    
    user2 = User(user_name="applepy",
                email_address="apple_py@py.net", 
                display_name="Apple Py", 
                password="applepy")
                
    group = Group(group_name="admin", 
                  display_name="Administrator")
    permission = Permission(permission_name="create_posts", 
                            description="Can create new posts")
    group.addPermission(permission)
    group.addUser(user)
    group.addUser(user2)
    
    theme1 = Themes(name="hemingway_reloaded")
    theme2 = Themes(name="simpla")
    
    site = Sites(title="My Blog",
                name="my",
                subtitle="Calabro powered",
                email="me@someplace.com",
                about_image="/static/images/calabro_logo.png",
                url="http://code.google.com/p/calabro",
                posts_per_page=5,
                description='''The fun easy to use web publishing system.''',
                theme="hemingway_reloaded")
    
    site2 = Sites(title="Python Talk",
                name="py_talk",
                subtitle="Discussing Python",
                about_image="/static/images/py_talk.png",
                email="py@cox.net",
                url="http://py_talk.com",
                posts_per_page=10,
                description='''The joy, questions, answers, and ramblings in the Python world.''',
                theme="simpla")
                
    
    site.addUser(user)
    site2.addUser(user2)

if __name__ == "__main__":
    populate_default_data()
    
    