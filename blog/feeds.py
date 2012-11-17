# encoding: utf-8
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import linebreaks, escape, capfirst
from django.utils.translation import ugettext_lazy as _
from django.utils import feedgenerator

from blog.models import Post, Blog

ITEMS_PER_FEED = getattr(settings, 'BLOG_ITEMS_PER_FEED', 20)

class BasePostFeed(Feed):
    feed_type = feedgenerator.Atom1Feed

    def item_title(self, item):
        return item.title
    
    def item_pubdate(self, item):
        return item.updated_at
    
    def item_author_name(self, item):
        return item.author.username
    
    def item_author_link(self, item):
        return 'http://%s%s' % (settings.SITE_DOMAIN,
            reverse('poetry_user_works', args=[item.author.username]))

    def item_description(self, item):
        if item.tease:
            return linebreaks(escape(item.tease))
        return linebreaks(escape(item.body))


class BlogFeedAll(BasePostFeed):
    title = "Escalibro all posts"
    link = "http://%s/feeds/posts/all/" % settings.SITE_DOMAIN

    def items(self):
        return Post.objects.filter(status=Post.IS_PUBLIC).order_by("-updated_at")[:ITEMS_PER_FEED]


class BlogFeedBlog(BasePostFeed):
    def get_object(self, request, *args, **kwargs):
        return get_object_or_404(Blog, slug=request.GET.get('slug'))

    def link(self, blog):
        return 'http://%s/feeds/posts/blog/?slug=%s' % (
            settings.SITE_DOMAIN,
            blog.slug,
        )

    def title(self, blog):
        return "Escalibro blog %s" % blog.name

    def items(self, blog):
        return Post.objects.filter(blog=blog, status=Post.IS_PUBLIC).order_by("-updated_at")[:ITEMS_PER_FEED]


class BlogFeedUser(BasePostFeed):
    def get_object(self, request, *args, **kwargs):
        return get_object_or_404(User, username=request.GET.get('username'))
    
    def link(self, user):
        return 'http://%s/feeds/posts/only/?username=%s' % (
            settings.SITE_DOMAIN,
            user.username,
        )

    def title(self, user):
        return "Escalibro user %s" % user.username

    def items(self, user):
        return Post.objects.filter(author=user, status=Post.IS_PUBLIC).order_by("-updated_at")[:ITEMS_PER_FEED]
