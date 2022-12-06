from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>', views.post),
    path('new_post', views.new_post),
    path('profile', views.profile),
]
