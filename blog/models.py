# encoding: utf-8
from datetime import datetime
from pytils.translit import slugify

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

if 'threadedcomments' in settings.INSTALLED_APPS:
    from threadedcomments.models import ThreadedComment
else:
    ThreadedComment = None

from tagging.fields import TagField
from voter.models import RatingField

class BlogUserAccess(models.Model):
    blog = models.ForeignKey('Blog', verbose_name=_("Blog"), 
        related_name="blog_user_access_list")
    user = models.ForeignKey(User, verbose_name=_("User"),
        related_name="blog_user_access_list")
    is_moderator = models.BooleanField(_("Is moderator"))
    can_read = models.BooleanField(_("Can read"))
    can_write = models.BooleanField(_("Can write"))

class Blog(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'))
    icon = models.ImageField(_('blog icon'), height_field=None, width_field=None, blank=True, upload_to="blog_icons/", default="blog_icons/default.jpg")
    description = models.TextField(_('description'), max_length=256, blank=True)

    user_access_list = models.ManyToManyField(User, through=BlogUserAccess,
        related_name="blog_user_access_m2m_list", verbose_name=_("User access list"))
    can_read = models.BooleanField(_('Are everybody can read'), default=True)
    can_write = models.BooleanField(_('Are everybody can write'), default=True)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog_detail', None, {
            'slug': self.slug
            })

    def __unicode__(self):
        return self.name

    def get_last_post(self):
        post = self.post_list.filter(status=Post.IS_PUBLIC)[:1]
        if post:
            return post[0]
        return None


class Post(models.Model):
    """Post model."""
    IS_DELETED = 0
    IS_DRAFT = 1
    IS_PUBLIC = 2

    STATUS_CHOICES = (
        (IS_DRAFT, _("Draft")), 
        (IS_PUBLIC, _("Public")),
        (IS_DELETED, _("Deleted"))
    )

    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True)
    author = models.ForeignKey(User, related_name='added_posts')
    creator_ip = models.CharField(_("IP Address of the Post Creator"),
        max_length=255, blank=True, null=True)
    tease = models.TextField(_("tease"), blank=True)
    body = models.TextField(_("body"))
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=IS_DRAFT)
    allow_comments = models.BooleanField(_("allow comments"), default=True)
    publish = models.DateTimeField(_("publish"), default=datetime.now)
    created_at = models.DateTimeField(_("created at"), default=datetime.now)
    updated_at = models.DateTimeField(_("updated at"), default=datetime.now)
    tags = TagField()
    blog = models.ForeignKey(Blog, verbose_name=_("Blog"),
        related_name='post_list', null=True, blank=True)
    comments_count = models.IntegerField(_("comments count"), default=0)
    last_comment_datetime = models.DateTimeField(_("date of last comment"),
        default=datetime.now)
    
    rating = RatingField(related_name="post_list")
    rating_score = models.FloatField(_("Rating score"), default=0)
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-updated_at',)
        get_latest_by = 'updated_at'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.blog:
            return ('blog_post_detail', None, {
                'blog_slug': self.blog.slug,
                'slug': self.slug,
            })
        else:
            return ('blog_user_post_detail', None, {
                'username': self.author.username,
                'slug': self.slug,
            })

    def save(self, **kwargs):
        if (self.slug == None or self.slug == ''):
            if not self.id:
                super(Post, self).save(**kwargs)
            self.slug = ('%d-%s' % (self.id, slugify(self.title)))[:50]
        super(Post, self).save(**kwargs)

    @property
    def is_public(self):
        return self.status == self.IS_PUBLIC

    def is_visible_for_user(self, user):
        return self.is_public or self.author == user

    def comment_status_changed(self, comment, status):
        if not ThreadedComment:
            return
        if status == ThreadedComment.IS_PUBLIC:
            self.comments_count += 1
        elif status == ThreadedComment.IS_UNAPPROVED or status == ThreadedComment.IS_DELETED:
            self.comments_count -= 1
        self._feed_not_need_update = True
        self.save()
        self._feed_not_need_update = False

    def can_comment(self, user):
        return self.allow_comments

    def can_edit(self, user):
        return user.is_authenticated() and (self.author == user or \
            (self.blog and self.blog.blog_user_access_list.filter(user=user, is_moderator=True).exists()))

    def get_owners(self):
        return [self.author]

