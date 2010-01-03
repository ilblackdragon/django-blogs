from datetime import datetime
from pytils.translit import slugify

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.models import Tag

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

class Category(models.Model):
    name = models.CharField(_('name'), max_length = 200)
    slug = models.SlugField(_('slug'))

    # may be need moderators
    #moderators = models.ManyToMany()
    # may also access rights, like who can view\post\comment this category

    class Meta:
        verbose_name        = _('category')
        verbose_name_plural = _('categories')

    @models.permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {
            'slug': self.slug
            })

    def __unicode__(self):
        return self.name

IS_DELETED = 0
IS_DRAFT = 1
IS_PUBLIC = 2
IS_APPROVED = 3

STATUS_CHOICES = (
    (IS_DRAFT, _("Draft")), 
    (IS_PUBLIC, _("Public")),
    (IS_APPROVED, _("Approved")),
    (IS_DELETED, _("Deleted"))
)

class Post(models.Model):
    """Post model."""
    title           = models.CharField(_('title'), max_length = 200)
    slug            = models.SlugField(_('slug'), blank = True)
    author          = models.ForeignKey(User, related_name = "added_posts")
    creator_ip      = models.IPAddressField(_("IP Address of the Post Creator"), blank = True, null = True)
    tease           = models.TextField(_('tease'), blank = True)
    body            = models.TextField(_('body'))
    status          = models.IntegerField(_('status'), choices = STATUS_CHOICES, default = IS_PUBLIC)
    allow_comments  = models.BooleanField(_('allow comments'), default = True)
    publish         = models.DateTimeField(_('publish'), default = datetime.now)
    created_at      = models.DateTimeField(_('created at'), default = datetime.now)
    updated_at      = models.DateTimeField(_('updated at'))
    markup          = models.CharField(_(u"Post Content Markup"), max_length = 20,
                              choices = settings.MARKUP_CHOICES,
                              null = True, blank = True)
    tags            = TagField()
    category        = models.ForeignKey(Category, related_name = 'post_list', null = True)
    
    class Meta:
        verbose_name        = _('post')
        verbose_name_plural = _('posts')
        ordering            = ('-publish',)
        get_latest_by       = 'publish'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_post_detail', None, {
            'category': self.category.slug,
            'slug': self.slug,
    })

    def save(self, force_insert=False, force_update=False):
        self.updated_at = datetime.now()
        if (self.slug == None or self.slug == ''):
            if not self.id:
                super(Post, self).save(force_insert, force_update)
            self.slug = '%d-%s' % (self.id, slugify(self.title))
        super(Post, self).save(force_insert, force_update)

# handle notification of new comments
from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Post):
        post = instance.content_object
        if notification:
            notification.send([post.author], "blog_post_comment",
                {"user": instance.user, "post": post, "comment": instance})
models.signals.post_save.connect(new_comment, sender=ThreadedComment)
