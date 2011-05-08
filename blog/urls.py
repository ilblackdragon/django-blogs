from django.conf.urls.defaults import patterns, url
from django.conf import settings

from blog.models import Post, Blog, IS_PUBLIC

ENABLE_USER_BLOG = getattr(settings, 'BLOG_ENABLE_USER_BLOG', True)
ENABLE_BLOGS = getattr(settings, 'BLOG_ENABLE_BLOGS', True)

post_dict = {
    'queryset': Post.objects.filter(),
    'template_object_name': 'post',
}

post_dict_public = {
    'queryset': Post.objects.filter(status=IS_PUBLIC),
    'template_object_name': 'post',
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', post_dict_public, name='blog_post_list'),
    url(r'^my_posts/$', 'blog.views.my_post_list', dict(post_dict, template_name='blog/post_my_list.html'), name='blog_my_post_list'),
    url(r'^add/$', 'blog.views.add', name='blog_add'),
    url(r'^edit/(?P<id>\d+)/$', 'blog.views.edit', name='blog_edit'),
    url(r'^(?P<action>draft|public)/(?P<id>\d+)/$', 'blog.views.change_status', name='blog_change_status'),
    url(r'^post/(?P<username>[\w\._\-]+)/(?P<slug>[-\w]+)/$', 'blog.views.blog_user_post_detail', post_dict, name='blog_user_post_detail')
)

if ENABLE_USER_BLOG:
    urlpatterns += patterns('',
        url(r'^user/(?P<username>[\w\._\-]+)/$', 'blog.views.user_post_list', dict(post_dict_public, template_name='blog/user_post_list.html'), name='blog_user_post_list'),
    )

if ENABLE_BLOGS:
    blog_dict = {
        'queryset': Blog.objects.all(),
        'template_object_name': 'blog',
    }
    
    urlpatterns += patterns('',
        url(r'^blogs/$', 'django.views.generic.list_detail.object_list', blog_dict, name='blog_blog_list'),
        url(r'^(?P<blog>[-\w]+)/(?P<slug>[-\w]+)/$', 'blog.views.blog_post_detail', name='blog_post_detail'),
        url(r'^(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', blog_dict, name='blog_blog_detail'),
    )

