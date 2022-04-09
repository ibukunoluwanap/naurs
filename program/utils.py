from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import ProgramModel

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter classes by day
	def formatday(self, day, classes):
		classes_per_day = classes.filter(start_time__day=day)
		d = ''
		for _class in classes_per_day:
			d += f'<li> <b>{_class.title}</b> by <b>{_class.start_time.hour}:{_class.start_time.minute}</b> </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, classes):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, classes)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter classes by year and month
	def formatmonth(self, withyear=True):
		classes = ProgramModel.objects.filter(start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, classes)}\n'
		return cal