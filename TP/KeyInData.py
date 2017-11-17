from django.db import models
from django.contrib.auth.models import User
from tutoria.models import *
from django.utils import timezone

import random

max_int = 2147483647

list_avatar = ["./avatars/1.png","./avatars/2.png","./avatars/3.png","./avatars/4.png","./avatars/5.png","./avatars/6.png","./avatars/7.png",
				"./avatars/8.png","./avatars/9.png","./avatars/10.png","./avatars/11.png","./avatars/12.png","./avatars/13.png","./avatars/14.png",
				"./avatars/15.png","./avatars/16.png","./avatars/17.png","./avatars/18.png","./avatars/19.png","./avatars/20.png"]
list_introduction = ["I have worked as a freelancer for some tutoring firms. I have received excellent reviews from my students and my peers that make me think that I am an accomplished person.", 
					 "When I teach, I used to develop interest of the student in a particular subject or problem by presenting it in a simpler way to make it more interesting in order to motivate the student.", 
					 " I teach Computer Science and Mathematics. It was a great experience as it helps not only students but me too to enhance my knowledge and skills.", 
					 "I have developed problem solving skills and analytical skills in me which further helps me to give solutions to various problems of my students.", 
					 "My enthusiasm to contribute towards education has led me to take up a job in teaching sector. So, I decide to involve myself in my area of interest.", 
					 "Hi, I have an experience in various programming languages for over 3 years .I have an experience working on different projects on python.I have expert in C,C++."]
list_time = ["9:00a.m.", "10:00a.m.", "11:00a.m.", "12:00a.m.", "13:00a.m.", "14:00a.m.", "15:00a.m.", "16:00a.m.", "17:00a.m.", "18:00a.m.", "19:00a.m.", "20:00a.m."]
list_course = ["COMP1117","COMP1202","COMP2119","COMP2123","COMP3234","COMP2396","COMP3258","MATH2101","MATH2211"]
list_course_description = ["This course covers both the basic and advanced features of the C/C++ programming languages, including syntax, identifiers, data types, control statements, functions, arrays, file access, objects and classes, class string, structures and pointers. It introduces programming techniques such as recursion, linked lists and dynamic data structures. The concept and skills of program design, implementation and debugging, with emphasis on problem-solving, will also be covered.",
					   "This course introduces a number of real-world computational problems taken from different areas of computer science (e.g. security and cryptography, artificial intelligence, database, web and networking). Through these problems and some hands-on exercises, students are exposed to the mathematics, data structures and algorithms that form the foundations of computer science and see how these elements integrated together to solve those problems.",
					   "Arrays, linked lists, trees and graphs; stacks and queues; symbol tables; priority queues, balanced trees; sorting algorithms; complexity analysis.",
					   "This course introduces various technologies and tools that are useful for software development, including Linux, C++ STL, the C language, shell scripts, python and xml. Learning materials will be provided but there will be no lecture. This strengthens the self-learning ability of the students.",
					   "Network structure and architecture; reference models; stop and wait protocol; sliding window protocols; character and bit oriented protocols; virtual circuits and datagrams; routing; flow control; congestion control; local area networks; issues and principles of network interconnection; transport protocols and application layer; and examples of network protocols.",
					   "Introduction to object-oriented programming; abstract data types and classes; inheritance and polymorphism; object-oriented program design; Java language and its program development environment; user interfaces and GUI programming; collection class and iteration protocol; program documentation.",
					   "The course teaches the basics of functional programming using the language Haskell. The main goal is introduce students to fundamental programming concepts such as recursion, abstraction, lambda expressions and higher-order functions and data types. The course will also study the mathematical reasoning involved in the design of functional programs and techniques for proving properties about functions so defined. With the adoption of lambda expressions recent versions of Java, C++ or C#, functional programming and related programming techniques are becoming increasingly more relevant even for programmers of languages that are not traditionally viewed as functional. This course is important to introduce students to such techniques.",
					   "This is a first university level course on linear algebra, which aims at introducing to students the basic concept of linear structure through many concrete examples in the Euclidean spaces. The course also enriches students' exposure to mathematical rigor and prepares them for studying more advanced mathematical courses.",
					   "Students of this course will learn the theory of multivariable calculus and learn how to apply the theory to solve practical problems. This is a required course for Mathematics and Mathematics/Physics Majors, and is suitable for all students in Science, Engineering, Economics and Finance, and other students who will use multivariable calculus in their areas of study. This is also a required course for all Minors offered by the Department of Mathematics, and is a pre-requisite of many advanced level mathematics courses."]
