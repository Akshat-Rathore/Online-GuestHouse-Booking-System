from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import SearchForm, StudentForm, ProfessorForm, LoginForm, EditProfessorForm, EditStudentForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from .utils import token_generator
from django.utils.timezone import datetime
# Create your views here.

# displays all the guest houses in the home page
def hall_list(request):
    guest_house = GuestHouse.objects.all().values()
    count = GuestHouse.objects.all().count()
    data = []

    for i in range(count):
        data1 = []
        data1.append((i+1))
        house = get_object_or_404(GuestHouse, pk=(i+1))
        data1.append(house.name)
        data1.append(house.food_availability)
        data1.append(house.cost_of_food)
        data1.append(house.description)
        data.append(data1)

    print(data)
    context = {
        'data': data,
    }
    
    return render(request, 'OGHBS_APP/index.html', context)

def update_booking(gh_id):
    guest_house = GuestHouse.objects.get(pk=gh_id)
    if guest_house.last_update == datetime.date.today():
        print("OKAY")
    else:
        print("NOT-OKAY")
    return HttpResponse("<h1>HH</h1>")

# displays details of hall with id=pk

def hall_details(request, pk):
    guest_house = get_object_or_404(GuestHouse, pk=pk)
    
    guest_house1 = serializers.serialize('json', [guest_house])
    # return JsonResponse(json.loads(guest_house1), safe=False)
    context={
        'pk':pk,
        'Name':guest_house.name,
        "food":guest_house.food_availability,
        "cost_of_food":guest_house.cost_of_food,
        "address":guest_house.address,
        "description":guest_house.description,
        "ac_one_bednum":guest_house.AC1Bed.total_number,
        "ac_two_bednum":guest_house.AC2Bed.total_number,
        "ac_three_bednum":guest_house.AC3Bed.total_number,
        "ac_dor_bednum":guest_house.ACDormitory.total_number,
        "nonac_one_bednum":guest_house.NAC1Bed.total_number,
        "nonac_two_bednum":guest_house.NAC2Bed.total_number,
        "nonac_three_bednum":guest_house.NAC3Bed.total_number,
        "nonac_dor_bednum":guest_house.NACDormitory.total_number,
        "ac_one_bednum_cost":guest_house.AC1Bed.cost,
        "ac_two_bednum_cost":guest_house.AC2Bed.cost,
        "ac_three_bednum_cost":guest_house.AC3Bed.cost,
        "ac_dor_bednum_cost":guest_house.ACDormitory.cost,
        "nonac_one_bednum_cost":guest_house.NAC1Bed.cost,
        "nonac_two_bednum_cost":guest_house.NAC2Bed.cost,
        "nonac_three_bednum_cost":guest_house.NAC3Bed.cost,
        "nonac_dor_bednum_cost":guest_house.NACDormitory.cost,


    }
    return render(request, 'OGHBS_APP/guesthouse_details/index.html', context)

# Function to set the 'In-Queue' status of booking to 'Confirmed' if possible
def clear_queue():
    # Get all the queued bookings and order them by their ID (temporal ordering)
    queued_bookings = Booking.objects.filter(booking_status=1,check_in_date__gte=datetime.today()).order_by('pk')
    print("&&&")
    print(queued_bookings)
    # Check for each queued booking
    for booking in queued_bookings:
        if booking.room_type == 'AC 1 Bed':
            room_booking(booking, booking.guest_house.AC1Bed)
        elif booking.room_type == 'AC 2 Bed':
            room_booking(booking, booking.guest_house.AC2Bed)
        elif booking.room_type == 'AC 3 Bed':
            room_booking(booking, booking.guest_house.AC3Bed)
        elif booking.room_type == "NAC 1 Bed":
            room_booking(booking, booking.guest_house.NAC1Bed)
        elif booking.room_type == "NAC 2 Bed":
            room_booking(booking, booking.guest_house.NAC2Bed)
        elif booking.room_type == "NAC 3 Bed":
            room_booking(booking, booking.guest_house.NAC3Bed)
        elif booking.room_type == "ACDormitory":
            room_booking(booking, booking.guest_house.ACDormitory)
        else:
            room_booking(booking, booking.guest_house.NACDormitory)


