# encoding: utf-8
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

if 'coffin' in settings.INSTALLED_APPS:
    from coffin.template.response import TemplateResponse
else:
    from django.template.response import TemplateResponse

from voter.models import create_rating

from blog.models import Blog, Post
from blog.forms import PostForm
from blog.signals import post_published

def blog_list(request, template_name='blog/blog_list.html'):
    blog_list = Blog.objects.all()
    if request.user.is_authenticated():
        blog_list = blog_list.filter(
            Q(can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__is_moderator=True)
        ).distinct()
    else:
        blog_list = blog_list.filter(Q(can_read=True))
    return TemplateResponse(request, template_name, {'blog_list': blog_list})

def blog_detail(request, slug, template_name='blog/blog_detail.html'):
    blog = Blog.objects.filter(slug=slug)
    if request.user.is_authenticated():
        blog = blog.filter(
            Q(can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__is_moderator=True)
        ).distinct()
    else:
        blog = blog.filter(can_read=True)
    if not blog:
        raise Http404("No blog matches given this slug or it isn't accessable")
    return TemplateResponse(request, template_name, {'blog': blog[0]})

def post_list(request, template_name='blog/post_list.html'):
    return TemplateResponse(request, template_name,
        {'post_list': Post.objects.filter(status=Post.IS_PUBLIC)})

def post_detail(request, blog_slug, slug, template_name='blog/post_detail.html'):
    blog = Blog.objects.filter(slug=blog_slug)
    if request.user.is_authenticated():
        blog = blog.filter(
            Q(can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__can_read=True) |
            Q(blog_user_access_list__user=request.user, blog_user_access_list__is_moderator=True)
        ).distinct()
    else:
        blog = blog.filter(can_read=True)
    if not blog:
        raise Http404("No blog matches given this slug or it isn't accessable")
    post = Post.objects.filter(blog=blog[0], slug=slug)
    if request.user.is_authenticated():
        post = post.filter(Q(author=request.user) | Q(status=Post.IS_PUBLIC))
    else:
        post = post.filter(status=Post.IS_PUBLIC)
    if not post:
        raise Http404("No post matches given this slug or it isn't accessable")
    return TemplateResponse(request, template_name, {'post': post[0]})

def user_post_detail(request, username, slug, template_name='blog/post_detail.html'):
    user = get_object_or_404(User, username=username)
    post = Post.objects.filter(author=user, slug=slug)
    if request.user != user:
        post = post.filter(status=Post.IS_PUBLIC)
    if not post:
        raise Http404("No post matches given this slug or it isn't accessable")
    return TemplateResponse(request, template_name, {'post': post[0]})

def user_post_list(request, username, compact_view, template_name='blog/user_post_list.html'):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user)
    if request.user == user:
        post_list = post_list.exclude(status=Post.IS_DELETED)
    else:
        post_list = post_list.filter(status=Post.IS_PUBLIC)
    return TemplateResponse(request, template_name,
        {'post_list': post_list, 'current_user': user, 'compact_view': compact_view})

@login_required
def my_post_list(request, template_name='blog/user_post_compact_list.html'):
    post_list = Post.objects.filter(author=request.user)\
        .exclude(status=Post.IS_DELETED).order_by('status', '-created_at')
    return TemplateResponse(request, template_name,
        {'post_list': post_list, 'current_user': request.user})

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
    return TemplateResponse(request, template_name, {'post_form': post_form, 'current_user': request.user})

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
    return TemplateResponse(request, template_name, {"post_form": post_form, "post": post})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id, status=Post.IS_DRAFT)
    if not post.can_edit(request.user):
        messages.error(request, _("You can't delete posts that aren't yours"))
    else:
        post.delete()
    return redirect("blog_my_post_list")
