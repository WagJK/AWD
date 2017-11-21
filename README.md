Construction Plan Phase 1
Internal DDL 11.19

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
1. detail booking information
2. restrict all calendar to only 2 weeks && student can only view timeslot of a tutor in 7 days

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

Unassigned functionalities
1. Messaging between tutor & student
2. Coupon code
