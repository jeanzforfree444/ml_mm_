from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rango.models import Category, Article, UserProfile, Comment
from rango.forms import CategoryForm, ArticleForm, UserProfileForm, CommentForm
from datetime import datetime
from rango.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.utils.safestring import mark_safe
import json

BANNED_WORDS = [
    # Profanity & Swear Words
    "fuck", "shit", "damn", "bitch", "ass", "asshole", "bastard", "prick", "wanker",
    "bollocks", "dick", "cunt", "twat", "arse", "arsehole",

    # Sexually Explicit Terms
    "porn", "hentai", "blowjob", "anal", "dildo", "vibrator", "cum", "orgasm",
    "pussy", "deepthroat", "threesome", "gangbang", "incest", "sex", "shag", "fucking"

    # Violent & Threatening Language
    "kill yourself", "die", "murder you", "bomb", "terrorist", "execute",
    "massacre", "suicide", "genocide", "kill you", "murder", "gun", "shoot", "blood"

    # Hate Speech & Harassment
    "retard", "cripple", "faggot", "dyke", "tranny", "spastic", "gimp",
    "fag", "stupid", "idiot", "dumb",

    # Drug & Substance-Related Terms
    "weed", "cocaine", "heroin", "meth", "ecstasy", "lsd", "shrooms", 
    "ketamine", "overdose",

    # Self-Harm & Suicide References
    "cut myself", "end my life", "overdose", "slit my wrists", "i want to die", "kill myself", "kms",

    # Scam & Spam Words
    "free money", "click here", "earn cash", "work from home", "make millions",
    "hot singles", "win a prize"
]

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

        founder_profile = get_object_or_404(UserProfile, user__username='lee_mcq')
        
        context_dict['founder_profile'] = founder_profile

        developer_profile = get_object_or_404(UserProfile, user__username='janebirkin4life')

        context_dict['developer_profile'] = developer_profile

        designer_profile = get_object_or_404(UserProfile, user__username='dolcenogabbana')

        context_dict['designer_profile'] = designer_profile

        marketing_profile = get_object_or_404(UserProfile, user__username='gabbriette360')
        
        context_dict['marketing_profile'] = marketing_profile

        visitor_cookie_handler(request)

        context_dict['visits'] = request.session['visits']

        return render(request, 'rango/about.html', context_dict)

class ShowCategoryView(View):

    def create_context_dict(self, category_name_slug):

        context_dict = {}

        try:

            category = Category.objects.get(slug=category_name_slug)

            category.views += 1

            category.save()

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

            article.views += 1
            
            article.save()

            comments = Comment.objects.filter(article=article).order_by('-date')
            
            context_dict['comments'] = comments

        except Article.DoesNotExist:
            
            context_dict['article'] = None

        return context_dict

    def get(self, request, category_name_slug, article_title_slug):
        
        context_dict = self.create_context_dict(category_name_slug, article_title_slug)
        
        context_dict['form'] = CommentForm()
        
        return render(request, 'rango/article.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug, article_title_slug):
        
        context_dict = self.create_context_dict(category_name_slug, article_title_slug)

        form = CommentForm(request.POST)
        
        if form.is_valid():

            content = form.cleaned_data['content']

            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "Your comment contains innappropriate content and was not posted.")
        
            else:

                comment = form.save(commit=False)
            
                comment.article = context_dict['article']
            
                comment.user = request.user
            
                comment.save()

                messages.success(request, "Your comment as been posted successfully.")
        
            return redirect('rango:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)
        
        context_dict['form'] = form
        
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

        form = ArticleForm(request.POST, request.FILES)

        category = self.get_category_name(category_name_slug)

        if category is None:

            return redirect(reverse('rango:index'))
        
        if form.is_valid():

            article = form.save(commit=False)

            article.category = category

            article.views = 0

            article.likes = 0

            article.save()

            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        
        else:

            print(form.errors)
        
        context_dict = {'form': form, 'category': category}

        return render(request, 'rango/add_article.html', context=context_dict)

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

        category_list = Category.objects.filter(name__istartswith=starts_with).order_by('-views')

    else:
        
        category_list = Category.objects.order_by('name')
    
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

        category_list = get_category_list(max_results=5, starts_with=suggestion)

        if len(category_list) == 0:

            category_list = Category.objects.order_by('name')
        
        return render(request, 'rango/categories.html', {'categories': category_list})
    
class PrivacyView(View):

    def get(self, request):

        return render(request, 'rango/privacy.html')
    
class TermsView(View):  

    def get(self, request):

        return render(request, 'rango/terms.html')
    
class MissionVisionView(View):
    
    def get(self, request):

        return render(request, 'rango/mission_vision.html')

class ValuesView(View):

    def get(self, request):

        return render(request, 'rango/values.html')
    
class StatsView(View):
    
    @method_decorator(login_required)
    def get(self, request):

        context_dict = {}
        
        if not request.user.userprofile.is_editor:

            return redirect(reverse('rango:index'))
        
        total_cats = Category.objects.count()

        context_dict['total_cats'] = total_cats
        
        total_articles = Article.objects.count()

        context_dict['total_articles'] = total_articles

        total_comments = Comment.objects.count()

        context_dict['total_comments'] = total_comments

        total_users = User.objects.count()

        context_dict['total_users'] = total_users

        total_likes = 0

        total_views = 0

        for article in Article.objects.all():

            total_likes += article.likes

            total_views += article.views

        context_dict['total_likes'] = total_likes

        context_dict['total_views'] = total_views

        category_stats = {}
        
        category_likes = []
        
        category_views = []
        
        category_names = []
        
        for category in Category.objects.all():
        
            category_likes_sum = 0
        
            category_views_sum = 0
        
            for article in category.article_set.all():
        
                category_likes_sum += article.likes
        
                category_views_sum += article.views
            
            category_stats[category.name] = {'likes': category_likes_sum, 'views': category_views_sum}

            category_names.append(category.name)
        
            category_likes.append(category_likes_sum)
        
            category_views.append(category_views_sum)

        context_dict['category_stats'] = category_stats

        context_dict['category_likes'] = mark_safe(json.dumps(category_likes))
        
        context_dict['category_views'] = mark_safe(json.dumps(category_views))
        
        context_dict['category_names'] = mark_safe(json.dumps(category_names))

        return render(request, 'rango/stats.html', context_dict)