# encoding: utf-8
from datetime import datetime
from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from misc.html.clear import clear_html_code

from blog import settings
from blog.models import Post, Blog


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('author', 'slug', 'creator_ip', 'created_at', 'updated_at', 'publish', 
                    'status', 'comments_count', 'last_comment_datetime', 'tags', 'tease', 'rating', 'rating_score', 'votes')
    
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        super(PostForm, self).__init__(request.POST or None, *args, **kwargs)
        self.fields['blog'].queryset = Blog.objects.filter(
            Q(can_write=True) | 
            Q(blog_user_access_list__user=self.user, blog_user_access_list__can_write=True) |
            Q(blog_user_access_list__user=self.user, blog_user_access_list__is_moderator=True)
        ).distinct()

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < settings.POST_NAME_MIN_LENGTH:
            raise forms.ValidationError(_("Post title should be at least 3 characters."))
        return title

    def clean_body(self):
        body = self.cleaned_data['body']
        for synonym in settings.CUT_TAG_SYNONYMS:
            body = body.replace(synonym, CUT_TAG)
        editor_cut = body.find(CUT_TAG)
        if editor_cut != -1:
            tease = body[:editor_cut]
            tease = clear_html_code(tease)
        else:
            tease = ''
        body = clear_html_code(body)
        
        if len(body) > settings.SHORT_POST_MAX_LENGTH and editor_cut == -1:
            raise forms.ValidationError(_("Your post is too long and without cut - please add cut somewhere to leave only introduction part before it."))
        if editor_cut > settings.CUT_MAX_LENGTH:
            raise forms.ValidationError(_("Your cut is too long - please add cut somewhere to leave only introduction part before it."))
        self.cleaned_data['tease'] = tease
        return body

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit', True)
        kwargs['commit'] = False
        post = super(PostForm, self).save(*args, **kwargs)
        post.tease = self.cleaned_data['tease']
        post.body = self.cleaned_data['body']
        if commit:
            post.save()
        return post
