from datetime import datetime
from pytils.translit import slugify
from BeautifulSoup import BeautifulSoup

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from caching_ext.base import CachingMixin

from tagging.fields import TagField
from tagging.models import Tag
from threadedcomments.models import IS_PUBLIC as COMMENT_IS_PUBLIC,\
    IS_UNAPPROVED as COMMENT_IS_UNAPPROVED, IS_DELETED as COMMENT_IS_DELETED
from threadedcomments.models import ThreadedComment
from misc.html.clear import clear_html_code

from ratings.fields import RatingField

IS_DELETED = 0
IS_DRAFT = 1
IS_PUBLIC = 2


class Blog(CachingMixin):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'))
    icon = models.ImageField(_('blog icon'), height_field=None, width_field=None, blank=True, upload_to="blog_icons/", default="blog_icons/default.jpg")
    description = models.TextField(_('description'), max_length=256, blank=True)
    
    # TODO: Made moderators
    # TODO: Made list of who can write to blog (empty - every one)
    # TODO: Or just made gerenal access rights - who can view,write,comment on this blog
    #moderators = models.ManyToMany()

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog_blog_detail', None, {
            'slug': self.slug
            })

    def __unicode__(self):
        return self.name

    def get_last_post(self):
        post = self.post_list.filter(status=IS_PUBLIC)[:1]
        if post:
            return post[0]
        return None


STATUS_CHOICES = (
    (IS_DRAFT, _("Draft")), 
    (IS_PUBLIC, _("Public")),
    (IS_DELETED, _("Deleted"))
)

class Post(CachingMixin):
    """Post model."""
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), blank=True)
    author = models.ForeignKey(User, related_name="added_posts")
    creator_ip = models.CharField(_("IP Address of the Post Creator"), max_length=255, blank=True, null=True)
    tease = models.TextField(_('tease'), blank=True)
    body = models.TextField(_('body'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=IS_DRAFT)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=datetime.now)
    created_at = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at = models.DateTimeField(_('updated at'))
    tags = TagField()
    blog = models.ForeignKey(Blog, related_name='post_list', null=True, blank=True)
    comments_count = models.IntegerField(_('comments count'), default=0)
    last_comment_datetime = models.DateTimeField(_('date of last comment'), default=datetime.now)
    
    rating = RatingField()
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-updated_at',)
        get_latest_by = 'updated_at'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.blog:
            return ('blog_post_detail', None, {
                'blog': self.blog.slug,
                'slug': self.slug,
            })
        else:
            return ('blog_user_post_detail', None, {
                'username': self.author.username,
                'slug': self.slug,
            })

    def save(self, force_insert=False, force_update=False, update_date=True):
        if update_date:
            self.updated_at = datetime.now()
        if (self.slug == None or self.slug == ''):
            if not self.id:
                super(Post, self).save(force_insert, force_update)
            self.slug = '%d-%s' % (self.id, slugify(self.title))
        if self.tease:
            editor_cut = self.body.find('<hr class="editor_cut"/>')
            if editor_cut != -1:
                self.tease = self.body[:editor_cut]
        self.body = clear_html_code(self.body)
        self.tease = clear_html_code(self.tease)
        super(Post, self).save(force_insert, force_update)

    def is_public(self):
        return self.status == IS_PUBLIC

    def comment_status_changed(self, comment, status):
        if status == COMMENT_IS_PUBLIC:
            self.comments_count += 1
        elif status == COMMENT_IS_UNAPPROVED or status == COMMENT_IS_DELETED:
            self.comments_count -= 1
        self.save(update_date=False)

    def can_comment(self, user):
        return self.allow_comments
    
    def get_owners(self):
        return [self.author]
