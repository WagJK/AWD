from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	login_type = models.CharField(max_length=20, default="Student")
	avatar = models.FileField(upload_to='media/avatars/%Y/%m/%d/', null=True)
	phone = models.CharField(max_length=10, default="None")

	class Meta:
		abstract = True

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name


class Student(Client):
	pass


class Admin (Client):
	pass


class MyTutors(models.Model):
	balance = models.FloatField(default="0.00")
	commission_rate = models.FloatField(default="0.05")


class TutorProfile(models.Model):
	university = models.CharField(max_length=50)
	hourly_rate = models.IntegerField(default=10)
	average_review = models.DecimalField(default=-1, max_digits=4, decimal_places=2)
	introduction = models.TextField(default="This is an introduction")
	availability = models.BooleanField(default=True)


class Course(models.Model):
	university = models.CharField(max_length=50)
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
	is_reviewed = models.BooleanField(default=False)
	startTime = models.DateTimeField(default=datetime.now())
	endTime = models.DateTimeField(default=datetime.now())
	within_week = models.BooleanField(default=False)

	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
	fee = models.FloatField(default=0.00)

	def __str__(self):
		interval = (str)((self.startTime.hour + 8) % 24) + ":" \
		+ ((str)(self.startTime.minute)).zfill(2) + " " + (str)(self.startTime.month) + "/" \
		+ ((str)(self.startTime.day)).zfill(2) + "/" + (str)(self.startTime.year) + " - " \
		+ (str)((self.endTime.hour + 8) % 24) + ":" + ((str)(self.endTime.minute)).zfill(2) + " " \
		+ (str)(self.endTime.month) + "/" + ((str)(self.endTime.day)).zfill(2) + "/" \
		+ (str)(self.endTime.year)
		return interval


class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	unread = models.BooleanField(default=True)
	category = models.CharField(max_length=20, default="booking")
	content = models.TextField(default="This is a notification!")
	createTime = models.DateTimeField(default=datetime.now())


class TransactionRecord(models.Model):
	fee = models.FloatField(default="0.00")
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField(default="This is a notification!")
	createTime = models.DateTimeField(default=datetime.now())


class Message(models.Model):
	unread = models.BooleanField(default=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
	content = models.TextField(default="None")
	createTime = models.DateTimeField(default=datetime.now())


class Review(models.Model):
	star = models.IntegerField(default="3")
	comment = models.TextField(default="")
	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	anonymous = models.BooleanField(default=False)
	createTime = models.DateTimeField(default=datetime.now())


class Wallet(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.FloatField(default="0.00")


class Coupon(models.Model):
	code = models.CharField(max_length=20)
	generation_date = models.DateTimeField(default=datetime.now())
	expiration_date = models.DateTimeField()