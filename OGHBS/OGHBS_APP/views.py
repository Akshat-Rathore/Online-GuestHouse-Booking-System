from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import SearchForm, StudentForm, ProfessorForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict

# Create your views here.


def hall_list(request):
    guest_house = GuestHouse.objects.all().values()
    guest_house = list(guest_house)
    # return JsonResponse(guest_house, safe=False)
    return render(request, 'OGHBS_APP/index.html', {})


def hall_details(request, pk):
    guest_house = get_object_or_404(GuestHouse, pk=pk)
    guest_house = serializers.serialize('json', [guest_house, ])
    return JsonResponse(json.loads(guest_house), safe=False)

# Function to set the 'In-Queue' status of booking to 'Confirmed' if possible
def clear_queue():
    # Get all the queued bookings and order them by their ID (temporal ordering)
    queued_bookings = Booking.objects.filter(booking_status=1).order_by('pk')
    print(queued_bookings)
    # Check for each queued booking
    for booking in queued_bookings:
        # For each booking in queued bookings get the list of confirmed bookings for which
        # 1. Room type, Hall type matches
        # 2. Exclude the bookings which have don't have any overlap with the timings of current booking
        confirmed_bookings = Booking.objects.filter(booking_status=0, room_type=booking.room_type, guest_house=booking.guest_house.pk).exclude(check_out_date__lt=booking.check_in_date).exclude(check_in_date__gt=booking.check_out_date)
        print(confirmed_bookings)

        # No confirmed bookings should overlap with the queued booking to make it confirmed
        if len(confirmed_bookings) == 0:
            if booking.room_type == 'AC 2 Bed':
                # Get the booked_rooms for the desired room in queued booking
                booked_rooms = booking.guest_house.AC2Bed.booked_rooms
                booked_rooms = [int(x) for x in booked_rooms.split(',')]
                room_start_id = booking.guest_house.AC2Bed.initial_room_id
                room_end_id = room_start_id + booking.guest_house.AC2Bed.total_number - 1
                # Case when all rooms of this type are booked => No confirmation possible
                if len(booked_rooms) == booking.guest_house.AC2Bed.total_number:
                    continue
                for i in range(room_start_id, room_end_id + 1):
                    # Get the smallest room no not present in the booked_rooms array (MEX)
                    if i != booked_rooms[i-room_start_id]:
                        booking.room_id = i
                        booked_rooms.insert(i-room_start_id, i)
                        # Update and save the booked_rooms string of the selected room type
                        booking.guest_house.AC2Bed.booked_rooms = ','.join([str(x) for x in booked_rooms])
                        booking.guest_house.AC2Bed.save()
                        booking.booking_status = 0
                        booking.save()
                        break
            elif booking.room_type == 'AC 3 Bed':
                booked_rooms = booking.guest_house.AC3Bed.booked_rooms
                booked_rooms = [int(x) for x in booked_rooms.split(',')]
                room_start_id = booking.guest_house.AC3Bed.initial_room_id
                room_end_id = room_start_id + booking.guest_house.AC3Bed.total_number - 1
                if len(booked_rooms) == booking.guest_house.AC3Bed.total_number:
                    continue
                for i in range(room_start_id, room_end_id + 1):
                    if i != booked_rooms[i - room_start_id]:
                        booking.room_id = i
                        booked_rooms.insert(i - room_start_id, i)
                        booking.guest_house.AC3Bed.booked_rooms = ','.join([str(x) for x in booked_rooms])
                        booking.guest_house.AC3Bed.save()
                        booking.booking_status = 0
                        booking.save()
                        break


def check_availability(room, check_in, check_out, gh_id):
    booked_rooms = [int(x) for x in room.booked_rooms.split(',')]
    count = 0
    if len(booked_rooms) == 0:
        count = room.total_number
    else:
        count = room.total_number - len(booked_rooms)
        for room_id in booked_rooms:
            bookings = Booking.objects.filter(room_id=room_id, guest_house=gh_id, booking_status=0)
            is_avl = True
            for booking in bookings:
                if not (booking.check_in_date > check_out or booking.check_out_date < check_in):
                    is_avl = False
            if is_avl:
                count += 1
    return count


def search(request, gh_id):
    print(gh_id)

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            guest_house = GuestHouse.objects.get(pk=gh_id)
            avl_rooms = dict()

            avl_rooms['AC2Bed'] = check_availability(guest_house.AC2Bed, check_in, check_out, gh_id)
            avl_rooms['AC3Bed'] = check_availability(guest_house.AC3Bed, check_in, check_out, gh_id)

            print(avl_rooms.items())
            context = {
                'form': form,
                'avl_rooms': avl_rooms,
                'gh_id': gh_id
            }
            return render(request, 'OGHBS_APP/searchform.html', context)

        context = {
            'form': form,
        }
        return render(request, 'OGHBS_APP/searchform.html', context)
    else:
        form = SearchForm()
        context = {
            'form': form,
        }
        return render(request, 'OGHBS_APP/searchform.html', context)


def book_room(request, gh_id):
    print(request.GET)
    clear_queue()
    return HttpResponse("<h1>Hello</h1>")

def user_register(request):
    if request.method == 'POST':
        print(request.POST)
        roll_no = request.POST.get('roll_no', -1)
        category = 1
        if roll_no == -1:
            category = 2
        if category == 1:
            form1 = StudentForm(request.POST)
            form2 = ProfessorForm()
            if form1.is_valid():
                print(form1.cleaned_data)
                user = User()
                user.email = form1.cleaned_data.get('email')
                user.username = form1.cleaned_data.get('user_name')
                user.set_password(form1.cleaned_data.get('password1'))
                user.save()
                student = Student()
                student.full_name = form1.cleaned_data.get('full_name')
                student.department = form1.cleaned_data.get('department')
                student.roll_no = form1.cleaned_data.get('roll_no')
                student.user = user
                student.save()
                return redirect('home')

            return render(request, 'OGHBS_APP/login/index.html',
                          {'form1': form1, 'form2': form2, 'category': category})
        else:
            form2 = ProfessorForm(request.POST)
            form1 = StudentForm()
            if form2.is_valid():
                print(form2.cleaned_data)
                user = User()
                user.email = form2.cleaned_data.get('email')
                user.username = form2.cleaned_data.get('user_name')
                user.set_password(form2.cleaned_data.get('password1'))
                user.save()
                professor = Professor()
                professor.full_name = form2.cleaned_data.get('full_name')
                professor.department = form2.cleaned_data.get('department')
                professor.address = form2.cleaned_data.get('address')
                professor.user = user
                professor.save()
                return redirect('home')
            return render(request, 'OGHBS_APP/login/index.html',
                          {'form1': form1, 'form2': form2, 'category': category})

    elif request.method == 'GET':
        context = {
            'form1': StudentForm(),
            'form2': ProfessorForm(),
            'category': 0
        }
        return render(request, 'OGHBS_APP/register/index.html', context)

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(request, username = user_name, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {
                'form': LoginForm(request.POST),
                'error': "Username or password is incorrect"
            }
            return render(request, 'OGHBS_APP/login/index.html', context)
    else:
        form = LoginForm()
        return render(request, 'OGHBS_APP/login/index.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')