import datetime

def from_date_string_to_date(date_string):
	return datetime.datetime.strptime(date_string, "%d-%m-%Y %H-%M-%S")

def date_range(start_date, end_date, include_end = False):
	end = int(include_end)
	for ordinal in range(start_date.toordinal(), end_date.toordinal() + end):
		yield datetime.datetime.fromordinal(ordinal)

# Converts datetime object to d-m-Y string (mostly used as key for daily activity)
def from_date_to_day_string(date):
	return str(date.day) + '-' + str(date.month) + '-' + str(date.year)

# Converts day string back to date
def from_day_string_to_date(day_string):
	return datetime.datetime.strptime(day_string, "%d-%m-%Y")

# Makes date range from user data list
def date_range_from_user_data_list(user_data_list):
	daily_use_dates = []
	
	# Accumulate dates from all users into sorted list with unique entries
	for user_data in user_data_list:
		for day_string in user_data.daily_use.keys():
			daily_use_dates.append(from_day_string_to_date(day_string)) # convert date string back to datetime
	daily_use_dates = list(set(daily_use_dates)) # make datetimes unique
	daily_use_dates.sort() # sort datetimes
	
	# Make date rnage
	min_date = daily_use_dates[0]
	max_date = daily_use_dates[-1]
	return list(date_range(min_date, max_date, include_end=True))