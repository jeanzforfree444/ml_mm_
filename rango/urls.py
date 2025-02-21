from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/', views.ShowCategoryView.as_view(), name='show_category'),
    path('category/<slug:category_name_slug>/article/<slug:article_title_slug>/', views.ShowArticleView.as_view(), name='show_article'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_article/', views.AddArticleView.as_view(), name='add_article'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('like_article/', views.LikeArticleView.as_view(), name='like_article'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('mission_vision/', views.MissionVisionView.as_view(), name='mission_vision'),
    path('values/', views.ValuesView.as_view(), name='values'),
    path('stats/', views.StatsView.as_view(), name='show_stats'),
    path('forum/', views.ForumCategoryListView.as_view(), name='forum_category_list'),
    path('forum/add_forum_category/', views.AddForumCategoryView.as_view(), name='add_forum_category'),
    path('forum/<slug:forum_category_name_slug>/', views.ThreadListView.as_view(), name='forum_thread_list'),
    path('forum/<slug:forum_category_name_slug>/create/', views.CreateThreadView.as_view(), name='create_thread'),
    path('forum/<slug:forum_category_name_slug>/thread/<slug:thread_title_slug>/', views.ThreadDetailView.as_view(), name='forum_thread_detail'),
    path('forum/<slug:forum_category_name_slug>/thread/<slug:thread_title_slug>/poll/', views.PollVoteView.as_view(), name='poll_vote'),
    path('forum/<slug:forum_category_name_slug>/thread/<slug:thread_title_slug>/add_poll/', views.AddPollView.as_view(), name='add_poll'),
]