def room_booking(booking, room):
    booked_room_ids = Booking.objects.filter(guest_house__id=booking.guest_house.id,
                                             room_type=booking.room_type,
                                             booking_status=0
                                             ).exclude(check_in_date__gt=booking.check_out_date
                                                       ).exclude(check_out_date__lt=booking.check_in_date
                                                                 ).order_by('room_id').values_list('room_id').distinct()

    booked_room_ids = [x[0] for x in booked_room_ids]
    start_id = room.initial_room_id
    end_id = room.initial_room_id + room.total_number - 1
    print(booked_room_ids)
    if len(booked_room_ids) == 0:
        booking.booking_status = 0
        booking.room_id = start_id
        booking.checked_out = 0
        booking.save()
    elif len(booked_room_ids) == room.total_number:
        booking.booking_status = 1
        booking.room_id = None
        booking.checked_out = 0
        booking.save()
    else:
        for _id in range(start_id, end_id+1):
            if _id not in booked_room_ids:
                booking.booking_status = 0
                booking.room_id = _id
                booking.checked_out = 0
                booking.save()
                return


def cancel_room_booking(booking):
    booking.booking_status = 3
    booking.checked_out = 0
    booking.save()
    clear_queue()


def check_availability(room, check_in, check_out, gh_id):
    booked_room_ids = Booking.objects.filter(guest_house__id=gh_id,
                                             room_type=room.room_type,
                                             booking_status=0
                                             ).exclude(check_in_date__gt=check_out
                                                       ).exclude(check_out_date__lt=check_in
                                                                 ).order_by('room_id').values_list('room_id').distinct()

    booked_room_ids = [x[0] for x in booked_room_ids]
    print(booked_room_ids, room.room_type)
    return room.total_number - len(booked_room_ids)


def search(request, gh_id):
    print(str(gh_id)+"ijk")
    print(request)
    guest_house = get_object_or_404(GuestHouse, pk=gh_id)
    if request.method == 'POST':
        print("****")
        print(request.POST)
        print(str(gh_id)+"ijk")
        form = SearchForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            guest_house = GuestHouse.objects.get(pk=gh_id)
            avl_rooms = dict()
            ast=[]
            avl_rooms['AC1Bed'] = check_availability(guest_house.AC1Bed, check_in, check_out, gh_id)
            ast.append(avl_rooms['AC1Bed'])
            avl_rooms['AC2Bed'] = check_availability(guest_house.AC2Bed, check_in, check_out, gh_id)
            ast.append(avl_rooms['AC2Bed'])
            avl_rooms['AC3Bed'] = check_availability(guest_house.AC3Bed, check_in, check_out, gh_id)
            ast.append(avl_rooms['AC3Bed'])
            avl_rooms['DorBed'] = check_availability(guest_house.ACDormitory, check_in, check_out, gh_id)
            ast.append(avl_rooms['DorBed'])
            avl_rooms['NAC1Bed'] = check_availability(guest_house.NAC1Bed, check_in, check_out, gh_id)
            ast.append(avl_rooms['NAC1Bed'])
            avl_rooms['NAC2Bed'] = check_availability(guest_house.NAC1Bed, check_in, check_out, gh_id)
            ast.append(avl_rooms['NAC2Bed'])
            avl_rooms['NAC3Bed'] = check_availability(guest_house.NAC3Bed, check_in, check_out, gh_id)
            ast.append(avl_rooms['NAC3Bed'])
            avl_rooms['NDorBed'] = check_availability(guest_house.NACDormitory, check_in, check_out, gh_id)
            ast.append(avl_rooms['NDorBed'])
            print("reaches")
            print(avl_rooms.items())
            context = {
                'form': form,
                'avl_rooms': avl_rooms,
                'ast': ast,
                'gh_id': gh_id,
                'name': guest_house.name,
                'desc':guest_house.description,
                "address":guest_house.address,
                "description":guest_house.description,
                "ac_one_bednum":guest_house.AC1Bed.total_number,
                "ac_two_bednum":guest_house.AC2Bed.total_number,
                "ac_three_bednum":guest_house.AC3Bed.total_number,
                "ac_dor_bednum":guest_house.ACDormitory.total_number,
                "nonac_one_bednum":guest_house.NAC1Bed.total_number,
                "nonac_two_bednum":guest_house.NAC2Bed.total_number,
                "nonac_three_bednum":guest_house.NAC3Bed.total_number,
                "nonac_dor_bednum":guest_house.NACDormitory.total_number,
                "ac_one_bednum_cost":guest_house.AC1Bed.cost,
                "ac_two_bednum_cost":guest_house.AC2Bed.cost,
                "ac_three_bednum_cost":guest_house.AC3Bed.cost,
                "ac_dor_bednum_cost":guest_house.ACDormitory.cost,
                "nonac_one_bednum_cost":guest_house.NAC1Bed.cost,
                "nonac_two_bednum_cost":guest_house.NAC2Bed.cost,
                "nonac_three_bednum_cost":guest_house.NAC3Bed.cost,
                "nonac_dor_bednum_cost":guest_house.NACDormitory.cost,
            }
            return render(request, 'OGHBS_APP/vacancies/index.html', context)

        context = {
            'form': form,
            'name': guest_house.name
        }
        return render(request, 'OGHBS_APP/search/index.html', context)
    else:
        form = SearchForm()
        context = {
            'form': form,
            'name': guest_house.name
        }
        return render(request, 'OGHBS_APP/search/index.html', context)

