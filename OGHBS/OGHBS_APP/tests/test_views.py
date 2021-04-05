from OGHBS_APP.models import *
from OGHBS_APP.views import *
from OGHBS_APP.forms import *
from django.test import TestCase
import datetime
from django.urls import reverse
from django.core.exceptions import ValidationError

class SearchTest(TestCase):

    def setUp(self):
        # Create a Guest House
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
        nac2bed = NAC2Bed.objects.create(total_number=2, cost=50,initial_room_id=9)

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
        self.gh.NAC2Bed = nac2bed
        self.gh.NAC3Bed = nac3bed
        self.gh.ACDormitory = acdormitory
        self.gh.NACDormitory = nacdormitory
        self.gh.save()
        
        self.test_user1 = User.objects.create(
            username='Ani',
            password='ABCDEFGH'
        )

        for i in range(8):
            self.test

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

    def test_search_valid_input(self):
        check_in_date = datetime.date(2021, 4, 8)
        check_out_date = datetime.date(2021, 4, 10)
        response = self.client.post(reverse('search_room', kwargs={'gh_id': self.gh.pk}), {'check_in_date': check_in_date,'check_out_date':check_out_date})
        self.assertEqual(response.status_code, 200)
        vacancies = [2,2,2,2,2,2,2,2]
        for i in range(8):
            self.assertEqual(vacancies[i], response.context['ast'][i])
        

