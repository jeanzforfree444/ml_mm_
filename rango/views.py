from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rango.models import Category, Article, UserProfile, Comment
from rango.forms import CategoryForm, ArticleForm, UserProfileForm
from datetime import datetime
from rango.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone

class IndexView(View):

    def get(self, request):

        category_list = Category.objects.order_by('-likes')[:5]

        article_list = Article.objects.order_by('-views')[:5]

        context_dict = {}

        context_dict['categories'] = category_list

        context_dict['articles'] = article_list
        
        comments = Comment.objects.order_by('-date')[:5]

        context_dict['comments'] = comments
        
        visitor_cookie_handler(request)

        return render(request, 'rango/index.html', context=context_dict)

class AboutView(View):

    def get(self, request):

        context_dict = {}

        visitor_cookie_handler(request)

        context_dict['visits'] = request.session['visits']

        return render(request, 'rango/about.html', context_dict)

class ShowCategoryView(View):

    def create_context_dict(self, category_name_slug):

        context_dict = {}

        try:

            category = Category.objects.get(slug=category_name_slug)

            articles = Article.objects.filter(category=category).order_by('-views')

            context_dict['articles'] = articles

            context_dict['category'] = category

        except Category.DoesNotExist:

            context_dict['articles'] = None

            context_dict['category'] = None
        
        return context_dict
    
    def get(self, request, category_name_slug):

        context_dict = self.create_context_dict(category_name_slug)

        return render(request, 'rango/category.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):

        context_dict = self.create_context_dict(category_name_slug)

        query = request.POST['query'].strip()

        if query:

            context_dict['result_list'] = run_query(query)

            context_dict['query'] = query
        
        return render(request, 'rango/category.html', context_dict)
    
class ShowArticleView(View):

    def create_context_dict(self, category_name_slug, article_title_slug):

        context_dict = {}

        try:

            category = Category.objects.get(slug=category_name_slug)

            context_dict['category'] = category

            article = Article.objects.get(slug=article_title_slug)

            context_dict['article'] = article

        except Article.DoesNotExist:

            context_dict['article'] = None
        
        return context_dict

    def get(self, request, category_name_slug, article_title_slug):

        context_dict = self.create_context_dict(category_name_slug, article_title_slug)

        return render(request, 'rango/article.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug, article_title_slug):

        context_dict = self.create_context_dict(category_name_slug, article_title_slug)

        query = request.POST['query'].strip()

        if query:

            context_dict['result_list'] = run_query(query)

            context_dict['query'] = query
        
        return render(request, 'rango/article.html', context_dict)    

class AddCategoryView(View):

    @method_decorator(login_required)
    def get(self, request):

        form = CategoryForm()

        return render(request, 'rango/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('rango:index'))
        
        else:

            print(form.errors)
        
        return render(request, 'rango/add_category.html', {'form': form})

class AddArticleView(View):

    def get_category_name(self, category_name_slug):

        try:

            category = Category.objects.get(slug=category_name_slug)

        except Category.DoesNotExist:

            category = None
        
        return category
    
    @method_decorator(login_required)
    def get(self, request, category_name_slug):

        form = ArticleForm()

        category = self.get_category_name(category_name_slug)

        if category is None:

            return redirect(reverse('rango:index'))
        
        context_dict = {'form': form, 'category': category}

        return render(request, 'rango/add_article.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):

        form = ArticleForm(request.POST)

        category = self.get_category_name(category_name_slug)

        if category is None:

            return redirect(reverse('rango:index'))
        
        if form.is_valid():

            article = form.save(commit=True)

            article.category = category

            article.views = 0

            article.likes = 0

            article.save()

            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        
        else:

            print(form.errors)
        
        context_dict = {'form': form, 'category': category}

        return render(request, 'rango/add_article.html', context=context_dict)

class GotoView(View):

    def get(self, request):

        article_id = request.GET.get('article_id')

        try:

            selected_article = Article.objects.get(id=article_id)

        except Article.DoesNotExist:

            return redirect(reverse('rango:index'))

        selected_article.views = selected_article.views + 1

        selected_article.last_visit = timezone.now()

        selected_article.save()

        return redirect(selected_article.url)

class RegisterProfileView(View):

    @method_decorator(login_required)
    def get(self, request):

        form = UserProfileForm()

        context_dict = {'form': form}

        return render(request, 'rango/profile_registration.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request):

        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():

            user_profile = form.save(commit=False)

            user_profile.user = request.user

            user_profile.save()

            return redirect(reverse('rango:index'))
        
        else:
        
            print(form.errors)
        
        context_dict = {'form': form}
        
        return render(request, 'rango/profile_registration.html', context_dict)

class ProfileView(View):
    
    def get_user_details(self, username):
    
        try:
    
            user = User.objects.get(username=username)
    
        except User.DoesNotExist:
    
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
    
        form = UserProfileForm({'website': user_profile.website, 'profile_picture': user_profile.profile_picture})
        
        return (user, user_profile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):

        try:
        
            (user, user_profile, form) = self.get_user_details(username)
        
        except TypeError:
        
            return redirect(reverse('rango:index'))
        
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):

        try:

            (user, user_profile, form) = self.get_user_details(username)

        except TypeError:

            return redirect(reverse('rango:index'))
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('rango:profile', kwargs={'username': username}))
        
        else:
        
            print(form.errors)
        
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
        
        return render(request, 'rango/profile.html', context_dict)

class ListProfilesView(View):

    @method_decorator(login_required)
    def get(self, request):

        profiles = UserProfile.objects.all()

        return render(request, 'rango/list_profiles.html', {'user_profile_list': profiles})

def get_server_side_cookie(request, cookie, default_val=None):

    val = request.session.get(cookie)
    
    if not val:
    
        val = default_val
    
    return val

def visitor_cookie_handler(request):
    
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
    
        visits = visits + 1
    
        request.session['last_visit'] = str(datetime.now())
    
    else:
    
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

class LikeCategoryView(View):

    @method_decorator(login_required)
    def get(self, request):

        category_id = request.GET['category_id']

        try:

            category = Category.objects.get(id=int(category_id))

        except Category.DoesNotExist:

            return HttpResponse(-1)
        
        except ValueError:

            return HttpResponse(-1)
        
        category.likes = category.likes + 1

        category.save()

        return HttpResponse(category.likes)
    
class LikeArticleView(View):

    @method_decorator(login_required)
    def get(self, request):

        article_id = request.GET['article_id']

        try:

            article = Article.objects.get(id=int(article_id))

        except Article.DoesNotExist:

            return HttpResponse(-1)
        
        except ValueError:

            return HttpResponse(-1)
        
        article.likes = article.likes + 1

        article.save()

        return HttpResponse(article.likes)
    
def get_category_list(max_results=0, starts_with=''):

    category_list = []

    if starts_with:

        category_list = Category.objects.filter(name__istartswith=starts_with)
    
    if max_results > 0:

        if len(category_list) > max_results:

            category_list = category_list[:max_results]
    
    return category_list

class CategorySuggestionView(View):

    def get(self, request):

        if 'suggestion' in request.GET:

            suggestion = request.GET['suggestion']
        
        else:

            suggestion = ''

        category_list = get_category_list(max_results=8, starts_with=suggestion)

        if len(category_list) == 0:

            category_list = Category.objects.order_by('-likes')
        
        return render(request, 'rango/categories.html', {'categories': category_list})
    
class PrivacyView(View):

    def get(self, request):

        return render(request, 'rango/privacy.html')
    
class TermsView(View):  

    def get(self, request):

        return render(request, 'rango/terms.html')