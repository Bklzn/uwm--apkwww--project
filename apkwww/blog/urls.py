from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allposts', views.posts_all),
    path('post/<int:pk>', views.post_view),
    path('post/<str:contains>', views.post_search),
    path('profile', views.my_profile_view),
    path('profile/<int:pk>', views.profile_view_by_id),
    path('profile/<str:name>', views.profile_view_by_string),
]
