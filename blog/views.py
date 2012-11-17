# encoding: utf-8
from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based, list_detail
from django.conf import settings
from django.db.models import Q

from misc.json_encode import json_response
from ratings.models import create_rating

from blog.models import Blog, Post
from blog.forms import PostForm
from blog.signals import post_published

def blog_list(request, *kargs, **kwargs):
    if request.user.is_authenticated():
        kwargs['queryset'] = kwargs['queryset'].filter(
            Q(can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__is_moderator=True)
       ).distinct()
    else:
         kwargs['queryset'] = kwargs['queryset'].filter(Q(can_read=True))
    return list_detail.object_list(request, *kargs, **kwargs)

def blog_detail(request, *kargs, **kwargs):
    if request.user.is_authenticated():
        blog = Blog.objects.filter(Q(slug=kwargs.get('slug', '')) & Q(
            Q(can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__is_moderator=True)
        )).distinct()
    else:
        blog = Blog.objects.filter(slug=kwargs.get('slug', ''), can_read=True)
    if len(blog) != 1:
        raise Http404("No blog matches given this slug or it isn't accessable")
    return list_detail.object_detail(request, *kargs, **kwargs)

def post_detail(request, *kargs, **kwargs):
    if request.user.is_authenticated():
        blog = Blog.objects.filter(Q(slug=kwargs.pop('blog', '')) & Q(
            Q(can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__is_moderator=True)
        )).distinct()
    else:
        blog = Blog.objects.filter(slug=kwargs.pop('blog', ''), can_read=True)
    if len(blog) != 1:
        raise Http404("No blog matches given this slug or it isn't accessable")
    kwargs['template_object_name'] = 'post'
    kwargs['queryset'] = Post.objects.filter(blog = blog[0])
    if request.user.is_authenticated():
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user) |\
                             kwargs['queryset'].filter(status=Post.IS_PUBLIC)
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(status=Post.IS_PUBLIC)
    return list_detail.object_detail(request, *kargs, **kwargs)

def user_post_detail(request, *kargs, **kwargs):
    user = get_object_or_404(User, username=kwargs.pop('username', ''))
    if user==request.user:
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user)
    else:
        kwargs['queryset'] = kwargs['queryset']\
            .filter(author=user, status=Post.IS_PUBLIC)
    return list_detail.object_detail(request, *kargs, **kwargs)

def user_post_list(request, *kargs, **kwargs):
    user = get_object_or_404(User, username=kwargs.pop('username', ''))
    if request.user == user:
        kwargs['queryset'] = Post.objects.filter(author=user)\
            .exclude(status=Post.IS_DELETED)
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(author=user)
    kwargs['extra_context'].update({
        'current_user': user,
    })
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def my_post_list(request, *kargs, **kwargs):
    kwargs['queryset'] = Post.objects.filter(author=request.user)\
        .exclude(status=Post.IS_DELETED)
    kwargs['extra_context'] = {'current_user': request.user}
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def post_change_status(request, action, id):
    post = get_object_or_404(Post, pk = id)
    if not post.can_edit(request.user):
        messages.error(request, "You can't change statuses of posts that aren't yours")
    else:
        if action == 'draft' and post.status == Post.IS_PUBLIC:
            post.status = Post.IS_DRAFT
        if action == 'public' and post.status == Post.IS_DRAFT:
            post.status = Post.IS_PUBLIC
            post_published.send(sender=Post, post=post)
        post.save()
        messages.success(request, _("Successfully change status for post '%s'") % post.title)
    return redirect("blog_my_post_list")

@login_required
def post_add(request, form_class=PostForm, template_name="blog/post_add.html"):
    post_form = form_class(request)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user
        post.rating = create_rating()
        creator_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if not creator_ip:
            creator_ip = request.META.get('REMOTE_ADDR', None)
        post.creator_ip = creator_ip
        post.save()
        messages.success(request, _("Successfully created post '%s'") % post.title)
        return redirect("blog_user_post_detail", username=request.user.username, slug=post.slug)
    return render_to_response(template_name, {'post_form': post_form, 'current_user': request.user},
        context_instance=RequestContext(request))

@login_required
def post_edit(request, id, form_class=PostForm, template_name="blog/post_edit.html"):
    post = get_object_or_404(Post, id=id)
    if not post.can_edit(request.user):
        messages.error(request, _("You can't edit posts that aren't yours"))
        return redirect("blog_my_post_list")
    post_form = form_class(request, instance=post)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.updated_at = datetime.now()
        post.save()
        messages.success(request, _("Successfully updated post '%s'") % post.title)
        return redirect("blog_user_post_detail", username=post.author.username, slug=post.slug)
    return render_to_response(template_name, {"post_form": post_form, "post": post}, context_instance=RequestContext(request))

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id, status=Post.IS_DRAFT)
    if not post.can_edit(request.user):
        messages.error(request, _("You can't delete posts that aren't yours"))
    else:
        post.delete()
    return redirect("blog_my_post_list")
