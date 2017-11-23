from django.conf.urls import url, include

from .views import log_view
from .views import message_view
from .views import notification_view

from .views.student_view import homepage_view as student_home
from .views.student_view import schedule_view as student_schedule
from .views.student_view import search_view as student_search
from .views.student_view import wallet_view as student_wallet
from .views.student_view import editProfile_view as student_editProfile

from .views.tutor_view import homepage_view as tutor_home
from .views.tutor_view import wallet_view as tutor_wallet
from .views.tutor_view import schedule_view as tutor_schedule
from .views.tutor_view import editProfile_view as tutor_editProfile

from .views.both_view import homepage_view as both_home
from .views.both_view import schedule_view as both_schedule
from .views.both_view import wallet_view as both_wallet

urlpatterns = [
	# shared log urls
	url(r'^$', log_view.login, name='login'),
	url(r'^registration/', log_view.registrate, name='registration'),
	url(r'^logout/', log_view.logout, name='logout'),
	url(r'^notification/', include([
		url(r'^$', notification_view.notification, name='notification'),
		url(r'^clearUnread/', notification_view.clearUnread, name='clearUnread'),
	])),
	url(r'^message/', include([
		url(r'^$', message_view.message, name='message'),
		url(r'^write/', message_view.write, name='write'),
		url(r'^send/', message_view.send, name='send'),
		url(r'^clearUnread/', message_view.clearUnread, name='clearUnread'),
	])),

	# student urls
	url(r'^student/', include([
		# student homepage
		url(r'^homepage/', include([
			url(r'^$', student_home.homepage, name='student_homepage'),
			url(r'^editProfile/', student_editProfile.editProfile, name='student_editProfile'),
			url(r'^getNumOfUnreadNotf/', student_home.getNumOfUnreadNotf, name='getNumOfUnreadNotf'),
			url(r'^getNumOfUnreadMsg/', student_home.getNumOfUnreadMsg, name='getNumOfUnreadMsg')
		])),
		# student search
		url(r'^search/', include([
			url(r'^searchOption/', student_search.searchOption, name='searchOption'),
			url(r'^shortProfile/', student_search.shortProfile, name='shortProfile'),
			url(r'^detailedProfile/', student_search.detailedProfile, name='detailedProfile'),
			url(r'^availableSlot/', student_search.availableTimeSlot, name='availableSlot'),
			url(r'^timeslotInfo/', student_search.timeslotInfo, name='timeslotInfo'),
			url(r'^bookSlot/', student_search.bookTimeSlot, name='bookSlot'),
			url(r'^sort/', student_search.sort, name='sort')
		])),
		# student upcoming tutorials in 7 days
		url(r'^schedule/', include([
			url(r'^$', student_schedule.schedule, name='schedule'),
			url(r'^bookingInfo/', student_schedule.bookingInfo, name='bookingInfo'),
			url(r'^cancelSlot/', student_schedule.cancelTimeSlot, name='cancelSlot'),
			url(r'^reviewSlot/', student_schedule.reviewTimeSlot, name='reviewSlot'),
			url(r'^submitReview/', student_schedule.submitReview, name='submitReview'),
		])),
		# student wallet
		url(r'^wallet/', include([
			url(r'^$', student_wallet.wallet, name='wallet'),
			url(r'^addValue/', student_wallet.addValue, name='addValue'),
		])),
	])),

	# tutor urls
	url(r'^tutor/', include([
		# tutor homepage
		url(r'^homepage/', include([
			url(r'^$', tutor_home.homepage, name="tutor_homepage"),
			url(r'^editProfile/', include([
				url(r'^$',tutor_editProfile.editProfile, name='tutor_editProfile'),
				url(r'^flushCourse/', tutor_editProfile.flushCourse, name='tutor_flushCourse')
			])),
			url(r'^getNumOfUnreadNotf/', tutor_home.getNumOfUnreadNotf, name='getNumOfUnreadNotf'),
			url(r'^getNumOfUnreadMsg/', tutor_home.getNumOfUnreadMsg, name='getNumOfUnreadMsg')
		])),
		# tutor schedule
		url(r'^schedule/', include([
			url(r'^$', tutor_schedule.schedule, name='schedule'),
			url(r'^bookingInfo/', tutor_schedule.bookingInfo, name='bookingInfo'),
			url(r'^activate/', tutor_schedule.activate, name='activate'),
			url(r'^deactivate/', tutor_schedule.deactivate, name='deactivate'),
		])),
		# tutor wallet
		url(r'^wallet/', include([
			url(r'^$', tutor_wallet.wallet, name='wallet'),
			url(r'^withdraw/', tutor_wallet.withdraw, name="withdraw"),
		])),
	])),

	# both urls
	url(r'^both/', include([
		# both homepage
		url(r'^homepage/', student_home.homepage, name='both_homepage'),
		# both search
		url(r'^search/', include([
			url(r'^searchOption/', student_search.searchOption, name='searchOption'),
			url(r'^shortProfile/', student_search.shortProfile, name='shortProfile'),
			url(r'^detailedProfile/', student_search.detailedProfile, name='detailedProfile'),
			url(r'^availableSlot/', student_search.availableTimeSlot, name='availableSlot'),
			url(r'^bookSlot/', student_search.bookTimeSlot, name='bookSlot'),
			url(r'^sort/', student_search.sort, name='sort')
		])),
		# both upcoming tutorials in 7 days
		url(r'^schedule/', include([
			url(r'^$', student_schedule.schedule, name='schedule'),
			url(r'^cancelSlot/', student_schedule.cancelTimeSlot, name='cancelSlot'),
		])),
		# both wallet
		url(r'^wallet/', include([
			url(r'^addValue/', student_wallet.addValue, name='addValue'),
		])),
	])),
]

from pytz import utc
from .views.manage_sch import manage
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
job = scheduler.add_job(manage, 'interval', seconds=10)
scheduler.configure(timezone=utc)
scheduler.start()
