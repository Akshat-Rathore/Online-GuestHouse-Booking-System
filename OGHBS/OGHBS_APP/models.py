from django.db import models
from django.contrib.auth.models import User
# Create your models here.


ROOM_TYPES = (
    ('AC 2 Bed', 'AC 2 Bed'),
    ('AC 3 Bed', 'AC 3 Bed'),
    ('AC 1 Bed', 'AC 1 Bed'),
    ('ACDormitory', 'ACDormitory'),
    ('NACDormitory', 'NACDormitory'),
    ('NAC 2 Bed', 'NAC 2 Bed'),
    ('NAC 3 Bed', 'NAC 3 Bed'),
    ('NAC 1 Bed', 'NAC 1 Bed'),
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
    full_name = models.CharField(max_length=200, null=True, help_text="Enter the full name of the student")
    roll_no = models.CharField(max_length=100, null=True, help_text="Enter the Roll No in DDXXDDDDD format (e.g-19CS10010)")
    department = models.CharField(max_length=200, null=True, help_text="Enter the department of the student")

    def __str__(self):
        return self.user.username


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, help_text="Enter the full name of the professor")
    department = models.CharField(max_length=200, null=True, help_text="Enter the department of the professor")
    address = models.CharField(max_length=1000, null=True, help_text="Enter the address of the professor")

    def __str__(self):
        return self.user.username

class Room(models.Model):
    total_number = models.IntegerField(null=True)
    cost = models.IntegerField(null=True)
    capacity = models.IntegerField(null=True)
    initial_room_id = models.IntegerField(null=True)

    class Meta:
        abstract = True

class AC1Bed(Room):
    is_AC = models.BooleanField(default=True)
    capacity = models.IntegerField(null=True, default=1)
    room_type = models.CharField(max_length=100, default="AC 1 Bed", null=True)

    class Meta:
        verbose_name = 'AC 1 Bed'

class AC2Bed(Room):
    is_AC = models.BooleanField(default=True)
    capacity = models.IntegerField(null=True, default=2)
    room_type = models.CharField(max_length=100, default="AC 2 Bed", null=True)

    class Meta:
        verbose_name = 'AC 2 Bed'

class AC3Bed(Room):
    is_AC = models.BooleanField(default=True)
    capacity = models.IntegerField(null=True, default=3)
    room_type = models.CharField(max_length=100, default="AC 3 Bed", null=True)

    class Meta:
        verbose_name = 'AC 3 Bed'

class NAC1Bed(Room):
    is_AC = models.BooleanField(default=False)
    capacity = models.IntegerField(null=True, default=1)
    room_type = models.CharField(max_length=100, default="NAC 1 Bed", null=True)

    class Meta:
        verbose_name = 'Non-AC 1 Bed'

class NAC2Bed(Room):
    is_AC = models.BooleanField(default=False)
    capacity = models.IntegerField(null=True, default=2)
    room_type = models.CharField(max_length=100, default="NAC 2 Bed", null=True)

    class Meta:
        verbose_name = 'Non-AC 2 Bed'

class NAC3Bed(Room):
    is_AC = models.BooleanField(default=False)
    capacity = models.IntegerField(null=True, default=3)
    room_type = models.CharField(max_length=100, default="NAC 3 Bed", null=True)

    class Meta:
        verbose_name = 'Non-AC 3 Bed'

class ACDormitory(Room):
    is_AC = models.BooleanField(default=True)
    capacity = models.IntegerField(null=True, default=15)
    room_type = models.CharField(max_length=100, default="ACDormitory", null=True)

    class Meta:
        verbose_name = 'AC Dormitory'

class NACDormitory(Room):
    is_AC = models.BooleanField(default=False)
    capacity = models.IntegerField(null=True, default=15)
    room_type = models.CharField(max_length=100, default="NACDormitory", null=True)

    class Meta:
        verbose_name = 'Non-AC Dormitory'

class GuestHouse(models.Model):
    name = models.CharField(max_length=300, null=True)
    AC1Bed = models.OneToOneField(AC1Bed, on_delete=models.CASCADE, null=True)
    AC2Bed = models.OneToOneField(AC2Bed, on_delete=models.CASCADE, null=True)
    AC3Bed = models.OneToOneField(AC3Bed, on_delete=models.CASCADE, null=True)
    NAC1Bed = models.OneToOneField(NAC1Bed, on_delete=models.CASCADE, null=True)
    NAC2Bed = models.OneToOneField(NAC2Bed, on_delete=models.CASCADE, null=True)
    NAC3Bed = models.OneToOneField(NAC3Bed, on_delete=models.CASCADE, null=True)
    ACDormitory = models.OneToOneField(ACDormitory, on_delete=models.CASCADE, null=True)
    NACDormitory = models.OneToOneField(NACDormitory, on_delete=models.CASCADE, null=True)
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
    checked_out = models.BooleanField(default=0, blank=True)
    refund_amount = models.IntegerField(default=0, null=True, blank=True)
    feedback = models.OneToOneField(Feedback, null=True, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Booking-{self.id}"



