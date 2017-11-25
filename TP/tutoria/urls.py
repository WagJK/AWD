from django.conf.urls import url, include
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

from .views.manage_sch import manage

from .views import log_view
from .views import message_view
from .views import notification_view
from .views import wallet_view
from .views import manage_view

from .views.student_view import homepage_view as student_home
from .views.student_view import schedule_view as student_schedule
from .views.student_view import search_view as student_search
from .views.student_view import editProfile_view as student_editProfile

from .views.tutor_view import homepage_view as tutor_home
from .views.tutor_view import schedule_view as tutor_schedule
from .views.tutor_view import editProfile_view as tutor_editProfile

from .views.both_view import homepage_view as both_home
from .views.mytutors_view import mytutors_view

urlpatterns = [
	url(r'^$', log_view.login, name='login'),
	url(r'^manage/', manage_view.manage, name='manage'),
	url(r'^registration/', log_view.registrate, name='registration'),
	url(r'^logout/', log_view.logout, name='logout'),
	url(r'^wallet/', include([
		url(r'^$', wallet_view.wallet, name='wallet'),
		url(r'^addValue/', wallet_view.addValue, name='addValue'),
		url(r'^withdraw/', wallet_view.withdraw, name="withdraw"),
	])),
	url(r'^notification/', include([
		url(r'^$', notification_view.notification, name='notification'),
		url(r'^clearUnread/', notification_view.clearUnread, name='clearUnread'),
		url(r'^getNumOfUnreadNotf/', notification_view.getNumOfUnreadNotf, name='getNumOfUnreadNotf'),
	])),
	url(r'^message/', include([
		url(r'^$', message_view.message, name='message'),
		url(r'^write/', message_view.write, name='write'),
		url(r'^send/', message_view.send, name='send'),
		url(r'^clearUnread/', message_view.clearUnread, name='clearUnread'),
		url(r'^getNumOfUnreadMsg/', message_view.getNumOfUnreadMsg, name='getNumOfUnreadMsg')
	])),

	url(r'^MyTutors/', include([
		url(r'^$', mytutors_view.homepage, name='mytutors_homepage'),
		url(r'^withdraw/', mytutors_view.withdraw, name="mytutors_withdraw"),
	])),

	url(r'^student/', include([
		url(r'^homepage/', include([
			url(r'^$', student_home.homepage, name='student_homepage'),
			url(r'^editProfile/', student_editProfile.editProfile, name='student_editProfile'),
		])),
		url(r'^search/', include([
			url(r'^searchOption/', student_search.searchOption, name='searchOption'),
			url(r'^shortProfile/', student_search.shortProfile, name='shortProfile'),
			url(r'^detailedProfile/', student_search.detailedProfile, name='detailedProfile'),
			url(r'^availableSlot/', student_search.availableTimeSlot, name='availableSlot'),
			url(r'^timeslotInfo/', student_search.timeslotInfo, name='timeslotInfo'),
			url(r'^bookSlot/', student_search.bookTimeSlot, name='bookSlot'),
			url(r'^sort/', student_search.sort, name='sort')
		])),
		url(r'^schedule/', include([
			url(r'^$', student_schedule.schedule, name='schedule'),
			url(r'^bookingInfo/', student_schedule.bookingInfo, name='bookingInfo'),
			url(r'^cancelSlot/', student_schedule.cancelTimeSlot, name='cancelSlot'),
			url(r'^reviewSlot/', student_schedule.reviewTimeSlot, name='reviewSlot'),
			url(r'^submitReview/', student_schedule.submitReview, name='submitReview'),
		])),
	])),

	url(r'^tutor/', include([
		url(r'^homepage/', include([
			url(r'^$', tutor_home.homepage, name="tutor_homepage"),
			url(r'^editProfile/', include([
				url(r'^$',tutor_editProfile.editProfile, name='tutor_editProfile'),
				url(r'^flushCourse/', tutor_editProfile.flushCourse, name='tutor_flushCourse')
			])),
		])),
		url(r'^schedule/', include([
			url(r'^$', tutor_schedule.schedule, name='schedule'),
			url(r'^bookingInfo/', tutor_schedule.bookingInfo, name='bookingInfo'),
			url(r'^activate/', tutor_schedule.activate, name='activate'),
			url(r'^deactivate/', tutor_schedule.deactivate, name='deactivate'),
		])),
	])),

	url(r'^both/', include([
		url(r'^homepage/', student_home.homepage, name='both_homepage'),
		url(r'^search/', include([
			url(r'^searchOption/', student_search.searchOption, name='searchOption'),
			url(r'^shortProfile/', student_search.shortProfile, name='shortProfile'),
			url(r'^detailedProfile/', student_search.detailedProfile, name='detailedProfile'),
			url(r'^availableSlot/', student_search.availableTimeSlot, name='availableSlot'),
			url(r'^timeslotInfo/', student_search.timeslotInfo, name='timeslotInfo'),
			url(r'^bookSlot/', student_search.bookTimeSlot, name='bookSlot'),
			url(r'^sort/', student_search.sort, name='sort')
		])),
		url(r'^schedule/', include([
			url(r'^student_schedule/', include([
				url(r'^$', student_schedule.schedule, name='schedule'),
				url(r'^bookingInfo/', student_schedule.bookingInfo, name='bookingInfo'),
				url(r'^cancelSlot/', student_schedule.cancelTimeSlot, name='cancelSlot'),
				url(r'^reviewSlot/', student_schedule.reviewTimeSlot, name='reviewSlot'),
				url(r'^submitReview/', student_schedule.submitReview, name='submitReview'),
			])),
			url(r'^tutor_schedule/', include([
				url(r'^$', tutor_schedule.schedule, name='schedule'),
				url(r'^bookingInfo/', tutor_schedule.bookingInfo, name='bookingInfo'),
				url(r'^activate/', tutor_schedule.activate, name='activate'),
				url(r'^deactivate/', tutor_schedule.deactivate, name='deactivate'),
			])),
		])),
	])),
]


# scheduler = BackgroundScheduler()
# job = scheduler.add_job(manage, 'interval', seconds=60)
# scheduler.configure(timezone=utc)
# scheduler.start()
