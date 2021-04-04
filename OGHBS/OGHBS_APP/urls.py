from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', hall_list, name='home'),
    path('details/<int:pk>', hall_details, name='details'),
    path('search/<int:gh_id>', search, name='search_room'),
    path('book/<int:gh_id>/', book_room, name='book_room'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('list/', halls_list, name='list'),
    path('buffer/<int:gh_id>/',buffer,name='buffer'),
    path('activate/<uidb64>/<token>',activate,name="activate"),
    path('dashboard/<int:pk>', dashboard, name='dashboard'),
    path('booking_history/<int:pk>', booking_history, name='booking_history'),
    path('edit_profile/<int:pk>/<int:cat>', edit_profile, name='edit_profile'),
]