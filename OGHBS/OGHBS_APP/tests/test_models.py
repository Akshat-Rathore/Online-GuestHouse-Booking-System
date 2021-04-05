from django.test import TestCase

# Create your tests here.
from OGHBS_APP.models import Student, Professor, Room, GuestHouse, Feedback, Booking

class StudentModelTest(TestCase):
    def setUpTestData(cls):
        Student.objects.create(full_name='Abc De', roll_no='19CS10001', department='CSE')

    def test_full_name_label(self):
        student = Student.objects.get(id=1)