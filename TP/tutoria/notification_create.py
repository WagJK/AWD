from .models import*

def get_all_notification(user):
	try:
		return Notification.objects.filter(user=user).order_by('-createTime', '-id')
	except Notification.DoesNotExist:
		return None

def createBookNotification(slot):
	studentContent = "You have successfully booked the tutorial session scheduled at "+ str(slot) \
					 + " given by tutor "+ (str)(slot.tutor) + "."
	studentBookNotification = Notification(
		category="book",
		content=studentContent,
		user=slot.student.user
	)
	studentBookNotification.save()
	tutorContent = "Your tutorial session scheduled at "+ str(slot) + " has been booked by student " \
				   + (str)(slot.student) + "."
	tutorBookNotification = Notification(
		category="book",
		content=tutorContent,
		user=slot.tutor.user
	)
	tutorBookNotification.save()
	return

def createCancelNotification(slot):
	studentContent = "You have successfully cancelled the tutorial session scheduled at " + str(slot) \
					 + " given by tutor " + (str)(slot.tutor) + "."
	studentCancelNotification = Notification(
		category="cancel",
		content=studentContent,
		user=slot.student.user,
	)
	studentCancelNotification.save()
	tutorContent = "Your tutorial session scheduled at " + str(slot) + " has been cancelled by student " \
				   + (str)(slot.student) + "."
	tutorCancelNotification = Notification(
		category="cancel",
		content=tutorContent,
		user=slot.tutor.user,
	)
	tutorCancelNotification.save()
	return

def createTransactionNotification(slot, money, type):
	if money == 0:
		return
	if type == 'book':
		studentContent = (str)(money) + " HKD has been deducted from your wallet."
		studentNotification = Notification(
			category="transaction",
			content=studentContent,
			user=slot.student.user,
		)
		studentNotification.save()
	elif type == 'cancel':
		studentContent = (str)(money) + " HKD has been returned to your wallet."
		studentNotification = Notification(
			category="transaction",
			content=studentContent,
			user=slot.student.user,
		)
		studentNotification.save()
	elif type == 'end':
		tutorContent = (str)(money) + " HKD has been transferred to your wallet."
		tutorNotification = Notification(
			category="transaction",
			content=tutorContent,
			user=slot.student.tutor,
		)
		tutorNotification.save()
	return

def createReviewNotification (slot):
	requestContent = "You are invited to post your review on the ended tutorial session at " + str(slot) \
					 + " conducted by tutor " + (str)(slot.tutor)\
					 + ". Please go to your schedule and find your finished tutorial to make a review."
	reviewNotification = Notification(
		category="review",
		content=requestContent,
		user=slot.student.user)
	reviewNotification.save()
	return

def createTransactionRecord(slot, money, type, user):
	if money == 0:
		return
	usr = User.objects.none()
	status = ""
	studentMoney = tutorMoney = myTutorMoney = 0
	if type == 'book':
		usr = slot.student.user
		status = "Outgoing"
		studentMoney = money
		tutorMoney = money / 1.05
		myTutorMoney = studentMoney - tutorMoney
	elif type == 'cancel':
		usr = slot.student.user
		status = "Incoming"
		studentMoney = money
		tutorMoney = money / 1.05
		myTutorMoney = studentMoney - tutorMoney
	elif type == 'end':
		usr = slot.tutor.user
		status = "Incoming"
		studentMoney = money * 1.05
		tutorMoney = money
		myTutorMoney = money * 0.05
	elif type == 'add':
		usr = user
		status = "Incoming"
	elif type == 'withdraw':
		usr = user
		status = "Outgoing"

	transferContent = "Amount: " + str(money) + " HKD\n" + "Status: " + status + "\n"

	if type == 'book':
		transferContent += "Related Timeslot: " + str(slot) + "\n"  + "Other Parties Involved: "
		transferContent += ("Tutor "+ (str)(slot.tutor) + " (" + str(tutorMoney) + " HKD Pending Income); MyTutors ("
						   + str(myTutorMoney) + " HKD Pending Income)")
	elif type == 'cancel':
		transferContent += "Related Timeslot: " + str(slot) + "\n" + "Other Parties Involved: "
		transferContent += ("Tutor " + (str)(slot.tutor) + " (" + str(tutorMoney) + " HKD Pending Refunded); MyTutors ("
							+ str(myTutorMoney) + " HKD Pending Refunded)")
	elif type == 'end':
		transferContent += "Related Timeslot: " + str(slot) + "\n" + "Other Parties Involved: "
		transferContent += ("Student " + (str)(slot.student) + " (" + str(studentMoney) + " HKD Paid); MyTutors ("
							+ str(myTutorMoney) + " HKD Received)")

	transactionHistory = TransactionRecord(
		content=transferContent,
		user=usr,
		fee=money
	)
	transactionHistory.save()
	return