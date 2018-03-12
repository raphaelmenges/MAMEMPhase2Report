### Helpers ###

import datetime

def to_date(date_string):
	return datetime.datetime.strptime(date_string, "%d-%m-%Y %H-%M-%S")