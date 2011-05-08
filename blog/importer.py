from blog.models import Post


def import_post(request, import_item):
    post = Post(author=request.user, title=import_item.title,
        tease=import_item.description, body=import_item.text)
    post.save()
    return 'http://url'
