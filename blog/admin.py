from django.contrib import admin

from blog.models import Post, Blog


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'body', 'tease')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
