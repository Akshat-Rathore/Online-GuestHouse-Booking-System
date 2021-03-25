from celery import shared_task
from .models import GuestHouse, Booking, Room
from .views import clear_queue
from django.utils.timezone import datetime

# This is a scheduled task that's performed daily to free the rooms that are vacated on that day
@shared_task
def update_bookings():
    # For each guest house booking update is done
    for guest_house in GuestHouse.objects.all():
        # Get all the past bookings that have
        # 1. check_out date < today
        # 2. guest house id of the current guest house
        # 3. bookings that aren't checkout out till yesterday
        # 4. The booking status should be confirmed
        past_bookings = Booking.objects.filter(guest_house__id=guest_house.id, check_out_date__lt=datetime.today(), checked_out=0, booking_status=0)
        print(guest_house, end='')
        print(past_bookings)
        for booking in past_bookings:
            # Check the type of room booking and update
            if booking.room_type == "AC 1 Bed":
                # The booking is checked out
                booking.checked_out = 1
                # Get the allotted room for this booking
                room = guest_house.AC1Bed
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                # Free this room i.e remove from booked_rooms for this type of room
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()

            elif booking.room_type == "AC 2 Bed":
                booking.checked_out = 1
                room = guest_house.AC2Bed
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()
                booking.save()
            elif booking.room_type == "AC 3 Bed":
                booking.checked_out = 1
                room = guest_house.AC3Bed
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()
                booking.save()
            elif booking.room_type == "NAC 1 Bed":
                booking.checked_out = 1
                room = guest_house.NAC1Bed
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()
                booking.save()
            elif booking.room_type == "NAC 2 Bed":
                booking.checked_out = 1
                room = guest_house.NAC2Bed
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()
                booking.save()
            elif booking.room_type == "NAC 3 Bed":
                booking.checked_out = 1
                room = guest_house.NAC3Bed
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()
                booking.save()
            elif booking.room_type == "ACDormitory":
                booking.checked_out = 1
                room = guest_house.ACDormitory
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()
                booking.save()
            else:
                booking.checked_out = 1
                room = guest_house.NACDormitory
                booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
                booked_rooms.remove(booking.room_id)
                if len(booked_rooms) == 0:
                    room.booked_rooms = None
                else:
                    room.booked_rooms = ','.join([str(x) for x in booked_rooms])
                room.save()
                guest_house.save()
                booking.save()
    # Finally call the clear_queue() function to change the booking status of the queued bookings if possible
    clear_queue()