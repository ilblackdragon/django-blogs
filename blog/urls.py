# encoding: utf-8
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url # Django < 1.6

from blog.models import Post, Blog
from blog import settings


urlpatterns = patterns('blog.views',
    url(r'^$', 'post_list', name='blog_post_list'),
    url(r'^my_posts/$', 'my_post_list', name='blog_my_post_list'),
    url(r'^add/$', 'post_add', name='blog_post_add'),
    url(r'^edit/(?P<id>\d+)/$', 'post_edit', name='blog_post_edit'),
    url(r'^delete/(?P<id>\d+)/$', 'post_delete', name='blog_post_delete'),
    url(r'^(?P<action>draft|public)/(?P<id>\d+)/$', 'post_change_status',
        name='blog_post_change_status'),
    url(r'^post/(?P<username>[\w\._\-]+)/(?P<slug>[-\w]+)/$',
        'user_post_detail', name='blog_user_post_detail')
)

if settings.ENABLE_USER_BLOG:
    urlpatterns += patterns('blog.views',
        url(r'^user/(?P<username>[\w\._\-]+)/$', 'user_post_list',
            {'compact_view': False}, name='blog_user_post_list'),
        url(r'^user/(?P<username>[\w\._\-]+)/compact/$', 'user_post_list',
            {'compact_view': True}, name='blog_user_post_compact_list'),
    )

if settings.ENABLE_BLOGS:
    urlpatterns += patterns('blog.views',
        url(r'^blogs/$', 'blog_list', name='blog_list'),
        url(r'^(?P<blog_slug>[-\w]+)/(?P<slug>[-\w]+)/$', 'post_detail', name='blog_post_detail'),
        url(r'^(?P<slug>[-\w]+)/$', 'blog_detail', name='blog_detail'),
    )