list_tag = ["CS", "MATH", "C++", "Java", "Network", "Introduction", "Algorithm", "Shell Script", "Hascal","Linear algebra", "Calculus"]

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

def generate_course():
	for i in range(len(list_course)):
		new_course = Course()
		new_course.code = list_course[i]
		new_course.description = list_course_description[i]
		new_course.save()

def generate_tag():
	for i in range(len(list_tag)):
		new_tag = Tag()
		new_tag.content = list_tag[i]
		new_tag.save()

def generate_tutor(given_name_v, surname_v, tutor_type, avatar_v, university_v, hourly_rate_v, average_review_v, introduction_v, dates_v, courses_v, tags_v):
# avatar_v \in [0, 19], because there are total 20 pictures in ./avatar.
# dates is a list of dates when the tutors is available. e.g. ["13","15"].
# courses is a list of integers \in [0, len(list_course)-1].
# tags is a list of integers \in [0, len(list_tag)-1].	
	courses = Course.objects.all()
	tags = Tag.objects.all()
	given_name = given_name_v
	surname = surname_v
	email = given_name.lower() + surname.lower() + "@example.com"
	login_type = "Tutor"
	avatar = list_avatar[avatar_v]
	phone = str(rand(49494949) + 31231231)
	balance = rand(100) * 100
	hourly_rate = hourly_rate_v
	university = university_v
	average_review = average_review_v
	introduction = list_introduction[introduction_v]
	# user
	new_user = User.objects.create_user(
		username = surname + " " + given_name,
		password = "a",
		email = email,
		first_name = given_name,
		last_name = surname
	)
	# tutor profile
	new_tutor_profile = TutorProfile.objects.create(
		university = university,
		hourly_rate = hourly_rate,
		average_review = average_review,
		introduction = introduction,
		availability = True
	)
	# tutor
	new_tutor = Tutor.objects.create(
		user = new_user,
		login_type = login_type,
		tutor_type = tutor_type,
		balance = balance,
		profile = new_tutor_profile,
	)
	#course
	for each in courses_v:
		new_tutor.course.add(courses[each])
	#tag
	for each in tags_v:
		new_tutor.tag.add(tags[each])
	# timeslot
	time_id = rand(len(list_time) - 1)
	for date in dates_v:
		for timeslot in generate_timeslot_list("2017", "11", date, tutor_type):
			new_timeslot = Timeslot.objects.create(
				fee = hourly_rate,
				is_booked = False,
				is_finished = False,
				bookable = False,
				cancellable = False,
				tutor = new_tutor,
				startTime = timeslot[0] + "+08:00",
				endTime = timeslot[1] + "+08:00",
			)

def generate_student(given_name_v, surname_v, avatar_v):
	given_name = given_name_v
	surname = surname_v
	email = given_name.lower() + surname.lower() + "@example.com"
	login_type = "Student"
	avatar = list_avatar[avatar_v]
	phone = str(rand(49494949) + 31231231)
	balance = 1000.0
	# user
	new_user = User.objects.create_user(
		username = surname + " " + given_name,
		password = "a",
		email = email,
		first_name = given_name,
		last_name = surname
	)
	# student
	new_student = Student.objects.create(
		user = new_user,
		login_type = login_type,
		balance = balance,
		avatar = avatar,
		phone = phone
	)

