# AWD
Model qp来维护，model.py只能qp自己改
有model更改需求的话更qp说，4个人一起去写的话要保证model不被改乱

JK 在model稳定之后搞一套data方便大家测试用

1. Student Tutor 身份融合
	解决方案
	admin mytuor client 三类人物，之前分开的student和tutor的逻辑估计都要merge成client一人的
	1.可以考虑在client下加入ENUM(tutor，student，both)三种身份，然后各种判断，html也采用判断的方式决定是否加载作为tutor的部分
	2. 或者维持之前的逻辑不变，但是加入both的逻辑和html。既 视both为一种独立的身份来处理，这样可以将改动局限在login和model上
2. Model 现有design转为OO 参考提交的django class diagram //qp
3. apply一下之前的UI设计 //jk & ghp
	1. 登陆后分为home，search，wallet，schedule，meesage
	2. timeslot相关全部使用calendar设计
	3. To be added ...

E2 需要实现的use cases
4. registration & authentication // xy
	1. 基本注册 -- 用户名，密码
	2. 重置密码
	3. 用户指定自己的类型
	4. admin 也需要以用户形式登陆
	5. admin 以 token形式重置密码
5. session locking and ending (manage all sessions) // jk & ghp
	怕是需要一波调研，主要是怎么测试trigger
	可能需要加一个手动的trigger来方便我们测试，instruction上说可以用第三方的东西
	1. seesion结束tutor收钱
	2. 24小时内不能book cancel
	3. 收钱之后notification
	4. Mytutor 在tutor收钱的同时也要收到自己的commission fee
	5. student收到review通知
6. search //xy & qp
	1. search by universiy, university course, subject tag, hourly price， contracted or private， show all (没时间的就不要显示了)
	2. search by family and given name
	3. sort
	