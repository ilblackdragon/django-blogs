from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from blog.models import Post

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('author', 'slug', 'creator_ip', 'created_at', 'updated_at', 'publish', 'status')
    
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        if request.method == "POST":
            super(BlogForm, self).__init__(request.POST, *args, **kwargs)
        else:
            super(BlogForm, self).__init__(*args, **kwargs)
