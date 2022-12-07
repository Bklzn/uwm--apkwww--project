from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>', views.post_view),
    path('new_post', views.post_create),
    path('profile', views.my_profile_view),
    path('profile/<int:pk>', views.profile_view),
    path('post/delete=<int:pk>', views.post_delete),
    path('post/edit=<int:pk>', views.post_edit),
    path('comment/delete=<int:pk>', views.comment_delete)
]
