from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Room)
admin.site.register(GuestHouse)
admin.site.register(Booking)
admin.site.register(Feedback)