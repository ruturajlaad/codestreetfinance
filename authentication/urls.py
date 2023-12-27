from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('activate/<uidb64>/<token>',views.activate,name="activate"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('contactus',views.contactus, name="constactus"),
    path('about',views.about, name="about"),
    path('webinar',views.webinar, name="webinar"),
    path('home',views.home, name="home"),
    #path('posts',views.posts, name="posts"),
    path('posts', views.list_of_articles, name='list_of_articles'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),

]