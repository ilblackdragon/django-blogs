from blog.models import Post, Category
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'publish', 'status')
    list_filter         = ('publish', 'status')
    search_fields       = ('title', 'body', 'tease')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
