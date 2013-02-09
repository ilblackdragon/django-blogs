# encoding: utf-8
import re
from datetime import date

from django.conf import settings
from django.template import Variable, Node, RequestContext
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

if 'coffin' in settings.INSTALLED_APPS:
    from coffin.template import Library
else:
    from django.template import Library

from blog.models import Post

register = Library()

if 'coffin' in settings.INSTALLED_APPS:
    register.simple_tag = register.object

@register.tag
def check_post_status(parser, token):
    bits = token.contents.split(' ')
    return CheckPostStatus(bits[1], bits[2])

class CheckPostStatus(Node):
    def __init__(self, user, post):
        self.user = user
        self.post = post

    def render(self, context):
        user = Variable(self.user).resolve(context)
        post = Variable(self.post).resolve(context)
        if not user or not post:
            return ''
        context['show_post'] = post.is_visible_for_user(user)
        return ''

@register.simple_tag
def get_last_escalibro_post_list():
    return Post.objects.filter(status=Post.IS_PUBLIC, blog__slug='escalibro')

@register.simple_tag
def get_month_escalibro_post_list():
    now = date.today()
    month_beginning = date(now.year, now.month, 1)
    return get_last_escalibro_post_list().filter(updated_at__gte=month_beginning)

@register.inclusion_tag("blog/post_item.html", takes_context=True)
def show_blog_post(context, post):
    context['post'] = post
    context['post_undetailed'] = True
    return context

@register.inclusion_tag("blog/post_item.html", takes_context=True)
def show_full_blog_post(context, post):
    context['post'] = post
    context['post_undetailed'] = False
    return context
