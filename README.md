Construction Plan Phase 1
Internal DDL 11.19

IMPORTANT !!!  
Before using the admin funciton, first install 'pip install django-bulk-admin'  
Admin username: 'admin'  
Password: 'Fxy86356428'  
Can only operate on Course model and support bulk oprtations  

qp:
1. Transaction History: 
	界面规划， 30天之内的history， 都在wallet下完成
	
2. Review:
	和tutor是一对多 null = true 的关系
	在timeslot 结束时create
	界面应该是0到5星的评价形式
	tutor拥有3个以上review的时候会create自己的average_review
	detail profile要显示所有的review

3. search加入tag 结果要显示姓名，头像，大学， hourly rate， average review 和 tags

jk：
1. restrict all calendar to only 2 weeks && student can only view timeslot of a tutor in 7 days

xy：
1. 个人资料编辑：
	User：
		编辑姓名, 邮箱, 电话
	Tutor：
		编辑tag, hourly rate, active/deactive 自己的profile
2. 用户头像问题
3. notification 同时向后台发邮件
4. admin规定每个university的course code

未解决的特殊要求
1. both 不能book自己的timeslot qp
2. tutor只能有一个university xy
3. check hourly rate 为 10的倍数 xy
4. Contract tutor 不能编辑自己的hourly rate xy
5. tutor student互相不能看到phone 除非他们之间有book关系 qp xy
6. student只能看到tutor7天内的timeslot (search part) jk
7. student 一天内只能定！一个人的一个timeslot！但是可以订多个每个都是不一样的人 qp jk
8. 没有足够钱来book的时候会被reject并提示 qp

Ongoing Functionalities:
XY: Profile Management
	a. Contract tutor cannot edit hourly rate = 0
QP: Review System

Finished Functionalities:
1. Login and Registration
2. Session Locking
3. Searching for tutor
4. Transaction History
5. Notification System
6. Messaging System

Unassigned Functionalities:
1. Coupon code
2. Administrator
	• (for Administrators) control access to Tutoria through user authentication based on username and password.
	• (for Administrators) send mail to the user containing a token for password reset after receiving a lost password request.

Unfinished Functionalities:
3. Wallet Management
	• (for Tutors) transfer money from their wallet.
	• (for Students) add money to their wallet.
	• (for MyTutors) transfer money from their wallet.
	Your responsibility is only to provide a system of internal wallets and a simple interface to support demos and testing. Through the interface, students may deposit funds in their wallets and tutors and MyTutors may remove funds from their wallets.
4. Calendar
	a. student can only view timeslots in a week (calendar locking).
5. Booking and Cancelling
	a. student can only book one timeslot from a tutor per day.
	b. student cannot book the same timeslot from different tutor.
	c. No money - booking rejected and student informed
	d. one cannot book his/her own timeslot
6. Detailed Profile
	a. tutor and student could not view each other's phone unless there is a session between them

Modeling:
1. Contracted tutor can only have 1 university, private tutor should not? have a university.