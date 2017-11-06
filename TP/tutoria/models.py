from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # many-to-one
    login_type = models.CharField(max_length=20, default="Student")
    balance = models.IntegerField(default=0)
    avatar = models.TextField(default="This is an avatar")
    phone = models.CharField(max_length=10, default="None")

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Student(Client):
    pass

class Admin (Client):
    pass

class TutorProfile(models.Model):
    university = models.CharField(max_length=50, default="HKU")
    hourly_rate = models.IntegerField(default=10)
    average_review = models.IntegerField(default=100)
    introduction = models.TextField(default="This is an introduction")
    availability = models.BooleanField(default=True)
    contact = models.EmailField(default="tutor@hku.hk")  # may change in further version


class Course(models.Model):
    code = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.code


class Tutor(Client):
    login_type = models.CharField(max_length=20, default="Tutor")
    profile = models.OneToOneField(TutorProfile, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Course)
    tutor_type = models.CharField(max_length=20, default="Contract")


class Operation(models.Model):
    @staticmethod
    def all_slots_to_book(client):
        try:
            if client.login_type == "Tutor":
                return Timeslot.objects.filter(is_booked=False, is_finished=False, tutor=client)

        except Timeslot.DoesNotExist:
            return None

    @staticmethod
    def all_slots_to_cancel(client):
        try:
            if client.login_type == "Student":
                return Timeslot.objects.filter(is_booked=True, student=client)

        except Timeslot.DoesNotExist:
            return None

    @staticmethod
    def book(booking_student, timeslot):

        if timeslot.tutor.tutor_type == "Contract":
            fee = 0
        else:
            fee = timeslot.tutor.profile.hourly_rate * 1.05

        if booking_student.balance >= fee:
            # Student modify booking
            booking_student.balance -= fee
            booking_student.save()

            # Slot modify booking
            timeslot.is_booked = True
            timeslot.student = booking_student
            timeslot.save()

            Confirmation.clientCreateConfirmation("booking", timeslot, fee)
            return True
        else:
            return False

    @staticmethod
    def cancel(cancelling_student, timeslot):

        if timeslot.tutor.tutor_type == "Contract":
            fee = 0
        else:
            fee = timeslot.tutor.profile.hourly_rate * 1.05

        Confirmation.clientCreateConfirmation("cancellation", timeslot, fee)

        # Slot modify cancelling
        timeslot.is_booked = False
        timeslot.save()

        # Student modify cancelling
        cancelling_student.balance += fee
        cancelling_student.timeslot_set.remove(timeslot)
        cancelling_student.save()


class Timeslot(models.Model):
    is_booked = models.BooleanField(default=False)  # default set to false
    is_finished = models.BooleanField(default=False)

    # can be changed to datetimefield
    startTime = models.DateTimeField(default=datetime.now())
    endTime = models.DateTimeField(default=datetime.now())

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)


class Confirmation(models.Model):
    category = models.CharField(max_length=20, default="booking")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    fee = models.FloatField(default="0.00")

    @staticmethod
    def clientGetAllConfirmations(requestingClient):
        try:
            if requestingClient.login_type == "Student":
                return Confirmation.objects.filter(student = requestingClient)

            elif requestingClient.login_type == "Tutor":
                return Confirmation.objects.filter(tutor = requestingClient)

        except Confirmation.DoesNotExist:
            return None

    @staticmethod
    def clientCreateConfirmation(type, slot, fee):
        newConfirmation = Confirmation(
            category=type, 
            tutor=slot.tutor, 
            student=slot.student,
            timeslot=slot,
            fee=fee)
        newConfirmation.save()
        return
