from django.db import models
from django.contrib.auth.models import User
from tutoria.models import Client, Student, TutorProfile, Course, Tutor, Timeslot
from django.utils import timezone

import random

max_int = 2147483647

def rand(mod):
	return round(random.random() * max_int  ) % mod

list_login_type = ["Student", "Tutor"]
list_tutor_type = ["Contract"]
list_university = ["The University of Hong Kong", "Hong Kong University of Science and Technology", "Tsinghua Univeristy", "Beijing University"]
list_surname = ["Zhao", "Qian", "Sun", "Li", "Zhou", "Wu", "Zheng", "Wang", "Feng", "Chen", "Chu", "Wei", "Jiang", "Shen", "Han", "Yang", "Zhu", "Qin", "You", "Xu", "He", "Lv", "Shi", "Zhang", "Kong", "Cao", "Yan", "Hua", "Jin", "Tao", "Qi", "Xie", "Zou", "Yu", "Bai", "Shui", "Dou"]
list_given_name = ["Jiayi", "Yucheng", "Yixuan", "Yewei", "Yuanbo", "Weizeng", "Yutong", "Hongxuan", "Botao", "Yelin", "Yehua", "Yuqi", "Zhichen", "Zhenghao", "Haoran", "Mingjie","Licheng", "Lixuan", "Lihui", "Junxi", "Hongwen"]
list_is_or_not = [True, False]
list_time = ["9:00a.m.", "10:00a.m.", "11:00a.m.", "12:00a.m.", "13:00a.m.", "14:00a.m.", "15:00a.m.", "16:00a.m.", "17:00a.m.", "18:00a.m.", "19:00a.m.", "20:00a.m."]

num_user = 50
num_course = 50

for i in range(num_course):
	new_course = Course()
	new_course.code = "EXMP" + str(rand(10000))
	new_course.description = "This is a example description"
	new_course.save()

courses = Course.objects.all()

cnt = 0
for surname in list_surname:
	for given_name in list_given_name:
		cnt = cnt + 1
		if (cnt > num_user):
			break

		email = given_name.lower() + surname.lower() + "123@example.com"
		balance = rand(100) * 100
		login_type = list_login_type[rand(len(list_login_type))]
		# user
		new_user = User()
		new_user.username = given_name.lower() + surname.lower()
		# print(given_name.lower() + surname.lower())
		
		new_user.password = "Aa123456"
		new_user.first_name = given_name
		new_user.last_name = surname
		new_user.save()
		# student / tutor
		if (login_type == "Tutor"):
			# tutor profile
			new_tutor_profile = TutorProfile()
			new_tutor_profile.tutor_type = list_tutor_type[rand(len(list_tutor_type))]
			new_tutor_profile.university = list_university[rand(len(list_university))]
			new_tutor_profile.hourly_rate = (rand(9) + 1) * 10
			new_tutor_profile.average_review = rand(100)
			new_tutor_profile.introduction = "This is an example introduction"
			new_tutor_profile.availability = True
			new_tutor_profile.contact = email
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
			for i in range(time_id, min(time_id + rand(3) + 3, len(list_time) - 1), 1):
				new_timeslot = Timeslot()
				new_timeslot.is_booked = False
				new_timeslot.is_finished = False
				new_timeslot.tutor = new_tutor
				new_timeslot.startTime = list_time[i]
				new_timeslot.endTime = list_time[i + 1]
				new_timeslot.save()
		else:
			new_student = Student()
			new_student.user = new_user
			new_student.login_type = login_type
			new_student.balance = balance
			new_student.save()
	if (cnt > num_user):
		break