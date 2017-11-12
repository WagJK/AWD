class Calendar():
	# dict timeslots: TimeInterval timeslots[D][H][M]
	def __init__(self, range_day, range_hour, range_minute):
		self.timeslots = {}
		for day in range_day:
			self.timeslots[day] = {}
			for hour in range_hour:
				self.timeslots[day][hour] = {}
				for minute in range_minute:
					self.timeslots[day][hour][minute] = TimeInterval(day, hour, minute)

	def next(self, ts):
		if ts.M == 0:
			return self.timeslots[ts.D][ts.H][30]
		else:
			return self.timeslots[ts.D][ts.H+1][0]


class TimeInterval():
	'''
	int startH: starting hour
	int startM: starting minute
	bool state: if it is booked
	bool disable: if it should be displayed
	bool extend: if it should be extended
	'''
	def __init__(self, day, hour, minute, state=False):
		self.D = day
		self.H = hour
		self.M = minute
		self.state = state
		self.disable = False
		self.extend = False

	def __str__(self):
		if self.M == 0:
			return str(self.H) + ":00 - " + str(self.H) + ":30"
		else:
			return str(self.H) + ":30 - " + str(self.H + 1) + ":00"