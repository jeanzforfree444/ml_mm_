from django.contrib import admin
from rango.models import Category, Article, UserProfile, Comment

class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}

    ordering = ['name']
    
class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    list_display = ('title', 'category', 'summary', 'content', 'article_picture')

    ordering = ['title']

class CommentAdmin(admin.ModelAdmin):

    list_display = ('article', 'user', 'content')

admin.site.register(Category, CategoryAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(UserProfile)

admin.site.register(Comment, CommentAdmin)