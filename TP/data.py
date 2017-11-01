from django.db import models
from django.contrib.auth.models import User
from tutoria.models import Client, Student, TutorProfile, Course, Tutor, Timeslot
from django.utils import timezone

import random

max_int = 2147483647

list_login_type = ["Student", "Tutor"]
list_tutor_type = ["Contract", "Private"]
list_university = ["The University of Hong Kong", "Hong Kong University of Science and Technology", "Tsinghua Univeristy", "Beijing University"]
list_surname = ["Zhao", "Qian", "Sun", "Li", "Zhou", "Wu", "Zheng", "Wang", "Feng", "Chen", "Chu", "Wei", "Jiang", "Shen", "Han", "Yang", "Zhu", "Qin", "You", "Xu", "He", "Lv", "Shi", "Zhang", "Kong", "Cao", "Yan", "Hua", "Jin", "Tao", "Qi", "Xie", "Zou", "Yu", "Bai", "Shui", "Dou"]
list_given_name = ["Jiayi", "Yucheng", "Yixuan", "Yewei", "Yuanbo", "Weizeng", "Yutong", "Hongxuan", "Botao", "Yelin", "Yehua", "Yuqi", "Zhichen", "Zhenghao", "Haoran", "Mingjie","Licheng", "Lixuan", "Lihui", "Junxi", "Hongwen"]
list_introduction = ["I have worked as a freelancer for some tutoring firms. I have received excellent reviews from my students and my peers that make me think that I am an accomplished person.", "When I teach, I used to develop interest of the student in a particular subject or problem by presenting it in a simpler way to make it more interesting in order to motivate the student.", " I teach Computer Science and Mathematics. It was a great experience as it helps not only students but me too to enhance my knowledge and skills.", "I have developed problem solving skills and analytical skills in me which further helps me to give solutions to various problems of my students.", "My enthusiasm to contribute towards education has led me to take up a job in teaching sector. So, I decide to involve myself in my area of interest.", "Hi, I have an experience in various programming languages for over 3 years .I have an experience working on different projects on python.I have expert in C,C++,Java,Python.I can help to students."]
list_is_or_not = [True, False]
list_time = ["9:00a.m.", "10:00a.m.", "11:00a.m.", "12:00a.m.", "13:00a.m.", "14:00a.m.", "15:00a.m.", "16:00a.m.", "17:00a.m.", "18:00a.m.", "19:00a.m.", "20:00a.m."]

def rand(mod):
	return round(random.random() * max_int  ) % mod

def generate_timeslot_list(year, month, date, tutor_type):
	result = []
	prefix = year + "-" + month + "-" + date + " "
	for hour in range(9, 17):
		str_hour = str(hour)
		if (hour == 9):
			str_hour = "0" + str(hour)
		if (tutor_type == "Contract"):
			result.append([prefix + str_hour + ":" + "30", 
				prefix + str(hour + 1) + ":" + "00"])
			result.append([prefix + str(hour + 1) + ":" + "00", 
				prefix + str(hour + 1) + ":" + "30"])
		else:
			result.append([prefix + str_hour + ":" + "30", 
				prefix + str(hour + 1) + ":" + "30"])
	return result

def generate_course(num_course):
	for i in range(num_course):
		new_course = Course()
		new_course.code = "COMP" + str(rand(10000))
		new_course.description = "This is a example description for a random course"
		new_course.save()

def generate_tutor(num_tutor, tutor_type):
	cnt = 0
	courses = Course.objects.all()
	while (True):
		given_name = list_given_name[rand(len(list_given_name))]
		surname = list_surname[rand(len(list_surname))]
		email = given_name.lower() + surname.lower() + "123@example.com"
		login_type = "Tutor"
		avatar = "This field will be replaced by the avatar of the user!"
		phone = str(rand(49494949) + 31231231)
		balance = rand(100) * 100

		try:
			obj = User.objects.get(username = surname + " " + given_name)
		except User.DoesNotExist:
			# user
			new_user = User.objects.create_user(
				username = surname + " " + given_name,
				password = "Aa123456",
				email = email,
				first_name = given_name,
				last_name = surname,
			)
			# tutor profile
			new_tutor_profile = TutorProfile()
			new_tutor_profile.tutor_type = tutor_type
			new_tutor_profile.university = list_university[rand(len(list_university))]
			new_tutor_profile.average_review = rand(40) + 60
			new_tutor_profile.introduction = list_introduction[rand(len(list_introduction))]
			new_tutor_profile.availability = True
			new_tutor_profile.contact = email
			if (tutor_type == "Contract"):
				new_tutor_profile.hourly_rate = 0
			else:
				new_tutor_profile.hourly_rate = (rand(3) + 4) * 10
			new_tutor_profile.save()
			# tutor
			new_tutor = Tutor()
			new_tutor.user = new_user
			new_tutor.login_type = login_type
			new_tutor.balance = balance
			new_tutor.profile = new_tutor_profile
			# new_tutor.courses.add(courses[rand(len(courses))])
			new_tutor.save()

			# timeslot
			time_id = rand(len(list_time) - 1)
			for date in ["3", "5", "9", "12"]:
				for timeslot in generate_timeslot_list("2017", "11", date, tutor_type):
					new_timeslot = Timeslot()
					new_timeslot.is_booked = False
					new_timeslot.is_finished = False
					new_timeslot.tutor = new_tutor
					new_timeslot.startTime = timeslot[0] + "+08:00"
					new_timeslot.endTime = timeslot[1] + "+08:00"
					new_timeslot.save()

			cnt = cnt + 1
			if (cnt >= num_tutor):
				break

def generate_student(num_student):
	cnt = 0
	while (True):
		given_name = list_given_name[rand(len(list_given_name))]
		surname = list_surname[rand(len(list_surname))]
		email = given_name.lower() + surname.lower() + "123@example.com"
		login_type = "Student"
		avatar = "This field will be replaced by image"
		phone = str(rand(49494949) + 31231231)
		balance = 1000
		try:
			obj = User.objects.get(username = given_name.lower() + surname.lower())
		except User.DoesNotExist:
			# user
			new_user = User.objects.create_user(
				username = surname + " " + given_name,
				password = "Aa123456",
				email = email,
				first_name = given_name,
				last_name = surname,
			)
			# student
			new_student = Student()
			new_student.user = new_user
			new_student.login_type = login_type
			new_student.balance = balance
			new_student.save()

			cnt = cnt + 1
			if (cnt >= num_student):
				break

# ------------------ Main --------------------
generate_course(4)
generate_tutor(2, "Contract")
generate_tutor(2, "Private")
generate_student(3)