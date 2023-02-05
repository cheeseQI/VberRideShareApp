from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_driver = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)


class Vehicle(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    plate_number = models.IntegerField()
    max_capacity = models.IntegerField()
    spec_info = models.CharField(max_length=50)


class Ride(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_as_owner')
    sharer = models.ManyToManyField(User, related_name='ride_as_sharer', blank=True)
    can_share = models.BooleanField(default=False)
    dest_addr = models.CharField(max_length=50)
    required_time = models.DateTimeField()
    vehicle_type = models.CharField(max_length=20)
    status = models.CharField(max_length=10)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True)
    spec_info = models.CharField(max_length=50)
