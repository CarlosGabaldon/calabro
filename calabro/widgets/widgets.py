from turbogears.widgets import Widget, CompoundWidget


class CommentWidget(Widget):
    template        = 'calabro.widgets.templates.comment'
    params          = ['comment', 'read_only']
    read_only       = False

comment_widget = CommentWidget()

class ArchivesWidget(Widget):
    template        = 'calabro.widgets.templates.archives'
    params          = ['archives', 'site', 'read_only']
    read_only       = False
    
archives_widget = ArchivesWidget()


class TagsWidget(Widget):
    template        = 'calabro.widgets.templates.tags'
    params          = ['tags', 'site', 'read_only']
    read_only       = False
    
tags_widget = TagsWidget()


class PostsWidget(Widget):
    template        = 'calabro.widgets.templates.posts'
    params          = ['posts', 'site', 'read_only']
    read_only       = False
    
posts_widget = PostsWidget()

class PagesWidget(Widget):
    template        = 'calabro.widgets.templates.pages'
    params          = ['pages', 'site', 'read_only']
    read_only       = False
    
pages_widget = PagesWidget()

class AdminWidget(Widget):
    template        = 'calabro.widgets.templates.admin'
    params          = ['site', 'read_only']
    read_only       = False
    
admin_widget = AdminWidget()

class BadgeWidget(Widget):
    template        = 'calabro.widgets.templates.badge'
    params          = ['badge', 'read_only']
    read_only       = False
    
badge_widget = BadgeWidget()

class RecentCommentsWidget(Widget):
    template        = 'calabro.widgets.templates.recent_comments'
    params          = ['recent_comments', 'site', 'read_only']
    read_only       = False
    
recent_comments_widget = RecentCommentsWidget()
