# encoding: utf-8
from blog.models import Post

from voter.models import create_rating

def import_post(user, import_item):
    title = import_item.title
    if not title:
        title = "(Noname)"
    post = Post(author=user, title=title, tease=import_item.description,
        body=import_item.text, rating=create_rating())
    post.save()
    return 'http://url'
