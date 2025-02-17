from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):

    NAME_MAX_LENGTH = 150

    DESCRIPTION_MAX_LENGTH = 1000

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)

    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    views = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    class Meta:

        ordering = ['name']

        verbose_name_plural = 'Categories'

    def __str__(self):

        return self.name

class Article(models.Model):

    TITLE_MAX_LENGTH = 500

    SUMMARY_MAX_LENGTH = 2000

    CONTENT_MAX_LENGTH = 20000

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=TITLE_MAX_LENGTH)

    summary = models.CharField(max_length=SUMMARY_MAX_LENGTH)

    content = models.CharField(max_length=CONTENT_MAX_LENGTH)

    article_picture = models.ImageField(upload_to='article_images', blank=True)

    views = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', null=True, blank=True)

    slug = models.SlugField(unique=True)

    last_visit = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)

        self.last_visit = timezone.now()

        super(Article, self).save(*args, **kwargs)

    class Meta:

        ordering = ['title']

        verbose_name_plural = 'Articles'

    def __str__(self):

        return self.title
    
class UserProfile(models.Model):

    NAME_MAX_LENGTH = 100

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)

    last_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)

    website = models.URLField(blank=True)

    profile_picture = models.ImageField(upload_to='profile_images', blank=True)

    is_editor = models.BooleanField(default=False)

    def __str__(self):

        return self.user.username
    
class Comment(models.Model):

    CONTENT_MAX_LENGTH = 2000

    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.CharField(max_length=CONTENT_MAX_LENGTH)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.content