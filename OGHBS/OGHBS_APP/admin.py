from django.contrib import admin
from django.utils.html import format_html

from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .views import room_booking, cancel_room_booking
import datetime
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'roll_no', 'department']

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'department', 'address']

class AC1BedAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class AC2BedAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class AC3BedAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class NAC1BedAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class NAC2BedAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class NAC3BedAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class ACDormitoryAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class NACDormitoryAdmin(admin.ModelAdmin):
    list_display = ['view_guest_house', 'room_type', 'is_AC', 'capacity']
    readonly_fields = ['room_type', 'is_AC', 'capacity']

    def view_guest_house(self, obj):
        return obj.guesthouse

    view_guest_house.short_description = "Guest House"

class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'guest_house', 'room_type', 'room_id', 'check_in_date', 'check_out_date', 'booking_status']
    readonly_fields = ['room_id', 'booking_status', 'checked_out', "refund_amount"]
    admin.site.disable_action('delete_selected')
    list_filter = ("guest_house", "room_type", "room_id", "booking_status")

    def save_model(self, request, obj, form, change):
        if change:
            pass
            # print(form.changed_data)
            # if 'guest_house' in form.changed_data or 'room_type' in form.changed_data:
            # if obj.room_type == 'AC 1 Bed':
            #     room_booking(obj, obj.guest_house.AC1Bed)
            # elif obj.room_type == 'AC 2 Bed':
            #     room_booking(obj, obj.guest_house.AC2Bed)
            # elif obj.room_type == 'AC 3 Bed':
            #     room_booking(obj, obj.guest_house.AC3Bed)
        else:
            if obj.room_type == 'AC 1 Bed':
                room_booking(obj, obj.guest_house.AC1Bed)
            elif obj.room_type == 'AC 2 Bed':
                room_booking(obj, obj.guest_house.AC2Bed)
            elif obj.room_type == 'AC 3 Bed':
                room_booking(obj, obj.guest_house.AC3Bed)
        obj.save()

    def delete_model(self, request, obj):
        if obj.room_type == 'AC 1 Bed':
            cancel_room_booking(obj)
        elif obj.room_type == 'AC 2 Bed':
            cancel_room_booking(obj)
        elif obj.room_type == 'AC 3 Bed':
            cancel_room_booking(obj)


class GuestHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'food_availability', 'description', 'address', 'cost_of_food']


admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(AC1Bed, AC1BedAdmin)
admin.site.register(AC2Bed, AC2BedAdmin)
admin.site.register(AC3Bed, AC3BedAdmin)
admin.site.register(NAC1Bed, NAC1BedAdmin)
admin.site.register(NAC2Bed, NAC2BedAdmin)
admin.site.register(NAC3Bed, NAC3BedAdmin)
admin.site.register(ACDormitory, ACDormitoryAdmin)
admin.site.register(NACDormitory, NACDormitoryAdmin)
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
