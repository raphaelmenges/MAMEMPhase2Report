### Helpers ###

import datetime

def to_date_DMYHMS(date_string):
	return datetime.datetime.strptime(date_string, "%d-%m-%Y %H-%M-%S")

def to_date_DMY(date_string):
	return datetime.datetime.strptime(date_string, "%d-%m-%Y")

def date_range(start_date, end_date, include_end = False):
	end = int(include_end)
	for ordinal in range(start_date.toordinal(), end_date.toordinal() + end):
		yield datetime.date.fromordinal(ordinal)