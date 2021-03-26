from django.contrib import admin
from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .views import AC2BedBooking, AC3BedBooking, AC1BedBooking, AC1CancelBooking, AC2CancelBooking, AC3CancelBooking
import datetime
from django.contrib import messages

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'roll_no', 'department']

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'department', 'address']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'guest_house', 'room_type', 'room_id', 'check_in_date', 'check_out_date', 'booking_status']
    # readonly_fields = ['room_id', 'booking_status', 'checked_out', ]

    def save_model(self, request, obj, form, change):
        if change:
            pass
            # print(form.changed_data)
            # if 'guest_house' in form.changed_data or 'room_type' in form.changed_data:
            #     if obj.room_type == 'AC 1 Bed':
            #         AC1BedBooking(obj)
            #     elif obj.room_type == 'AC 2 Bed':
            #         AC2BedBooking(obj)
            #     elif obj.room_type == 'AC 3 Bed':
            #         AC3BedBooking(obj)
        else:
            pass
            # if obj.room_type == 'AC 1 Bed':
            #     AC1BedBooking(obj)
            # elif obj.room_type == 'AC 2 Bed':
            #     AC2BedBooking(obj)
            # elif obj.room_type == 'AC 3 Bed':
            #     AC3BedBooking(obj)
        obj.save()

    def delete_model(self, request, obj):
        if obj.room_type == 'AC 1 Bed':
            AC1CancelBooking(obj)
        elif obj.room_type == 'AC 2 Bed':
            AC2CancelBooking(obj)
        elif obj.room_type == 'AC 3 Bed':
            AC3CancelBooking(obj)

class GuestHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'food_availability', 'description', 'address', 'cost_of_food']


admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Room)
admin.site.register(GuestHouse, GuestHouseAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Feedback)

@receiver(post_delete, sender=Student)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()

@receiver(post_delete, sender=Professor)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()
