from django.contrib import admin
from rango.models import Category, Article, UserProfile

class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    
class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    list_display = ('title', 'category', 'url', 'content', 'article_picture')

admin.site.register(Category, CategoryAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(UserProfile)