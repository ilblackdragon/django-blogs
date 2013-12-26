# encoding: utf-8
from blog.models import Post

if 'voter' in settings.INSTALLED_APPS:
    from voter.models import create_rating

def import_post(user, import_item):
    title = import_item.title
    if not title:
        title = "(Noname)"
    kwargs = {
        'author': user, 
        'title': title, 
        'tease': import_item.description,
        'body': import_item.text
    }
    if 'voter' in settings.INSTALLED_APPS:
        kwargs['rating'] = create_rating()
    post = Post(**kwargs)
    post.save()
    return 'http://url'
