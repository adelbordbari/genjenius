from django.urls import path
from .views import *
from uhf.views import follow

urlpatterns = [
    path('', homeView, name='home'),
    path('404/', fourohfourView, name='404'),
    path('contact/', contactView, name='contact'),

    path('meta/about/', aboutView, name='about'),
    path('meta/guidelines/', guidelinesView, name='guidelines'), #format, font, whitespace
    path('meta/coc/', cocView, name='coc'), #copyright, licensing, terms of use

    path('index/', indexView, name='index'),
    path('write/', writeView, name='write'),

    path('profile/', profileView, name='profile'),
    path('profile/<str:username>/', userProfileView, name='others_profile'),

    path('profile/followers/', followersView, name='followers'),
    path('profile/followers/<str:username>/', userFollowersView, name='others_followers'),

    path('profile/followings/', followingsView, name='followings'),
    path('profile/followings/<str:username>/', userFollowingsView, name='others_followings'),

    path('<str:username>/follow/<int:option>/', follow, name='follow'),#option0=follow

    path('post/<uuid:post_id>/', detailsView, name='post_details'),
    path('post/<uuid:post_id>/edit/', editPostView, name='edit_post'),
    path('post/<uuid:post_id>/delete/', deletePostView, name='delete_post'),

    path('post/<uuid:post_id>/like/', likeToggleView.as_view(), name='like_toggle'),

    path('tag/<str:tag_slug>/', tagsView, name='tags'),
    path('author/<str:author>/', authorView, name='author'),

    path('search/', searchView, name='search'),
    
    ]
