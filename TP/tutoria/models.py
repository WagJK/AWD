from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # many-to-one
    login_type = models.CharField(max_length=20, default="Student")
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Student(Client):
    pass


class TutorProfile(models.Model):
    # avatar = models.ImageField()
    tutor_type = models.CharField(max_length=20, default="Contract")
    university = models.CharField(max_length=50, default="HKU")
    # university course
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    average_review = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    # subject tags

    introduction = models.TextField()
    # reviews
    availability = models.BooleanField(default=True)
    contact = models.EmailField(default = "tutor@hku.hk")  # may change in further version


class Course(models.Model):
    code = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.code


class Tutor(Client):
    profile = models.OneToOneField(TutorProfile, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)


class Timeslot(models.Model):
    is_booked = models.BooleanField(default=False)  # default set to false
    is_finished = models.BooleanField(default=False)

    # can be changed to datetimefield
    startTime = models.TextField(default="0:00a.m")
    endTime = models.TextField(default="1:00a.m")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)


