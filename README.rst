django-blogs
##############

**Django blogs** is module that provide configurable blogs for Django projects.

.. contents::

Quick overview
==============

- Using this module, you can implement blogging system in your project.
- This application allows to configure:
-- One blog (for companies news blog or for personal blog)
-- Multiblogging system (multiple blogs with different topics, for internet societies or instead of forum as more orginized way to share information)
-- Blog-per-user system (each user writes in his own blog, useful for companies when each person has it's own blog)
-- Mix of blog-per-user and blog-per-topic - multiple blogs with specific topic and each user has own blog (Large internet societies, social networks)
- Post's content is cleaned up to contain only safe html tags. So you can use any JS editor you like (we use http://frol.github.com/prostoEscribir/)
- Each post can have tease which will be shown at when posts are listed, you can configure how will it be cut and how long it can be.
- RSS feeds are available for all types of blogs.

Requirements
==============

- python >= 2.5
- pip >= 0.8
- django >= 1.2
- django-misc (https://github.com/ilblackdragon/django-misc)
- django-pagination
- django-tagging
- django-ratings (https://github.com/ilblackdragon/django-ratings)

Optional:

- django-threadedcomments (https://github.com/ilblackdragon/django-threadedcomments)
- django-notification (https://github.com/frol/django-notification)

Installation
=============

**Django blogs** should be installed using pip: ::

    pip install git+git://github.com/ilblackdragon/django-blogs.git


Setup
============

- Add 'blog' to INSTALLED_APPS ::

    INSTALLED_APPS += ( 'blog', )

- Add blog urls to urlpatterns in url.py: ::

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

Please, consider templates and css that are in this application - as example how to create your own design.
Note, that I use django-themes (https://github.com/ilblackdragon/django-themes) in my templates.


Configure django-blogs
===============

There are two main settings:

- BLOG_ENABLE_USER_BLOG - enable user blogs, by default TRUE

- BLOG_ENABLE_BLOGS - enable multiblogging system, by default TRUE

Additional settings:

- BLOG_SHORT_POST_MAX_LENGTH - limits to post, that can be without tease, by default - 2048 symbols.

- BLOG_CUT_MAX_LENGTH - limits to size of cut added, by default - 2048 symbols.

- BLOG_CUT_TAG and BLOG_CUT_TAG_SYNONYMS are added to help customize tag that is used to cut post on tease and main content. Defaults: '<hr class="redactor_cut">' as main cut tag, and <!--more--> as one synonym.


Contributing
============

Development of django-blogs happens at github: https://github.com/ilblackdragon/django-blogs

Note, that I don't like having django-ratings as obligatory requirement, and if you have a solution how to make it not to be obligatory but still be able to use it's RatingField as an optional feature - I'm open for suggestion.

License
============

Copyright (C) 2013 Illia Polosukhin
This program is licensed under the MIT License (see LICENSE)
 
