# encoding: utf-8
from django.conf.urls.defaults import patterns, url
from django.shortcuts import get_object_or_404

from misc.views import redirect_by_name

from blog.models import Blog, Post

def get_blog_slug(kwargs):
    return get_object_or_404(Blog, id=kwargs.pop('blog_id', 0)).slug
    
def get_post_slug(kwargs):
    return get_object_or_404(Post, id=kwargs.pop('post_id', 0)).slug

urlpatterns = patterns('',
    url('^b/(?P<blog_id>\d+)/(?P<post_id>\d+)/$', redirect_by_name, {'name': 'blog_post_detail', 'blog': get_blog_slug, 'slug': get_post_slug}, name="blog_post_detail_short"),
    url('^u/(?P<username>[\w\._\-]+)/(?P<post_id>\d+)/$', redirect_by_name, {'name': 'blog_user_post_detail', 'slug': get_post_slug}, name="blog_user_post_detail_short"),
)