def generate_both(given_name_v, surname_v, tutor_type, avatar_v, university_v, hourly_rate_v, average_review_v, introduction_v, dates_v, courses_v, tags_v):
# avatar_v \in [0, 19], because there are total 20 pictures in ./avatar.
# dates is a list of dates when the tutors is available. e.g. ["13","15"].
# courses is a list of integers \in [0, len(list_course)-1].
# tags is a list of integers \in [0, len(list_tag)-1].	
	courses = Course.objects.all()
	tags = Tag.objects.all()
	given_name = given_name_v
	surname = surname_v
	email = given_name.lower() + surname.lower() + "@example.com"
	login_type = "Tutor"
	avatar = list_avatar[avatar_v]
	phone = str(rand(49494949) + 31231231)
	balance = rand(100) * 100
	hourly_rate = hourly_rate_v
	university = university_v
	average_review = average_review_v
	introduction = list_introduction[introduction_v]
	# user
	new_user = User.objects.create_user(
		username = surname + " " + given_name,
		password = "a",
		email = email,
		first_name = given_name,
		last_name = surname
	)
	# student
	new_student = Student.objects.create(
		user = new_user,
		login_type = login_type,
		balance = balance,
		avatar = avatar,
		phone = phone
	)
	# tutor profile
	new_tutor_profile = TutorProfile.objects.create(
		university = university,
		hourly_rate = hourly_rate,
		average_review = average_review,
		introduction = introduction,
		availability = True
	)
	# tutor
	new_tutor = Tutor.objects.create(
		user = new_user,
		login_type = login_type,
		tutor_type = tutor_type,
		balance = balance,
		profile = new_tutor_profile,
	)
	#course
	for each in courses_v:
		new_tutor.course.add(courses[each])
	#tag
	for each in tags_v:
		new_tutor.tag.add(tags[each])
	# timeslot
	time_id = rand(len(list_time) - 1)
	for date in dates_v:
		for timeslot in generate_timeslot_list("2017", "11", date, tutor_type):
			new_timeslot = Timeslot.objects.create(
				fee = hourly_rate,
				is_booked = False,
				is_finished = False,
				bookable = False,
				cancellable = False,
				tutor = new_tutor,
				startTime = timeslot[0] + "+08:00",
				endTime = timeslot[1] + "+08:00",
			)

# ------------------ Main --------------------

# list_university = ["The University of Hong Kong", "Hong Kong University of Science and Technology", "Tsinghua Univeristy", "Beijing University"]
# list_surname = ["Zhao", "Qian", "Sun", "Li", "Zhou", "Wu", "Zheng", "Wang", "Feng", "Chen", "Chu", "Wei", "Jiang", "Shen", "Han", "Yang", "Zhu", "Qin", "You", "Xu", "He", "Lv", "Shi", "Zhang", "Kong", "Cao", "Yan", "Hua", "Jin", "Tao", "Qi", "Xie", "Zou", "Yu", "Bai", "Shui", "Dou"]
# list_given_name = ["Jiayi", "Yucheng", "Yixuan", "Yewei", "Yuanbo", "Weizeng", "Yutong", "Hongxuan", "Botao", "Yelin", "Yehua", "Yuqi", "Zhichen", "Zhenghao", "Haoran", "Mingjie","Licheng", "Lixuan", "Lihui", "Junxi", "Hongwen"]


generate_course()
generate_tag()
generate_tutor("Jiayi", "Zhao", "Contract", 0, "The University of Hong Kong", 0, 80, 0, ["13", "15"], [0], [0, 2])
generate_tutor("Yucheng", "Qian", "Contract", 1, "The University of Hong Kong", 0, 90, 1, ["13", "15"], [1], [0, 3])
generate_tutor("Yixuan", "Sun", "Private", 2, "Hong Kong University of Science and Technology", 150, 80, 2, ["13", "15"], [2], [0, 4])
generate_tutor("Yewei", "Li", "Private", 3, "Hong Kong University of Science and Technology", 120, 80, 3, ["13", "15"], [3], [0, 1])
generate_tutor("Yuanbo", "Zhou", "Private", 4, "Tsinghua Univeristy", 130, 80, 4, ["13", "15"], [4], [4, 2])
generate_tutor("Weizeng", "Wu", "Private", 5, "Tsinghua Univeristy", 100, 80, 5, ["13", "15"], [5], [5, 2])
generate_tutor("Yutong", "Zheng", "CPrivate", 6, "Beijing University", 110, 80, 0, ["13", "15"], [6], [1, 2])
generate_student("Xiyang", "Feng", 7)
generate_student("Hongpeng", "Guo", 8)
generate_both("Hongxuan", "Chen", "Private", 9, "Beijing University", 150, 80, 3, ["13", "15"], [7], [7, 2])
generate_both("Botao", "Chu", "Contract", 10, "The University of Hong Kong", 0, 80, 4, ["13", "15"], [8], [1, 2])

