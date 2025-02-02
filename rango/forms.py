from django import forms
from rango.models import Article, Category, UserProfile, Comment
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):

    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name:")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Category

        fields = ('name',)

class ArticleForm(forms.ModelForm):

    title = forms.CharField(max_length=Article.TITLE_MAX_LENGTH, help_text="Please enter the title of the page:")

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}), max_length=Article.CONTENT_MAX_LENGTH, help_text="Please enter the content of the article:")

    article_picture = forms.ImageField(required=True, help_text="Please upload an image for the article:")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    last_visit = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Article

        exclude = ('category',)
    
class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
              
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    is_editor = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = UserProfile
        
        fields = ('website', 'profile_picture', 'is_editor',)

class CommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Comment.CONTENT_MAX_LENGTH, help_text="Please enter your comment:")

    class Meta:

        model = Comment

        exclude = ('article', 'user', 'date',)