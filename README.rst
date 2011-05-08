django-blogs
##############

**Django blogs** is module that provide configurable Django blogs.

.. contents::

Quick overview
==============

Using this module, you can add to your project blogs.
From simple one person blog, to multiblogging and multi-user blogs system.
Posts can conain safe html tags. RSS feeds for blogs and user's blogs.

Requirements
==============

- python >= 2.5
- pip >= 0.8
- django >= 1.2
- django-misc
- django-pagination


Installation
=============

**Django blogs** should be installed using pip: ::

    pip install git+git://github.com/ilblackdragon/django-blogs.git


Setup
============

- Add 'blog' to INSTALLED_APPS ::

    INSTALLED_APPS += ( 'blog', )

- Add blog urls to urlpatterns in url.py:

    from blog.feeds import BlogFeedAll, BlogFeedBlog, BlogFeedUser

    blogs_feed_dict = {"feed_dict": {
        'all': BlogFeedAll,
        'blog' : BlogFeedBlog,
        'only': BlogFeedUser,
    }}


    urlpatterns = ('',
        ...
        (r'^blogs/', include('blog.urls')),
        (r'^b/', include('blogs.short_urls')), # For short urls, if you want
        (r'^feeds/posts/(?P<url>\w+)/', 'django.contrib.syndication.views.feed', blogs_feed_dict), # Rss feeds
        ...
    )

- Copy blog/static/ to your STATIC_URL path


Configure django-blogs
===============

There are two main settings:

- BLOG_ENABLE_USER_BLOG - enable user blogs, by default TRUE

- BLOG_ENABLE_BLOGS - enable multiblogging system, by default TRUE

Contributing
============

Development of django-blogs happens at github: https://github.com/ilblackdragon/django-blogs

License
============

Licensed under a `GNU lesser general public license`_.

.. _GNU lesser general public license: http://www.gnu.org/copyleft/lesser.html

