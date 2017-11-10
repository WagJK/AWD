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
	university = models.CharField(max_length=50, default="HKU")
	hourly_rate = models.IntegerField(default=10)
	average_review = models.IntegerField(default=100)
	introduction = models.TextField(default="This is an introduction")
	availability = models.BooleanField(default=True)


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


class Timeslot(models.Model):
	available_for_booking = models.BooleanField(default=False)
	available_for_cancelling = models.BooleanField(default=False)
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
		fee = timeslot.fee * 1.05
		if booking_student.balance < fee:
			return False
		manage()
		if not timeslot.available_for_booking:
			return False
		# modify student wallet
		booking_student.balance -= fee
		booking_student.save()
		# modify timeslot status
		timeslot.is_booked = True
		timeslot.available_for_booking = False
		timeslot.available_for_cancelling = True
		timeslot.student = booking_student
		timeslot.save()
		# sending confirmation
		Confirmation.clientCreateConfirmation("booking", timeslot, fee)
		return True

	@staticmethod
	def cancel(cancelling_student, timeslot):
		refund = timeslot.fee * 1.05
		manage()
		if not timeslot.available_for_cancelling:
			return False
		# modify timeslot status
		timeslot.is_booked = False
		timeslot.available_for_booking = True
		timeslot.available_for_cancelling = False
		timeslot.save()
		# modify student wallet
		cancelling_student.balance += refund
		cancelling_student.timeslot_set.remove(timeslot)
		cancelling_student.save()
		# sending confirmation
		Confirmation.clientCreateConfirmation("cancellation", timeslot, refund)
