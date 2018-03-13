### Helpers ###

import datetime

def from_date_string_to_date(date_string):
	return datetime.datetime.strptime(date_string, "%d-%m-%Y %H-%M-%S")

def date_range(start_date, end_date, include_end = False):
	end = int(include_end)
	for ordinal in range(start_date.toordinal(), end_date.toordinal() + end):
		yield datetime.date.fromordinal(ordinal)

# Converts datetime object to Y-m-d string (mostly used as key for daily activity)
def from_date_to_day_string(date):
	return str(date.day) + '-' + str(date.month) + '-' + str(date.year)

# Converts day string back to date
def from_day_string_to_date(day_string):
	return datetime.datetime.strptime(day_string, "%d-%m-%Y")
