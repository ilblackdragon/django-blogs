from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from blog.models import Post, IS_DRAFT, IS_PUBLIC


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('author', 'slug', 'creator_ip', 'created_at', 'updated_at', 'publish', 
                    'status', 'comments_count', 'last_comment_datetime', 'tags', 'tease', 'rating', 'votes')
    
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        super(PostForm, self).__init__(request.POST or None, *args, **kwargs)

    def save(self, *args, **kwargs):
        body = self.cleaned_data['body']
        editor_cut = body.find('<hr class="editor_cut"')
        tease = body[:editor_cut]
        post = super(PostForm, self).save(*args, **kwargs)
        if editor_cut == -1:
            post.tease = ''
        else:
            post.tease = tease
        return post
