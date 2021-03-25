from django.contrib import admin
from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_delete


# Register your models here.
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Room)
admin.site.register(GuestHouse)
admin.site.register(Booking)
admin.site.register(Feedback)

@receiver(post_delete, sender=Student)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()

@receiver(post_delete, sender=Professor)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()
