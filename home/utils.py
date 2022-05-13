from calendar import HTMLCalendar
from home.models import CalendarModel

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter classes by day
	def formatday(self, day, classes):
		classes_per_day = classes.filter(start_at__day=day).order_by("-id")
		d = ''
		for _class in classes_per_day:
			d += f'''
				<li>
					<a href="/dashboard/calendar/duplicate/{_class.id}/" class="d-btn">
						<span data-feather="copy"></span>
					</a>
					<b>Class:</b> {_class.program.title}
					<br>
					<b>Time:</b> {_class.start_at.strftime("%I:%M %p")} - {_class.end_at.strftime("%I:%M %p")}
					<br>
					<b>Instructor:</b> {_class.instructor.user.get_full_name()}
				</li>
			'''

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
		classes = CalendarModel.objects.filter(start_at__year=self.year, start_at__month=self.month).order_by("-id")

		cal = f'<table class="calendar table align-middle table-bordered"\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, classes)}\n'
		return cal