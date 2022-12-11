from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),            # wyświetla wszystkie publiczne posty [GET: all]
    path('post/<int:pk>', views.post_view),         # wyświetla post o danym id wraz z komentarzami [GET: all, PUT(comment): all, DELETE: author]
    path('post/<str:contains>', views.post_search), # wyświetla posty zawierające daną frazę [GET: all]
    path('post/<int:pk>/edit', views.post_edit),    # edycja posta o danym id [GET: author, PUT: author]
    path('profile', views.my_profile_view),                   # wyświetla profil zalogowanego użytkownika [GET: for users]
    path('profile/<int:pk>', views.profile_view_by_id),       # wyświetla profil użytkownika o danym id z jego publicznymi postami i komentarzami [GET: all (for owner get all posts)]
    path('profile/<str:name>', views.profile_view_by_string), # wyświetla profil użytkownika wyszukany po jego nazwie [GET: all]
    path('comment/<int:pk>', views.comments_view_by_id),                                # wyświetla komentarz o danym id [GET: all]
    path('post/<int:postID>/comment/<int:comID>', views.comment_of_the_post),           # wyświetla komentarz danego posta z listy posortowanej według daty utworzenia [GET: all, DELETE: comment_author, post_author]
    path('post/<int:postID>/comment/<str:contains>', views.comments_of_the_post_by_str), # wyświetla komentarze danego posta zawierającą daną frazę [GET: all]
    path('categories',views.category_view),             # wyświetla istniejące kategorie [GET: all]
    path('category/<int:id>',views.category_byId),      # wyświetla kategorie po id [GET: all]
    path('category/<str:cat>',views.category_byName),   # wyświetla kategorie po nazwie [GET: all]
]
