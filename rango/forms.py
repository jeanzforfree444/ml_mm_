from django import forms
from rango.models import Article, Category, UserProfile
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

    url = forms.URLField(max_length=Article.URL_MAX_LENGTH, help_text="Please enter the URL of the page:")

    content = forms.CharField(max_length=Article.CONTENT_MAX_LENGTH, help_text="Please enter the content of the article:")

    article_picture = forms.ImageField(required=True, help_text="Please upload an image for the article:")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Article

        exclude = ('category',)
    
    def clean(self):

        cleaned_data = self.cleaned_data

        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):

            url = f'http://{url}'

            cleaned_data['url'] = url
        
        return cleaned_data
    
class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
              
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile
        
        fields = ('website', 'profile_picture',)