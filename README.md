Construction Plan Phase 1
Internal DDL 11.19

qp:
1. Transaction History: 
	界面规划， 30天之内的history， 都在wallet下完成
	history包括，钱数， outgoing还是incoming，name of parties involved
	eg. student：$105， outgoing，xxx timeslot， $100 to xxx， $ to xxx as commission fee
		tutor： $100， incoming  
2. Review:
	和tutor是一对多 null = true 的关系
	在timeslot 结束时create
	界面应该是0到5星的评价形式
	tutor拥有3个以上review的时候会create自己的average_review
	detail profile要显示所有的review

3。 notification
	payment notification
	book notification
	cancel notification
	review notification

4. search加入tag 结果要显示姓名，头像，大学， hourly rate， average review 和 tags

jk：
1. schedule 界面完善:
	student：7天
		schedule 界面展示7天内自己book的timeslot， 点击后可看detail，并进行各类operation
	Tutor：14天， 翻页形式
		schedule 界面展示自己指定的所有timeslot的状态 (每个格子状态可以为 not available， booked， unbooked)
2. wallet:
	add/withdraw money


xy：
1. 个人资料编辑：
	User：
		编辑姓名，邮箱，电话
	Tutor：
		编辑tag， hourly rate，选择自己的available timeslot(此处jk搞) 或者black out unavailable, active/deactive 自己的profile
2. 用户头像问题
3. notification 同时向后台发邮件
4. admin规定每个university的course code

附属功能：
1. tutor student 通信

未解决的特殊要求
1. both 不能book自己的timeslot qp
2. tutor只能有一个university xy
3. check hourly rate 为 10的倍数 xy
4. Contract tutor 不能编辑自己的hourly rate xy
5. tutor student互相不能看到phone 除非他们之间有book关系 qp xy
6. student只能看到tutor7天内的timeslot (search part) jk
7. student 一天内只能定！一个人的一个timeslot！但是可以订多个每个都是不一样的人 qp jk
8. tutor 不能blackout 已经被定的timeslot jk 
9. 没有足够钱来book的时候会被reject并提示 qp



Q1：Tag 的形式，是否为系统指定好再有tutor选择，或是tutor自由输入？
A1：系统指定

Q2：Coupon code实现形式？
A2：  