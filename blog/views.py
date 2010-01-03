import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based, list_detail
from django.conf import settings

from blog.models import Post, Category, IS_DRAFT, IS_PUBLIC, IS_DELETED
from blog.forms import *

def category_post_detail(request, *kargs, **kwargs):
    category = get_object_or_404(Category, slug = kwargs.pop('category', ''))
    kwargs['queryset'] = kwargs['queryset'].filter(category = category)
    return list_detail.object_detail(request, *kargs, **kwargs)

def user_post_detail(request, *kargs, **kwargs):
    user = get_object_or_404(User, username = kwargs.pop('username', ''))
    kwargs['queryset'] = kwargs['queryset'].filter(author = user)
    return list_detail.object_detail(request, *kargs, **kwargs)

def user_post_list(request, *kargs, **kwargs):
    user = get_object_or_404(User, username = kwargs.pop('username', ''))
    kwargs['queryset'] = kwargs['queryset'].filter(author = user)
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def my_post_list(request, *kargs, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].filter(author = request.user)
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def delete(request, id):
    post = get_object_or_404(Post, pk = id)
    if post.author != request.user:
        request.user.message_set.create(message="You can't delete posts that aren't yours")
    else:
        post.status = IS_DELETED
        post.save()
        request.user.message_set.create(message=_("Successfully deleted post '%s'") % post.title)
    return HttpResponseRedirect(reverse("blog_my_post_list"))

@login_required
def add(request, form_class=BlogForm, template_name="blog/post_add.html"):
    blog_form = form_class(request)
    if request.method == "POST" and blog_form.is_valid():
        blog = blog_form.save(commit=False)
        blog.author = request.user
        blog.status = IS_PUBLIC
        blog.creator_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        blog.save()
        request.user.message_set.create(message=_("Successfully created post '%s'") % blog.title)
        return HttpResponseRedirect(reverse("blog_my_post_list"))
    return render_to_response(template_name, { "blog_form": blog_form }, context_instance=RequestContext(request))

@login_required
def edit(request, id, form_class=BlogForm, template_name="blog/post_edit.html"):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        request.user.message_set.create(message="You can't edit posts that aren't yours")
        return HttpResponseRedirect(reverse("blog_my_post_list"))
    blog_form = form_class(request, instance=post)
    if request.method == "POST" and blog_form.is_valid():
        blog = blog_form.save(commit=False)
        blog.save()
        request.user.message_set.create(message=_("Successfully updated post '%s'") % blog.title)
        return HttpResponseRedirect(reverse("blog_my_post_list"))
    return render_to_response(template_name, {"blog_form": blog_form, "post": post }, context_instance=RequestContext(request))
