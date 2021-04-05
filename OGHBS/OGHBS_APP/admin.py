from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.sites import AdminSite
from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .views import room_booking, cancel_room_booking, check_availability
import datetime
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class MyAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        bookings = Booking.objects.filter(date_of_booking=datetime.date.today())
        if bookings is not None:
            messages.info(request, mark_safe("New bookings are created today! Check them out <a href='OGHBS_APP/booking?q=today'>here</a>"))
        return super(MyAdminSite, self).index(request, extra_context)


my_admin_site = MyAdminSite(name='myadmin')

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

class MyForm(forms.ModelForm):
    def clean(self, *args, **kwargs):
        cleaned_data = super(MyForm, self).clean()
        if cleaned_data['check_in_date'] > cleaned_data['check_out_date']:
            raise ValidationError(_("Check out date can't be before check in date"))


class BookingAdmin(admin.ModelAdmin):
    form = MyForm
    list_display = ['customer', 'guest_house', "date_of_booking", 'room_type', 'room_id', 'check_in_date', 'check_out_date', 'booking_status']
    readonly_fields = ['room_id', 'booking_status', 'checked_out', "refund_amount", "date_of_booking"]
    # admin.site.disable_action('delete_selected')
    list_filter = ("guest_house", "date_of_booking", "room_type", "room_id", "booking_status")

    def get_queryset(self, request):
        qs = super(BookingAdmin, self).get_queryset(request)
        query = request.GET.get('q')
        if query is not None:
            return qs.filter(date_of_booking=datetime.date.today())
        return qs

    def save_model(self, request, obj, form, change):
        if change:
            if True:
                obj.save()
                return
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

    # def delete_model(self, request, obj):
    #     if obj.room_type == 'AC 1 Bed':
    #         cancel_room_booking(obj)
    #     elif obj.room_type == 'AC 2 Bed':
    #         cancel_room_booking(obj)
    #     elif obj.room_type == 'AC 3 Bed':
    #         cancel_room_booking(obj)


class GuestHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'food_availability', 'description', 'address', 'cost_of_food']


my_admin_site.register(Student, StudentAdmin)
my_admin_site.register(Professor, ProfessorAdmin)
my_admin_site.register(AC1Bed, AC1BedAdmin)
my_admin_site.register(AC2Bed, AC2BedAdmin)
my_admin_site.register(AC3Bed, AC3BedAdmin)
my_admin_site.register(NAC1Bed, NAC1BedAdmin)
my_admin_site.register(NAC2Bed, NAC2BedAdmin)
my_admin_site.register(NAC3Bed, NAC3BedAdmin)
my_admin_site.register(ACDormitory, ACDormitoryAdmin)
my_admin_site.register(NACDormitory, NACDormitoryAdmin)
my_admin_site.register(GuestHouse, GuestHouseAdmin)
my_admin_site.register(Booking, BookingAdmin)
my_admin_site.register(Feedback)
my_admin_site.register(User)

@receiver(post_delete, sender=Student)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()

@receiver(post_delete, sender=Professor)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()


