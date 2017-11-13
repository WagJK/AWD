from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)  # many-to-one
	login_type = models.CharField(max_length=20, default="Student")
	balance = models.FloatField(default="0.00")
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

class MyTutor(models.Model):
	balance = models.FloatField(default="0.00")

class TutorProfile(models.Model):
	university = models.CharField(max_length=50)
	hourly_rate = models.IntegerField(default=10)
	average_review = models.IntegerField(default=100)
	introduction = models.TextField(default="This is an introduction")
	availability = models.BooleanField(default=True)


class Course(models.Model):
	code = models.CharField(max_length=200)
	description = models.CharField(max_length=2000)

	def __str__(self):
		return self.code

class Tag(models.Model):
	content = models.CharField(max_length=50)

	def __str__(self):
		return self.content


class Tutor(Client):
	login_type = models.CharField(max_length=20, default="Tutor")
	profile = models.OneToOneField(TutorProfile, on_delete=models.CASCADE, null=True)
	course = models.ManyToManyField(Course)
	tag = models.ManyToManyField(Tag)
	tutor_type = models.CharField(max_length=20, default="Contract")


class Timeslot(models.Model):
	bookable = models.BooleanField(default=False)
	cancellable = models.BooleanField(default=False)
	is_booked = models.BooleanField(default=False)
	is_finished = models.BooleanField(default=False)

	fee = models.FloatField(default="0.00")
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
