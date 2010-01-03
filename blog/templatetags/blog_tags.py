# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag("blog/post_item.html")
def show_blog_post(request, post):
    return {'request': request, 'post': post, 'post_undetailed': True}

@register.inclusion_tag("blog/post_item.html")
def show_full_blog_post(request, post):
    return {'request': request, 'post': post, 'post_undetailed': False}
