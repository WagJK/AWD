from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # many-to-one
    login_type = models.CharField(max_length=20, default="Student")
    balance = models.IntegerField(default=0)

    class Meta:
        abstract = True



    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Student(Client):
    def studentModifyBooking(self,transaction):
        self.balance-=transaction
        self.save()

    def studentModifyCancelling(self,transaction,cancelledSlot):
        self.balance+=transaction
        self.timeslot_set.remove(cancelledSlot)
        self.save()


class TutorProfile(models.Model):
    # avatar = models.ImageField()
    tutor_type = models.CharField(max_length=20, default="Contract")
    university = models.CharField(max_length=50, default="HKU")
    # university course
    hourly_rate = models.IntegerField(default=10)
    average_review = models.IntegerField(default=100)
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

    def slotModifyBooking(self, bookingStudent):
        self.is_booked = True
        self.student=bookingStudent
        self.save()

    def slotModifyCancelling(self):
        self.is_booked = False
        self.save()

    @staticmethod
    def tutorGetAllSlots(selectedTutor):
        try:
            return Timeslot.objects.filter(is_booked=False, is_finished=False, tutor=selectedTutor)

        except Timeslot.DoesNotExist:
            return None

    @staticmethod
    def studentGetAllSlots(bookingStudent):
        try:
            return Timeslot.objects.filter(is_booked = True, student = bookingStudent)

        except Timeslot.DoesNotExist:
            return None


class Confirmation(models.Model):
    category = models.CharField(max_length=20, default="booking")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)

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
    def clientCreateConfirmation(type, slot):

        newConfirmation = Confirmation(category=type, tutor=slot.tutor, student=slot.student, timeslot=slot)
        newConfirmation.save()
        return

