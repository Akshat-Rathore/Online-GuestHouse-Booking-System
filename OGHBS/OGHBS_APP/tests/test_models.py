from django.test import TestCase

# Create your tests here.
from OGHBS_APP.models import *

class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Student.objects.create(user=User.objects.create_user('Abc'), full_name='Abc De', roll_no='19CS10001', department='CSE')
        

    def test_full_name_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'full name')

    def test_roll_no_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('roll_no').verbose_name
        self.assertEqual(field_label, 'roll no')
    
    def test_department_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'department')

    def test_full_name_max_length(self):
        student = Student.objects.get(id=1)
        max_length = student._meta.get_field('full_name').max_length
        self.assertEqual(max_length, 200)

    def test_roll_no_max_length(self):
        student = Student.objects.get(id=1)
        max_length = student._meta.get_field('roll_no').max_length
        self.assertEqual(max_length, 100)

    def test_department_max_length(self):
        student = Student.objects.get(id=1)
        max_length = student._meta.get_field('department').max_length
        self.assertEqual(max_length, 200)

    def test_full_name_help_text(self):
        student = Student.objects.get(id=1)
        help_text = student._meta.get_field('full_name').help_text
        self.assertEqual(help_text, "Enter the full name of the student")

    def test_roll_no_help_text(self):
        student = Student.objects.get(id=1)
        help_text = student._meta.get_field('roll_no').help_text
        self.assertEqual(help_text, "Enter the Roll No in DDXXDDDDD format (e.g-19CS10010)")

    def test_department_help_text(self):
        student = Student.objects.get(id=1)
        help_text = student._meta.get_field('department').help_text
        self.assertEqual(help_text, "Enter the department of the student")

class ProfessorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Professor.objects.create(user=User.objects.create_user('Abc'), full_name='Abc De', department='CSE', address='XYZ')
        

    def test_full_name_label(self):
        professor = Professor.objects.get(id=1)
        field_label = professor._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'full name')

    def test_address_label(self):
        professor = Professor.objects.get(id=1)
        field_label = professor._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'address')
    
    def test_department_label(self):
        professor = Professor.objects.get(id=1)
        field_label = professor._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'department')

    def test_full_name_max_length(self):
        professor = Professor.objects.get(id=1)
        max_length = professor._meta.get_field('full_name').max_length
        self.assertEqual(max_length, 200)

    def test_adress_max_length(self):
        professor = Professor.objects.get(id=1)
        max_length = professor._meta.get_field('address').max_length
        self.assertEqual(max_length, 1000)

    def test_department_max_length(self):
        professor = Professor.objects.get(id=1)
        max_length = professor._meta.get_field('department').max_length
        self.assertEqual(max_length, 200)

    def test_full_name_help_text(self):
        professor = Professor.objects.get(id=1)
        help_text = professor._meta.get_field('full_name').help_text
        self.assertEqual(help_text, "Enter the full name of the professor")

    def test_address_help_text(self):
        professor = Professor.objects.get(id=1)
        help_text = professor._meta.get_field('address').help_text
        self.assertEqual(help_text, "Enter the address of the professor")

    def test_department_help_text(self):
        professor = Professor.objects.get(id=1)
        help_text = professor._meta.get_field('department').help_text
        self.assertEqual(help_text, "Enter the department of the professor")

class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AC1Bed.objects.create()

    def test_total_number_label(self):
        room = AC1Bed.objects.get(id=1)
        field_label = room._meta.get_field('total_number').verbose_name
        self.assertEqual(field_label, 'total number')

    def test_cost_label(self):
        room = AC1Bed.objects.get(id=1)
        field_label = room._meta.get_field('cost').verbose_name
        self.assertEqual(field_label, 'cost')
    
    def test_capacity_label(self):
        room = AC1Bed.objects.get(id=1)
        field_label = room._meta.get_field('capacity').verbose_name
        self.assertEqual(field_label, 'capacity')

    def test_initial_room_id_label(self):
        room = AC1Bed.objects.get(id=1)
        field_label = room._meta.get_field('initial_room_id').verbose_name
        self.assertEqual(field_label, 'initial room id')

    def test_is_AC_label(self):
        room = AC1Bed.objects.get(id=1)
        field_label = room._meta.get_field('is_AC').verbose_name
        self.assertEqual(field_label, 'is AC')

    def test_room_type_label(self):
        room = AC1Bed.objects.get(id=1)
        field_label = room._meta.get_field('room_type').verbose_name
        self.assertEqual(field_label, 'room type')

    def test_room_type_max_length(self):
        room = AC1Bed.objects.get(id=1)
        max_length = room._meta.get_field('room_type').max_length
        self.assertEqual(max_length, 100)

class GuestHouseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GuestHouse.objects.create(name = 'ABC', AC2Bed = AC2Bed.objects.create(), AC3Bed = AC3Bed.objects.create(), NAC1Bed = NAC1Bed.objects.create(), NAC2Bed = NAC2Bed.objects.create(), NAC3Bed = NAC3Bed.objects.create(), ACDormitory = ACDormitory.objects.create(), NACDormitory = NACDormitory.objects.create(), food_availability = True, cost_of_food = 100, address = 'XYZ', description = 'Best')
        

    def test_name_label(self):
        gh = GuestHouse.objects.get(id=1)
        field_label = gh._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')


    def test_food_availability_label(self):
        gh = GuestHouse.objects.get(id=1)
        field_label = gh._meta.get_field('food_availability').verbose_name
        self.assertEqual(field_label, 'food availability')
    
    def test_cost_of_food_label(self):
        gh = GuestHouse.objects.get(id=1)
        field_label = gh._meta.get_field('cost_of_food').verbose_name
        self.assertEqual(field_label, 'cost of food')

    def test_address_label(self):
        gh = GuestHouse.objects.get(id=1)
        field_label = gh._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'address')

    def test_description_label(self):
        gh = GuestHouse.objects.get(id=1)
        field_label = gh._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_name_max_length(self):
        gh = GuestHouse.objects.get(id=1)
        max_length = gh._meta.get_field('name').max_length
        self.assertEqual(max_length, 300)

    def test_address_max_length(self):
        gh = GuestHouse.objects.get(id=1)
        max_length = gh._meta.get_field('address').max_length
        self.assertEqual(max_length, 500)

    def test_description_max_length(self):
        gh = GuestHouse.objects.get(id=1)
        max_length = gh._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)


class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Feedback.objects.create(additional_feedback = 'Best')
        

    def test_comfort_of_stay_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field('comfort_of_stay').verbose_name
        self.assertEqual(field_label, 'comfort of stay')

    def test_room_cleanliness_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field('room_cleanliness').verbose_name
        self.assertEqual(field_label, 'room cleanliness')
    
    def test_service_quality_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field('service_quality').verbose_name
        self.assertEqual(field_label, 'service quality')

    def test_additional_feedback_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field('additional_feedback').verbose_name
        self.assertEqual(field_label, 'additional feedback')

    def test_additional_feedback_max_length(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field('additional_feedback').max_length
        self.assertEqual(max_length, 1000)

    
