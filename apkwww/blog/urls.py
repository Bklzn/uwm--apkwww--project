from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>', views.post_view),
    path('new_post', views.post_create),
    path('profile', views.profile_view),
]
