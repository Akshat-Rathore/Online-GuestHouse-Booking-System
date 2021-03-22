from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', hall_list, name='home'),
    path('details/<int:pk>', hall_details, name='details'),
    path('search/<int:gh_id>', search, name='search_room'),
    path('book/<int:gh_id>/', book_room, name='book_room'),
    path('register/', user_register, name = 'register'),
    path('login/', user_login, name = 'login')
]