@login_required(login_url='login/')
def book_room(request, gh_id):
    print(request.GET)
    clear_queue()
    return HttpResponse("<h1>Hello {{gh_id}}+{{a}}</h1>")

def buffer(request,gh_id):
    context={
        'gh_id':gh_id,
        'flag':True
    }
    if request.user.is_authenticated:
        print(request.user)
        return render(request, 'OGHBS_APP/index.html', context)
        
    else:
        return render(request, 'OGHBS_APP/login/index.html', context)


def user_register(request):
    if request.method == 'POST':
        print(request.POST)
        roll_no = request.POST.get('roll_no', -1)
        password =request.POST.get('password1', -1)
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
                user.is_active=False
                user.save()

                uidb64= urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link=reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                email_subject = "[OGBS] : Activate your account"
                activate_url = "http://" +domain+link
                email_body = 'Hi' +user.username + "Click\n"+activate_url
                if category == 1:
                    cat = "Student"
                else:
                    cat = "Professor"
                message = render_to_string('OGHBS_APP/email/email_verify.html', {
                    'user': user,
                    'category': cat,
                    'password': password,
                    'domain': domain,
                    'uid': uidb64,
                    'token': token_generator.make_token(user),
                    })
                email = EmailMessage(
                                    email_subject,
                                    message,
                                    to=[user.email]
                    )
                email.content_subtype = "html"
                email.send(fail_silently=False)
                student = Student()
                student.full_name = form1.cleaned_data.get('full_name')
                student.department = form1.cleaned_data.get('department')
                student.roll_no = form1.cleaned_data.get('roll_no')
                student.user = user
                student.save()
                return redirect('login')

            return render(request, 'OGHBS_APP/register/index.html',
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
                user.is_active=False
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                email_subject = "[OGBS] : Activate your account"
                activate_url = "http://" +domain+link
                email_body = 'Hi ' +user.username+ " Click the following Link to activate your OGHBS\n"+activate_url
                email = EmailMessage(
                                    email_subject,
                                    email_body,
                                    to=[user.email]
                    )
                email.send(fail_silently=False)
                professor = Professor()
                professor.full_name = form2.cleaned_data.get('full_name')
                professor.department = form2.cleaned_data.get('department')
                professor.address = form2.cleaned_data.get('address')
                professor.user = user
                professor.save()
                return redirect('login')
            return render(request, 'OGHBS_APP/register/index.html',
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
        flag = True
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
           
            print("printed")
            return redirect('home')
        else:
            try:
                user1 = User.objects.get(username=user_name)
                if user1.is_active:
                    error_msg = "Username or password is incorrect"
                else:
                    error_msg = "Please verify your email first by visiting link given in verification mail."
                    flag = False
            except User.DoesNotExist:
                error_msg = "Username or password is incorrect"
            context = {
                'form': LoginForm(request.POST),
                'error': error_msg,
                'flag': flag
            }
            print(request.user)
            print("printed")
            return render(request, 'OGHBS_APP/login/index.html', context)
    else:
        form = LoginForm()
        return render(request, 'OGHBS_APP/login/index.html', {'form': form, 'flag':True})

@login_required(login_url='login/')
def user_logout(request):
    logout(request)
    return redirect('home')

# def halls_list(request):
#     return render(request, 'OGHBS_APP/guesthouse_details/index.html', {})


# view for activating accounts after email verification

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # user is activated if token from link is correct
    if user is not None and token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('login')
    # else error is returned
    else:
        context = {
            'form': LoginForm(),
            'error': "Verification Link is invalid",
            'flag': False
            }
        return render(request, 'OGHBS_APP/login/index.html', context)

def dashboard(request,pk):
    user = User.objects.get(pk=pk)
    num1=Student.objects.filter(user=user).count()
    num2=Professor.objects.filter(user=user).count()
    if(num1==1):
        stud=Student.objects.filter(user=user).first()
        category=0
        if stud is not None:
            dif=stud.roll_no
            full_name=stud.full_name
            department=stud.department
        else:
            dif=" "
            full_name=" "
            department=" "
        
    else:
        prof=Professor.objects.filter(user=user).first()
        category=1
        if prof is not None:
            dif=prof.address
            full_name=prof.full_name
            department=prof.department
        else:
            dif=" "
            full_name=" "
            department=" "
    context={
        'name':user.username,
        'fullname':full_name,
        'different':dif,
        'department':department,
        'password':user.password,
        'pk':pk,
        'category':category
    }
    return render(request, 'OGHBS_APP/dashboard/index.html', context)

def booking_history(request,pk):
    user=get_object_or_404(User, pk=pk)
    bookings = Booking.objects.filter(customer=user)
    count=Booking.objects.all().count()
    data=[]
    s=""
    s1=""
    s2=""
    feedback=[]
    for i in bookings:
        data1=[]
        if i.booking_status == 0:
            s="Confirmed"
        elif i.booking_status==1:
            s="queued"
        elif i.booking_status==2:
            s="refunded"
        else:
            s="cancelled"
        if i.payment_status==0:
            s1="No"
        else:
            s1="Yes"
        if i.food:
            s2="Yes"
        else:
            s2="No"
        # data1.append(i.pk)
        house = i.guest_house
        data1.append(house.name)
        data1.append(i.payment_status)
        data1.append(i.visitors_name)
        data1.append(s)
        data1.append(i.paid_amount)
        data1.append(i.room_id)
        data1.append(s2)
        data1.append(i.refund_amount)
        data1.append(str(i.check_in_date))
        data1.append(str(i.check_out_date))
        if i.feedback is not None:
            feedback.append(i.feedback.comfort_of_stay)
            feedback.append(i.feedback.room_cleanliness)
            feedback.append(i.feedback.service_quality)
            feedback.append(i.feedback.additional_feedback)
        else:
            feedback.append(" ")
            feedback.append(" ")
            feedback.append(" ")
            feedback.append(" ")
        data1.append(feedback)
        data1.append(str(i.check_in_date))
        data1.append(str(i.check_out_date))
        data.append(data1)
    context={
        'datas':data,
        'name': user.username,
    }
    return render(request, 'OGHBS_APP/booking_history/index.html', context)

def edit_profile(request,pk,cat):
    if request.method == 'POST':
        print(request.POST)
        password =request.POST.get('password1', -1)
        if cat == 0:
            form1 = EditStudentForm(request.POST)
            form2 = EditProfessorForm()
            if form1.is_valid():
                print(form1.cleaned_data)
                user =  get_object_or_404(User, pk=pk)
                # user.email = form1.cleaned_data.get('email')
                user.username = form1.cleaned_data.get('user_name')
                user.set_password(form1.cleaned_data.get('password1'))
                user.save()
                student = get_object_or_404(Student, user=user)
                student.full_name = form1.cleaned_data.get('full_name')
                student.department = form1.cleaned_data.get('department')
                student.roll_no = form1.cleaned_data.get('roll_no')
                student.user = user
                student.save()
                return redirect('dashboard',pk=pk)

            return render(request, 'OGHBS_APP/profile/index.html',
                          {'form1': form1, 'form2': form2, 'category': cat})
        else:
            form2 = EditProfessorForm(request.POST)
            form1 = EditStudentForm()
            if form2.is_valid():
                print(form2.cleaned_data)
                user = get_object_or_404(User, pk=pk)
                # user.email = form2.cleaned_data.get('email')
                user.username = form2.cleaned_data.get('user_name')
                user.set_password(form2.cleaned_data.get('password1'))
                user.save()
                professor = get_object_or_404(Professor, user=user)
                professor.full_name = form2.cleaned_data.get('full_name')
                professor.department = form2.cleaned_data.get('department')
                professor.address = form2.cleaned_data.get('address')
                professor.user = user
                professor.save()
                return redirect('dashboard',pk=pk)
            return render(request, 'OGHBS_APP/profile/index.html',
                          {'form1': form1, 'form2': form2, 'category': cat})

    elif request.method == 'GET':
        user=get_object_or_404(User, pk=pk)
        if cat==0:
            parentuser=get_object_or_404(Student, user=user)
        else:
            parentuser=get_object_or_404(Professor,user=user)
        context = {
            'form1': EditStudentForm(),
            'form2': EditProfessorForm(),
            'category': cat,
            'name':user.username,
            'full_name':parentuser.full_name,
            'email':user.email,
            'pk':pk

        }
    return render(request, 'OGHBS_APP/profile/index.html', context)