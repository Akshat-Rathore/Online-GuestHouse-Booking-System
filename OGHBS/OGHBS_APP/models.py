from django.db import models
from django.contrib.auth.models import User
# Create your models here.


ROOM_TYPES = (
    ('AC 2 Bed', 'AC 2 Bed'),
    ('AC 3 Bed', 'AC 3 Bed'),
    ('AC 1 Bed','AC 1 Bed'),
    ('ACDormatory','ACDormatory'),
    ('NACDormatory','NACDormatory'),
    ('NAC 2 Bed', 'NAC 2 Bed'),
    ('NAC 3 Bed', 'NAC 3 Bed'),
    ('NAC 1 Bed','NAC 1 Bed'),
)

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

BOOKING_STATUS = (
    ('0', 'Confirmed'),
    ('1', 'In-Queue'),
    ('2', 'Refund'),
    ('3', 'Cancelled'),
)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True)
    roll_no = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.username


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.user.username

class Room(models.Model):
    is_AC = models.BooleanField(default=False)
    total_number = models.IntegerField(null=True)
    booked_rooms = models.CharField(max_length=1000, null=True,blank=True)
    cost = models.IntegerField(null=True)
    capacity = models.IntegerField(null=True)
    room_type = models.CharField(max_length=100, choices=ROOM_TYPES, null=True)
    initial_room_id = models.IntegerField(null=True)

    def __str__(self):
        s = ''
        if self.is_AC:
            s += "AC "
        else:
            s += "Non-AC "
        s += (str(self.capacity) + " Bed Room")
        return s


class GuestHouse(models.Model):
    name = models.CharField(max_length=300, null=True)
    ACDormatory=models.OneToOneField(Room, related_name='ACDormatory_set', on_delete=models.CASCADE,null=True)
    AC1Bed=models.OneToOneField(Room, related_name='AC1Bed_set', on_delete=models.CASCADE,null=True)
    AC2Bed = models.OneToOneField(Room, related_name='AC2Bed_set', on_delete=models.CASCADE,null=True)
    AC3Bed = models.OneToOneField(Room, related_name='AC3Bed_set', on_delete=models.CASCADE,null=True)
    NACDormatory=models.OneToOneField(Room, related_name='NACDormatory_set', on_delete=models.CASCADE,null=True)
    NAC1Bed=models.OneToOneField(Room, related_name='NAC1Bed_set', on_delete=models.CASCADE,null=True)
    NAC2Bed = models.OneToOneField(Room, related_name='NAC2Bed_set', on_delete=models.CASCADE,null=True)
    NAC3Bed = models.OneToOneField(Room, related_name='NAC3Bed_set', on_delete=models.CASCADE,null=True)
    food_availability = models.BooleanField(default=False)
    cost_of_food = models.IntegerField(null=True, blank=True)
    customer = models.ManyToManyField(User, through='Booking', null=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.name


class Feedback(models.Model):
    comfort_of_stay = models.IntegerField(choices=RATING_CHOICES, null=True, default=5, blank=True)
    room_cleanliness = models.IntegerField(choices=RATING_CHOICES, null=True, default=5, blank=True)
    service_quality = models.IntegerField(choices=RATING_CHOICES, null=True, default=5, blank=True)
    additional_feedback = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.additional_feedback


class Booking(models.Model):
    guest_house = models.ForeignKey(GuestHouse, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    room_type = models.CharField(max_length=100, choices=ROOM_TYPES)
    check_in_date = models.DateField(null=True)
    check_out_date = models.DateField(null=True)
    visitors_count = models.IntegerField(null=True)
    visitors_name = models.CharField(max_length=5000, null=True)
    payment_status = models.BooleanField(default=False)
    booking_status = models.CharField(max_length=100, choices=BOOKING_STATUS, null=True)
    paid_amount = models.IntegerField(null=True)
    room_id = models.IntegerField(null=True, blank=True)
    food = models.BooleanField(default=0, blank=True)
    refund_amount = models.IntegerField(default=0, null=True, blank=True)
    feedback = models.OneToOneField(Feedback, null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.guest_house.name + '_' + self.room_type + '_' + self.customer.username + '_' + str(self.id)



