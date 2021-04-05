from OGHBS_APP.models import *
from OGHBS_APP.views import *
from OGHBS_APP.forms import *
from django.test import TestCase
import datetime
from django.urls import reverse
from django.core.exceptions import ValidationError
import json 
class SearchTest(TestCase):

    def setUp(self):
        # Create a Guest House
        self.ac1bed = AC1Bed.objects.create(
            total_number=2,
            cost=500,
            initial_room_id=1,
        )
        self.ac1bed.save()

        self.ac2bed = AC2Bed.objects.create(
            total_number=2,
            cost=1000,
            initial_room_id=3,
        )

        self.ac2bed.save()

        self.ac3bed = AC3Bed.objects.create(
            total_number=2,
            cost=1500,
            initial_room_id=5,
        )

        self.ac3bed.save()
        self.nac1bed = NAC1Bed.objects.create(
            total_number=2,
            cost=250,
            initial_room_id=7,
        )
        self.nac1bed.save()
        
        self.nacdormitory = NACDormitory.objects.create(total_number=2, cost=50,initial_room_id=15)
        self.nacdormitory.save()
        self.acdormitory = ACDormitory.objects.create(total_number=2, cost=80,initial_room_id=13)
        self.acdormitory.save()
        self.nac3bed = NAC3Bed.objects.create(total_number=2, cost=150,initial_room_id=11)
        self.nac3bed.save()
        self.nac2bed = NAC2Bed.objects.create(total_number=2, cost=50,initial_room_id=9)
        self.nac2bed.save()

        self.gh = GuestHouse()
        self.gh.name = "test guest house"
        self.gh.food_availability = 1
        self.gh.cost_of_food = 500
        self.gh.address = "IIT Kharagpur/Kharagpur"
        self.gh.description = "The guest house of your dream"
        self.gh.AC1Bed = self.ac1bed
        self.gh.AC2Bed = self.ac2bed
        self.gh.AC3Bed = self.ac3bed
        self.gh.NAC1Bed = self.nac1bed
        self.gh.NAC2Bed = self.nac2bed
        self.gh.NAC3Bed = self.nac3bed
        self.gh.ACDormitory = self.acdormitory
        self.gh.NACDormitory = self.nacdormitory
        self.gh.save()
        
        self.test_user1 = User.objects.create(
            username='Ani',
            password='ABCDEFGH'
        )
        
        self.test_user1.save()
        self.test_user2 = User.objects.create(
            username='Ani01',
            password='ABCDEFGH'
        )
        self.test_user2.save()

    def test_search_date_in_the_past(self):
        check_in_date1 = datetime.date(2021, 4, 1) 
        check_out_date1 = datetime.date(2021, 4, 3)
        response = self.client.post(reverse('search_room', kwargs={'gh_id': self.gh.pk}), {'check_in_date': check_in_date1,'check_out_date':check_out_date1})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'check_in_date', 'Invalid date - Check-in date cannot be in the past')


    def test_search_check_in_date_ahead_of_check_out_date(self):
        check_in_date2 = datetime.date(2021, 4, 8)
        check_out_date2 = datetime.date(2021, 4, 6)
        sform = SearchForm({
            'check_in_date':check_in_date2,
            'check_out_date':check_out_date2
        })
        self.assertIsInstance(
            sform.errors.as_data()['__all__'][0],
            ValidationError
        )
        self.assertEquals(
            sform.errors['__all__'][0],
            'Invalid date - Check-out date cannot be before Check-in Date'
        )

    def test_search_valid_input_1(self):
        check_in_date = datetime.date(2021, 4, 8)
        check_out_date = datetime.date(2021, 4, 10)
        response = self.client.post(reverse('search_room', kwargs={'gh_id': self.gh.pk}), {'check_in_date': check_in_date,'check_out_date':check_out_date})
        self.assertEqual(response.status_code, 200)
        vacancies = [2,2,2,2,2,2,2,2]
        


    def test_search_valid_input_2(self):
        # Create two bookings for AC1 bed and One booking for AC2 Bed
        b1 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 8),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "Anindya",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        b1.save()
        room_booking(b1, self.ac1bed)

        b3 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 9),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "Akshat",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        b3.save()
        room_booking(b3, self.ac1bed)

        b2 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 2 Bed',
            check_in_date = datetime.date(2021, 4, 6),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "KD",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        b2.save()
        room_booking(b2, self.ac2bed)

        check_in_date = datetime.date(2021, 4, 8)
        check_out_date = datetime.date(2021, 4, 10)
        response = self.client.post(reverse('search_room', kwargs={'gh_id': self.gh.pk}), {'check_in_date': check_in_date,'check_out_date':check_out_date})
        self.assertEqual(response.status_code, 200)

        # Golder O/P
        vacancies = [0,1,2,2,2,2,2,2]
        for i in range(8):
            self.assertEqual(vacancies[i], response.context['ast'][i])

