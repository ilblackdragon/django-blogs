from django.conf.urls.defaults import *
from django.conf import settings

from blog.models import Post, Category, IS_PUBLIC
from blog.forms import BlogForm

PAGINATION = getattr(settings, 'PAGINATION_DEFAULT_PAGINATION', 10)

category_dict = {
    'queryset': Category.objects.all(),
    'template_object_name': 'category',
}

post_dict = {
    'queryset': Post.objects.filter(status = IS_PUBLIC),
    'template_object_name': 'post',
}

category_dict_paginate = dict(category_dict, paginate_by = PAGINATION)
post_dict_paginate = dict(post_dict, paginate_by = PAGINATION)

urlpatterns = patterns('django.views.generic.list_detail',
)

urlpatterns += patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', post_dict_paginate, name='blog_post_list'),
    url(r'^categories/$', 'django.views.generic.list_detail.object_list', category_dict_paginate, name='blog_category_list'),

    url(r'^user/(?P<username>[-\w]+)/$', 'blog.views.user_post_list', dict(post_dict_paginate, template_name = 'blog/user_post_list.html'), name='blog_user_post_list'),
    url(r'^user/(?P<username>[-\w]+)/(?P<slug>[-\w]+)/$', 'blog.views.user_post_detail', post_dict, name='blog_user_post_detail'),

    # your posts
    url(r'^my_posts/$', 'blog.views.my_post_list', dict(post_dict_paginate, template_name = 'blog/post_my_list.html'), name='blog_my_post_list'),

    # new blog post
    url(r'^add/$', 'blog.views.add', name='blog_add'),

    # edit blog post
    url(r'^edit/(\d+)/$', 'blog.views.edit', name='blog_edit'),

    #destory blog post
    url(r'^delete/(\d+)/$', 'blog.views.delete', name='blog_delete'),

    # ajax validation
    (r'^validate/$', 'ajax_validation.views.validate',
                    {'form_class': BlogForm,
                     'callback': lambda request, *args, **kwargs: {'user': request.user}
                    },'blog_form_validate'),

    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$', 'blog.views.category_post_detail', post_dict, name='blog_post_detail'),
    url(r'^(?P<slug>[\w]+)/$', 'django.views.generic.list_detail.object_detail', category_dict, name='blog_category_detail'),
)
