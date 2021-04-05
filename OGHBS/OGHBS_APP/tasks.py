from celery import shared_task
from .models import GuestHouse, Booking, Room
from .views import clear_queue
from django.utils.timezone import datetime

# This is a scheduled task that's performed daily to free the rooms that are vacated on that day
@shared_task
def update_bookings():
    # Update booking status and refund for all past queued bookings
    wl_bookings = Booking.objects.filter(booking_status=1, check_in_date__lte=datetime.today())
    for booking in wl_bookings:
        booking.booking_status = 2
        # Calculate the refund amount
        booking.save()
    # For each guest house booking update is done
    # for guest_house in GuestHouse.objects.all():
    #     past_bookings = Booking.objects.filter(guest_house__id=guest_house.id, check_out_date__lte=datetime.today(), checked_out=1, booking_status=0)
    #     for booking in past_bookings:
    #         booking.checked_out =


    # Finally call the clear_queue() function to change the booking status of the queued bookings if possible
    clear_queue()