class RoomBookingTest(TestCase):

    def setUp(self):
        # Create a Guest House
        self.ac1bed = AC1Bed.objects.create(
            total_number=2,
            cost=500,
            initial_room_id=1,
        )
        self.ac1bed.save()

        self.ac2bed = AC2Bed.objects.create(
            total_number=2,
            cost=1000,
            initial_room_id=3,
        )

        self.ac2bed.save()

        self.ac3bed = AC3Bed.objects.create(
            total_number=2,
            cost=1500,
            initial_room_id=5,
        )

        self.ac3bed.save()
        self.nac1bed = NAC1Bed.objects.create(
            total_number=2,
            cost=250,
            initial_room_id=7,
        )
        self.nac1bed.save()
        
        self.nacdormitory = NACDormitory.objects.create(total_number=2, cost=50,initial_room_id=15)
        self.nacdormitory.save()
        self.acdormitory = ACDormitory.objects.create(total_number=2, cost=80,initial_room_id=13)
        self.acdormitory.save()
        self.nac3bed = NAC3Bed.objects.create(total_number=2, cost=150,initial_room_id=11)
        self.nac3bed.save()
        self.nac2bed = NAC2Bed.objects.create(total_number=2, cost=50,initial_room_id=9)
        self.nac2bed.save()

        self.gh = GuestHouse()
        self.gh.name = "test guest house"
        self.gh.food_availability = 1
        self.gh.cost_of_food = 500
        self.gh.address = "IIT Kharagpur/Kharagpur"
        self.gh.description = "The guest house of your dream"
        self.gh.AC1Bed = self.ac1bed
        self.gh.AC2Bed = self.ac2bed
        self.gh.AC3Bed = self.ac3bed
        self.gh.NAC1Bed = self.nac1bed
        self.gh.NAC2Bed = self.nac2bed
        self.gh.NAC3Bed = self.nac3bed
        self.gh.ACDormitory = self.acdormitory
        self.gh.NACDormitory = self.nacdormitory
        self.gh.save()
        
        self.test_user1 = User.objects.create(
            username='Ani',
            password='ABCDEFGH'
        )
        
        self.test_user1.save()
        self.test_user2 = User.objects.create(
            username='Ani01',
            password='ABCDEFGH'
        )
        self.test_user2.save()

    def test_booking(self):
        b1 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 8),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "Anindya",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        b1.save()
        room_booking(b1, self.ac1bed)

        b2 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 10),
            check_out_date = datetime.date(2021, 4, 12),
            visitors_count = 1,
            visitors_name = "KD",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        b2.save()
        room_booking(b2, self.ac1bed)

        b3 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 9),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "Akshat",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        b3.save()
        room_booking(b3, self.ac1bed)

        b4 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 8),
            check_out_date = datetime.date(2021, 4, 12),
            visitors_count = 1,
            visitors_name = "KD",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        b4.save()
        room_booking(b4, self.ac1bed)

        # b1,b2 and b3 all should get confirmed but b4 should be in queue
        self.assertEqual(b1.booking_status,0)
        self.assertEqual(b1.room_id,1)
        self.assertEqual(b3.booking_status,0)
        self.assertEqual(b3.room_id,2)
        self.assertEqual(b2.booking_status,0)
        self.assertEqual(b3.room_id,None)
        self.assertEqual(b4.booking_status,1)
        self.assertEqual(b3.room_id,None)

