from datetime import datetime
from datetime import time
from datetime import timedelta

class Calendar():
	# dict timeslots: TimeInterval timeslots[D][H][M]
	def __init__(self, range_date, range_hour, private_tutor=False):
		self.timeslots = {}
		for day in range(len(range_date)):
			self.timeslots[day] = {}
			for hour in range_hour:
				self.timeslots[day][hour] = {}
				if private_tutor:
					self.timeslots[day][hour][0] = TimeInterval(day, range_date[day], hour, 0, extend=True)
					self.timeslots[day][hour][30] = TimeInterval(day, range_date[day], hour, 30, disable=True)
				else:
					self.timeslots[day][hour][0] = TimeInterval(day, range_date[day], hour, 0)
					self.timeslots[day][hour][30] = TimeInterval(day, range_date[day], hour, 30)
					

	def next(self, ts):
		if ts.minute == 0:
			return self.timeslots[ts.day][ts.hour][30]
		else:
			return self.timeslots[ts.day][ts.hour+1][0]


class TimeInterval():
	'''
	datetime time: date
	int day: starting day
	int hour: starting hour
	int minute: starting minute
	bool state: if it is in model.Timeslot
	bool activate: if it can be activated by tutor
	bool disable: if it should be displayed
	bool extend: if it should be extended
	'''
	def __init__(self, day, date, hour, minute, state=False, disable=False, extend=False):
		self.day = day
		self.hour = hour
		self.minute = minute
		self.time = datetime.combine(date, time(hour, minute))
		self.time_str = self.time.strftime("%Y-%m-%d %H:%M:%S")
		self.state = state
		self.disable = disable
		self.extend = extend
		if datetime.now() + timedelta(days = 1) < self.time:
			self.activate = True
		else:
			self.activate = False

	def __str__(self):
		if self.minute == 0:
			return str(self.hour) + ":00 - " + str(self.hour) + ":30"
		else:
			return str(self.hour) + ":30 - " + str(self.hour + 1) + ":00"