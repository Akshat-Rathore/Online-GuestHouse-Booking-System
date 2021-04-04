from django.contrib import admin
from django.urls import path
from django.urls import path, register_converter
from datetime import datetime
from .views import *


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('', hall_list, name='home'),
    path('details/<int:pk>', hall_details, name='details'),
    path('search/<int:gh_id>', search, name='search_room'),
    path('book/<int:gh_id>/', book_room, name='book_room'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('buffers/<yyyy:check_in_date>/<yyyy:check_out_date>/<int:booking_status>/',branching,name='buffer'),
    path('activate/<uidb64>/<token>',activate,name="activate"),
    path('dashboard/<int:pk>', dashboard, name='dashboard'),
    path('booking_history/<int:pk>', booking_history, name='booking_history'),
    path('edit_profile/<int:pk>/<int:cat>', edit_profile, name='edit_profile'),
    path('book/<int:pk>/<str:room_type>/<yyyy:check_in_date>/<yyyy:check_out_date>/<int:booking_status>',make_booking,name='book'),
    path('payment/<yyyy:check_in_date>/<yyyy:check_out_date>/', payment, name='payment'),
    path('feedback/<int:pk>/<int:userid>/',feedback,name='feedback'),
    path('cancel/<int:pk>/',cancel_booking,name='cancel'),
]