class CancelRoomBookingTest(TestCase):

    def setUp(self):
        # Create a Guest House
        self.ac1bed = AC1Bed.objects.create(
            total_number=2,
            cost=500,
            initial_room_id=1,
        )
        self.ac1bed.save()

        self.ac2bed = AC2Bed.objects.create(
            total_number=2,
            cost=1000,
            initial_room_id=3,
        )

        self.ac2bed.save()

        self.ac3bed = AC3Bed.objects.create(
            total_number=2,
            cost=1500,
            initial_room_id=5,
        )

        self.ac3bed.save()
        self.nac1bed = NAC1Bed.objects.create(
            total_number=2,
            cost=250,
            initial_room_id=7,
        )
        self.nac1bed.save()
        
        self.nacdormitory = NACDormitory.objects.create(total_number=2, cost=50,initial_room_id=15)
        self.nacdormitory.save()
        self.acdormitory = ACDormitory.objects.create(total_number=2, cost=80,initial_room_id=13)
        self.acdormitory.save()
        self.nac3bed = NAC3Bed.objects.create(total_number=2, cost=150,initial_room_id=11)
        self.nac3bed.save()
        self.nac2bed = NAC2Bed.objects.create(total_number=2, cost=50,initial_room_id=9)
        self.nac2bed.save()

        self.gh = GuestHouse()
        self.gh.name = "test guest house"
        self.gh.food_availability = 1
        self.gh.cost_of_food = 500
        self.gh.address = "IIT Kharagpur/Kharagpur"
        self.gh.description = "The guest house of your dream"
        self.gh.AC1Bed = self.ac1bed
        self.gh.AC2Bed = self.ac2bed
        self.gh.AC3Bed = self.ac3bed
        self.gh.NAC1Bed = self.nac1bed
        self.gh.NAC2Bed = self.nac2bed
        self.gh.NAC3Bed = self.nac3bed
        self.gh.ACDormitory = self.acdormitory
        self.gh.NACDormitory = self.nacdormitory
        self.gh.save()
        
        self.test_user1 = User.objects.create(
            username='Ani',
            password='ABCDEFGH'
        )
        
        self.test_user1.save()
        self.test_user2 = User.objects.create(
            username='Ani01',
            password='ABCDEFGH'
        )
        self.test_user2.save()

        self.b1 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 8),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "Anindya",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        self.b1.save()
        room_booking(self.b1, self.ac1bed)

        self.b2 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 9),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "KD",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        self.b2.save()
        room_booking(self.b2, self.ac1bed)

        self.b3 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 6),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "Akshat",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        self.b3.save()
        room_booking(self.b3, self.ac1bed)

        self.b4 = Booking.objects.create(
            guest_house=self.gh,
            customer=self.test_user1,
            room_type = 'AC 1 Bed',
            check_in_date = datetime.date(2021, 4, 7),
            check_out_date = datetime.date(2021, 4, 10),
            visitors_count = 1,
            visitors_name = "KD",
            payment_status = 1,
            booking_status = 1,
            paid_amount = 1000,
            food = 1,
            checked_out = 0,
        )
        self.b4.save()
        room_booking(self.b4, self.ac1bed)
    
    def test_cancel_room_booking(self):
        cancel_room_booking(self.b1)
        self.assertEqual(self.b1.booking_status,3)
        self.assertEqual(self.b2.booking_status,0)

        # b3 should have confirmed status now and b4 should not get confirmed
        # as b3 was done before b4 (priority wrt date of booking)
        self.b3 = Booking.objects.get(pk=self.b3.pk)
        self.b4 = Booking.objects.get(pk=self.b4.pk)
        self.assertEqual(self.b3.booking_status,'0')
        self.assertEqual(self.b4.booking_status,'1')

