from django.contrib import admin
from rango.models import Category, Article, UserProfile, Comment, ForumCategory, Thread, Post, Poll, PollOption

class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}

    ordering = ['name']
    
class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    list_display = ('title', 'category', 'author')

    ordering = ['title']

class CommentAdmin(admin.ModelAdmin):

    list_display = ('article', 'user', 'content')

class ForumCategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}

class ThreadAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(UserProfile)

admin.site.register(Comment, CommentAdmin)

admin.site.register(ForumCategory, ForumCategoryAdmin)

admin.site.register(Thread, ThreadAdmin)

admin.site.register(Post)

admin.site.register(Poll)

admin.site.register(PollOption)