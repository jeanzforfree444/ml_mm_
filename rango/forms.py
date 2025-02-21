from django import forms
from rango.models import Article, Category, UserProfile, Comment, ForumCategory, Thread, Post, Poll, PollOption
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):

    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name:")

    description = forms.CharField(max_length=Category.DESCRIPTION_MAX_LENGTH, help_text="Please enter the category description:")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Category

        fields = ('name', 'description',)

class ArticleForm(forms.ModelForm):

    title = forms.CharField(max_length=Article.TITLE_MAX_LENGTH, help_text="Please enter the title of the article:")

    summary = forms.CharField(max_length=Article.SUMMARY_MAX_LENGTH, help_text="Please enter the summary of the article:")

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}), max_length=Article.CONTENT_MAX_LENGTH, help_text="Please enter the content of the article:")

    article_picture = forms.ImageField(required=True, help_text="Please upload an image for the article:")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    last_visit = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Article

        exclude = ('category', 'author',)
    
class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
              
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    is_editor = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    first_name = forms.CharField(max_length=UserProfile.NAME_MAX_LENGTH, required=True)

    last_name = forms.CharField(max_length=UserProfile.NAME_MAX_LENGTH, required=True)

    class Meta:

        model = UserProfile
        
        fields = ('first_name', 'last_name', 'website', 'profile_picture', 'is_editor',)

class CommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Comment.CONTENT_MAX_LENGTH, help_text="Please enter your comment:")

    class Meta:

        model = Comment

        exclude = ('article', 'user', 'date',)

class ForumCategoryForm(forms.ModelForm):

    name = forms.CharField(max_length=ForumCategory.NAME_MAX_LENGTH, help_text="Please enter the forum name:")

    description = forms.CharField(max_length=ForumCategory.DESCRIPTION_MAX_LENGTH, help_text="Please enter the forum description:")

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = ForumCategory

        fields = ('name', 'description',)

class ThreadForm(forms.ModelForm):

    title = forms.CharField(max_length=Thread.TITLE_MAX_LENGTH, help_text="Enter the title of your thread:")

    class Meta:

        model = Thread
        
        fields = ['title']

class PostForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Post.CONTENT_MAX_LENGTH, help_text="Enter your post:")

    class Meta:
        
        model = Post
        
        fields = ['content']

class PollForm(forms.ModelForm):

    question = forms.CharField(max_length=Poll.QUESTION_MAX_LENGTH, help_text="Enter the poll question:")

    class Meta:
    
        model = Poll
    
        fields = ['question']

class PollOptionForm(forms.ModelForm):

    option_text = forms.CharField(max_length=PollOption.OPTION_MAX_LENGTH, help_text="Enter an option for the poll:")

    class Meta:
        
        model = PollOption
        
        fields = ['option_text']