class HallListTest(TestCase):

    def setup(self):
        ac1bed = AC1Bed.objects.create(
            total_number=2,
            cost=500,
            initial_room_id=1,
        )

        ac2bed = AC2Bed.objects.create(
            total_number=2,
            cost=1000,
            initial_room_id=3,
        )

        ac3bed = AC3Bed.objects.create(
            total_number=2,
            cost=1500,
            initial_room_id=5,
        )

        nac1bed = NAC1Bed.objects.create(
            total_number=2,
            cost=250,
            initial_room_id=7,
        )
        
        
        nacdormitory = NACDormitory.objects.create(total_number=2, cost=50,initial_room_id=15)
        acdormitory = ACDormitory.objects.create(total_number=2, cost=80,initial_room_id=13)
        nac3bed = NAC3Bed.objects.create(total_number=2, cost=150,initial_room_id=11)
        nac2bed = NAC2Bed.objects.create(total_number=2, cost=100,initial_room_id=9)

        self.gh = GuestHouse()
        self.gh.name = "test guest house"
        self.gh.food_availability = 1
        self.gh.cost_of_food = 500
        self.gh.address = "IIT Kharagpur/Kharagpur"
        self.gh.description = "The guest house of your dream"
        self.gh.AC1Bed = ac1bed
        self.gh.AC2Bed = ac2bed
        self.gh.AC3Bed = ac3bed
        self.gh.NAC1Bed = nac1bed
        self.gh.NAC2Bed=nac2bed
        self.gh.NAC3Bed=nac3bed
        self.gh.ACDormitory=acdormitory
        self.gh.NACDormitory=nacdormitory
        self.gh.save()
        # print(self.gh)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'OGHBS_APP/index.html')

    def test_lists_all_guesthouses(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('data' in response.context)
        # print(response.context['data'])
        # self.assertEqual(response.context['data'],None)

class HallDetailsTest(TestCase):
    def setUp(self):
        ac1bed = AC1Bed.objects.create(
            total_number=2,
            cost=500,
            initial_room_id=1,
        )

        ac2bed = AC2Bed.objects.create(
            total_number=2,
            cost=1000,
            initial_room_id=3,
        )

        ac3bed = AC3Bed.objects.create(
            total_number=2,
            cost=1500,
            initial_room_id=5,
        )

        nac1bed = NAC1Bed.objects.create(
            total_number=2,
            cost=250,
            initial_room_id=7,
        )
        
        
        nacdormitory = NACDormitory.objects.create(total_number=2, cost=50,initial_room_id=15)
        acdormitory = ACDormitory.objects.create(total_number=2, cost=80,initial_room_id=13)
        nac3bed = NAC3Bed.objects.create(total_number=2, cost=150,initial_room_id=11)
        nac2bed = NAC2Bed.objects.create(total_number=2, cost=100,initial_room_id=9)
        self.ac1bed=ac1bed
        self.gh1 = GuestHouse()
        self.gh1.name = "test guest house"
        self.gh1.food_availability = 1
        self.gh1.cost_of_food = 500
        self.gh1.address = "IIT Kharagpur/Kharagpur"
        self.gh1.description = "The guest house of your dream"
        self.gh1.AC1Bed = ac1bed
        self.gh1.AC2Bed = ac2bed
        self.gh1.AC3Bed = ac3bed
        self.gh1.NAC1Bed = nac1bed
        self.gh1.NAC2Bed=nac2bed
        self.gh1.NAC3Bed=nac3bed
        self.gh1.ACDormitory=acdormitory
        self.gh1.NACDormitory=nacdormitory
        self.gh1.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('details/1/')
        # print(self.gh1.pk)
        self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('details', kwargs={'pk': self.gh1.pk}))
       
        # print("response")
        # print(response)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('details', kwargs={'pk': self.gh1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'OGHBS_APP/guesthouse_details/index.html')

    def test_context_all(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('details', kwargs={'pk': self.gh1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('pk' in response.context)
        self.assertTrue('Name' in response.context)
        self.assertEqual(response.context['Name'],'test guest house')
        self.assertTrue('food' in response.context)
        self.assertEqual(response.context['food'],True)
        self.assertTrue('cost_of_food' in response.context)
        self.assertEqual(response.context['cost_of_food'],500)
        self.assertTrue('address' in response.context)
        self.assertEqual(response.context['address'],"IIT Kharagpur/Kharagpur")
        self.assertTrue('description' in response.context)
        self.assertEqual(response.context['description'],"The guest house of your dream")
        self.assertTrue('ac_one_bednum_cost' in response.context)
        self.assertEqual(response.context['ac_one_bednum_cost'],self.ac1bed.cost)
        
class DashboardTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        self.test_user1.save()
        self.test_user2.save()
        
        self.student=Student.objects.create(
            user=self.test_user1,
            full_name="Test User1",
            roll_no="19XXABCDE",
            department="XX"
        )
        self.student.save()
        self.professor=Professor.objects.create(
            user=self.test_user2,
            full_name="Test User2",
            department="XX",
            address="IIT-kgp/somewhere"
        )
        self.professor.save()
    
    def test_logged_in_uses_correct_template_and_category(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('dashboard', kwargs={'pk': self.test_user1.pk}))
        # Check our user is logged in
        self.assertEqual(str(response.context['name']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'OGHBS_APP/dashboard/index.html')
        #check category
        self.assertEqual(response.context['different'],self.student.roll_no)

        login_professor = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('dashboard', kwargs={'pk': self.test_user2.pk}))
        # Check our user is logged in
        self.assertEqual(str(response.context['name']), 'testuser2')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'OGHBS_APP/dashboard/index.html')
        #check category
        self.assertEqual(response.context['different'],self.professor.address)

class BookingHistoryTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        self.student=Student.objects.create(
            user=test_user1,
            full_name="Test User1",
            roll_no="19XXABCDE",
            department="XX"
        )
        self.student.save()

        ac1bed = AC1Bed.objects.create(total_number=2,cost=500,initial_room_id=1)
        ac2bed = AC2Bed.objects.create(total_number=2,cost=1000,initial_room_id=3,)
        ac3bed = AC3Bed.objects.create(total_number=2,cost=1500,initial_room_id=5,)
        nac1bed = NAC1Bed.objects.create(total_number=2,cost=250,initial_room_id=7,)
        nacdormitory = NACDormitory.objects.create(total_number=2, cost=50,initial_room_id=15)
        acdormitory = ACDormitory.objects.create(total_number=2, cost=80,initial_room_id=13)
        nac3bed = NAC3Bed.objects.create(total_number=2, cost=150,initial_room_id=11)
        nac2bed = NAC2Bed.objects.create(total_number=2, cost=100,initial_room_id=9)
        self.ac1bed=ac1bed
        self.gh1 = GuestHouse()
        self.gh1.name = "test guest house"
        self.gh1.food_availability = 1
        self.gh1.cost_of_food = 500
        self.gh1.address = "IIT Kharagpur/Kharagpur"
        self.gh1.description = "The guest house of your dream"
        self.gh1.AC1Bed = ac1bed
        self.gh1.AC2Bed = ac2bed
        self.gh1.AC3Bed = ac3bed
        self.gh1.NAC1Bed = nac1bed
        self.gh1.NAC2Bed=nac2bed
        self.gh1.NAC3Bed=nac3bed
        self.gh1.ACDormitory=acdormitory
        self.gh1.NACDormitory=nacdormitory
        self.gh1.save()
        number_of_bookings=5
        self.booking=[]
        visitors_name=" "
        for i in range(number_of_bookings):
            visitors_count=i%3+1
            for j in range(visitors_count):
                visitors_name+="Visitor"+str(i)
                if j !=(visitors_count-1):
                    visitors_name+=","
            booking_status=""
            if(i%4==0):
                booking_status="COnfirmed"
            elif i%4==1:
                booking_status="In-Queue"
            elif i%4==2:
                booking_status="Refund"
            else:
                booking_status="Cancelled"
            check_in_date = datetime.date(2020, 4, i+1)
            check_out_date = datetime.date(2020, 5, i+1)
            booking=Booking.objects.create(
                guest_house=self.gh1,
                customer=test_user1,
                room_type="AC 3 Bed",
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                visitors_count=visitors_count,
                visitors_name=visitors_name,
                payment_status=i%2,
                booking_status=booking_status,
                paid_amount=0,
                refund_amount=0,
                feedback=None,
                date_of_booking=datetime.date.today
                )
            booking.save()
            self.booking.append(booking)
    
    def test_logged_in_uses_correct_template(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('booking_history', kwargs={'pk': self.student.pk}))
        # Check our user is logged in
        self.assertEqual(str(response.context['name']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'OGHBS_APP/booking_history/index.html')
        
    def test_context(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('booking_history', kwargs={'pk': self.student.pk}))
        self.assertEqual(len(response.context['datas']), 5)
        self.assertEqual(response.context['datas'][0][0],"test guest house")

class EditProfileTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        self.test_user1.save()
        self.test_user2.save()
        
        self.student=Student.objects.create(
            user=self.test_user1,
            full_name="Test User1",
            roll_no="19XXABCDE",
            department="XX"
        )
        self.student.save()
        self.professor=Professor.objects.create(
            user=self.test_user2,
            full_name="Test User2",
            department="XX",
            address="IIT-kgp/somewhere"
        )
        self.professor.save()
    
    def test_logged_in_uses_correct_template(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_profile', kwargs={'pk': self.test_user1.pk, 'cat':0}))
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'OGHBS_APP/profile/index.html')
        # Check we used correct template
        self.assertTemplateUsed(response, 'OGHBS_APP/profile/index.html')
        login_professor = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('edit_profile', kwargs={'pk': self.test_user2.pk, 'cat':1}))
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'OGHBS_APP/profile/index.html')
        
    def test_error_statemants(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_profile', kwargs={'pk': self.test_user1.pk, 'cat':0}))
        pass1="1X<ISRUkw+tuK"
        repeat_pass1="1X<ISRUkw+tuK_diff"
        # sform = EditStudentForm({
        #     'password1':pass1,
        #     'password2':repeat_pass1
        # })
        # self.assertIsInstance(
        #     sform.errors.as_data()['__all__'][0],
        #     ValidationError
        # )
        # self.assertEquals(
        #     sform.errors['__all__'][0],
        #     "Password and Confirm Password don't match with each other"
        # )
        # login_professor = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        # response = self.client.get(reverse('edit_profile', kwargs={'pk': self.test_user2.pk, 'cat':1}))
        # pass1="1X<ISRUkw+tuK"
        # repeat_pass1="1X<ISRUkw+tuK_diff"
        # pform = EditProfessorForm({
        #     'password1':pass1,
        #     'password2':repeat_pass1
        # })
        # # print(pform.errors)
        # self.assertIsInstance(
        #     pform.errors.as_data()['__all__'][0],
        #     ValidationError
        # )
        # self.assertEquals(
        #     pform.errors['__all__'][0],
        #     "Password and Confirm Password don't match with each other"
        # )
        response = self.client.post(reverse('edit_profile', kwargs={'pk': self.test_user2.pk, 'cat':1}), {
            
            'full_name':'full_name',
            'department':'full_name',
            'address':'address',
            
        })

        # self.assertFormError(response, 'form2', 'user_name', 'Username is already taken')
        

    def test_editing_success(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_profile', kwargs={'pk': self.test_user1.pk, 'cat':0}))
        pass1="newpass"
        response = self.client.post(reverse('edit_profile', kwargs={'pk': self.test_user1.pk, 'cat':0}), {
            'user_name':'new_user',
            'full_name':'new_full_name',
            'department':'new_department',
            'roll_no':'new_roll_no',
            'password1':pass1,
            'password2':pass1
        })
        self.assertEqual(response.status_code, 302)
        print("response")
        print(response)
        
class FeedbackTest(TestCase):
    def setUp(self):
        self.feedback=Feedback.objects.create(
            comfort_of_stay=5,
            room_cleanliness=5,
            service_quality=5,
            additional_feedback="Good"
        )
        self.feedback.save()
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        self.test_user1.save()
        self.test_user2.save()
        
        self.student=Student.objects.create(
            user=self.test_user1,
            full_name="Test User1",
            roll_no="19XXABCDE",
            department="XX"
        )
        self.student.save()
        self.professor=Professor.objects.create(
            user=self.test_user2,
            full_name="Test User2",
            department="XX",
            address="IIT-kgp/somewhere"
        )
        self.professor.save()
        ac1bed = AC1Bed.objects.create(total_number=2,cost=500,initial_room_id=1)
        ac2bed = AC2Bed.objects.create(total_number=2,cost=1000,initial_room_id=3,)
        ac3bed = AC3Bed.objects.create(total_number=2,cost=1500,initial_room_id=5,)
        nac1bed = NAC1Bed.objects.create(total_number=2,cost=250,initial_room_id=7,)
        nacdormitory = NACDormitory.objects.create(total_number=2, cost=50,initial_room_id=15)
        acdormitory = ACDormitory.objects.create(total_number=2, cost=80,initial_room_id=13)
        nac3bed = NAC3Bed.objects.create(total_number=2, cost=150,initial_room_id=11)
        nac2bed = NAC2Bed.objects.create(total_number=2, cost=100,initial_room_id=9)
        self.ac1bed=ac1bed
        self.gh1 = GuestHouse()
        self.gh1.name = "test guest house"
        self.gh1.food_availability = 1
        self.gh1.cost_of_food = 500
        self.gh1.address = "IIT Kharagpur/Kharagpur"
        self.gh1.description = "The guest house of your dream"
        self.gh1.AC1Bed = ac1bed
        self.gh1.AC2Bed = ac2bed
        self.gh1.AC3Bed = ac3bed
        self.gh1.NAC1Bed = nac1bed
        self.gh1.NAC2Bed=nac2bed
        self.gh1.NAC3Bed=nac3bed
        self.gh1.ACDormitory=acdormitory
        self.gh1.NACDormitory=nacdormitory
        self.gh1.save()
        number_of_bookings=5
        self.booking=[]
        visitors_name=" "
        for i in range(number_of_bookings):
            visitors_count=i%3+1
            for j in range(visitors_count):
                visitors_name+="Visitor"+str(i)
                if j !=(visitors_count-1):
                    visitors_name+=","
            booking_status=""
            if(i%4==0):
                booking_status="COnfirmed"
            elif i%4==1:
                booking_status="In-Queue"
            elif i%4==2:
                booking_status="Refund"
            else:
                booking_status="Cancelled"
            check_in_date = datetime.date(2020, 4, i+1)
            check_out_date = datetime.date(2020, 5, i+1)
            booking=Booking.objects.create(
                guest_house=self.gh1,
                customer=self.test_user1,
                room_type="AC 3 Bed",
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                visitors_count=visitors_count,
                visitors_name=visitors_name,
                payment_status=i%2,
                booking_status=booking_status,
                paid_amount=0,
                refund_amount=0,
                feedback=None,
                date_of_booking=datetime.date.today
                )
            booking.save()
            self.booking.append(booking)

    def test_logged_in_uses_correct_template(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('feedback', kwargs={'pk':self.booking[0].pk,'userid': self.test_user1.pk}))
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'OGHBS_APP/feedback/index.html')
        # Check we used correct template
        self.assertTemplateUsed(response, 'OGHBS_APP/feedback/index.html')
        login_professor = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('feedback', kwargs={'pk':self.booking[0].pk,'userid': self.test_user1.pk}))
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'OGHBS_APP/feedback/index.html')

    def test_post_data(self):
        login_student = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('feedback', kwargs={'pk':self.booking[0].pk,'userid': self.test_user1.pk}))
        pass1="newpass"
        response = self.client.post(reverse('feedback', kwargs={'pk':self.booking[0].pk,'userid': self.test_user1.pk}), {
            'comfort_of_stay':5,
            'room_cleanliness':5,
            'service_quality':5,
            'additional_feedback':"Good"
        })
        self.assertEqual(response.status_code, 302)
        




