# encoding: utf-8
from django.contrib import admin

from blog.models import Post, Blog, BlogUserAccess


class BlogUserAccessInline(admin.TabularInline):
    model = BlogUserAccess
    raw_id_fields = ('user', )


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        BlogUserAccessInline,
    ]


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'body', 'tease')
    raw_id_fields = ('author', 'rating')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
