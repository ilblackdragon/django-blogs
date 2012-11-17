# encoding: utf-8
from django.conf.urls.defaults import patterns, url

from blog.models import Post, Blog
from blog import settings

post_dict = {
    'queryset': Post.objects.filter(),
    'template_object_name': 'post',
}

post_dict_public = {
    'queryset': Post.objects.filter(status=Post.IS_PUBLIC),
    'template_object_name': 'post',
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list',
        post_dict_public, name='blog_post_list'),
)

urlpatterns += patterns('blog.views',
    url(r'^my_posts/$', 'my_post_list', dict(post_dict,
            template_name='blog/user_post_compact_list.html'),
        name='blog_my_post_list'),
    url(r'^add/$', 'post_add', name='blog_post_add'),
    url(r'^edit/(?P<id>\d+)/$', 'post_edit', name='blog_post_edit'),
    url(r'^delete/(?P<id>\d+)/$', 'post_delete', name='blog_post_delete'),
    url(r'^(?P<action>draft|public)/(?P<id>\d+)/$', 'post_change_status',
        name='blog_post_change_status'),
    url(r'^post/(?P<username>[\w\._\-]+)/(?P<slug>[-\w]+)/$',
        'user_post_detail', post_dict,
        name='blog_user_post_detail')
)

if settings.ENABLE_USER_BLOG:
    urlpatterns += patterns('blog.views',
        url(r'^user/(?P<username>[\w\._\-]+)/$', 'user_post_list',
            dict(post_dict_public, template_name='blog/user_post_list.html',
                extra_context=dict(compact_view=False)),
            name='blog_user_post_list'),
        url(r'^user/(?P<username>[\w\._\-]+)/compact/$', 'user_post_list',
            dict(post_dict_public, template_name='blog/user_post_list.html',
                extra_context=dict(compact_view=True)),
            name='blog_user_post_compact_list'),
    )

if settings.ENABLE_BLOGS:
    blog_dict = {
        'queryset': Blog.objects.all(),
        'template_object_name': 'blog',
    }
    
    urlpatterns += patterns('blog.views',
        url(r'^blogs/$', 'blog_list', blog_dict, name='blog_list'),
        url(r'^(?P<blog>[-\w]+)/(?P<slug>[-\w]+)/$', 'post_detail', name='blog_post_detail'),
        url(r'^(?P<slug>[-\w]+)/$', 'blog_detail', blog_dict, name='blog_detail'),
    )
