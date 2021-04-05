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
