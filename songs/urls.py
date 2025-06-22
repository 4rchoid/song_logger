from django.urls import path
from .views import *

urlpatterns = [
    path('songs/', get_all_songs, name='song-list'),
    path('song_by_title/', get_song_by_title, name='song-by-title'),
    path('rate_song/<str:id_song>/', rate_song, name='rate-song'),
]

