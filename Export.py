import Defines as dfn
import Helpers as hlp
import csv

# Export accumulated data per user
def accumulated_data_per_user(user_data_list):
	fieldnames = ['id', 'start_count', 'run_time_hours']
	with open(dfn.output_dir + 'users.csv', 'w', newline='') as csvfile:
		output = csv.DictWriter(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
		output.writeheader()
		
		# Go over users
		for user_data in user_data_list:
			
			# Write user data
			output.writerow({'id': user_data.mid, 'start_count': user_data.start_count, 'run_time_hours': user_data.total_run_time_hours})
			
# Export different daily use metrics per user
def daily_use_per_user(user_data_list):
	
	# Get days of the experiment as range
	daily_use_dates = []
	for user_data in user_data_list:
		for day_string in user_data.daily_use.keys():
			daily_use_dates.append(hlp.from_day_string_to_date(day_string)) # convert date string back to datetime
	daily_use_dates = list(set(daily_use_dates)) # make datetimes unique
	daily_use_dates.sort() # sort datetimes
	min_date = daily_use_dates[0]
	max_date = daily_use_dates[-1]
	date_range = list(hlp.date_range(min_date, max_date, include_end=True))
	date_range_string_list =  [str(x.day) + '/' + str(x.month) for x in date_range]

	# TODO: char_input_count / char_input_seconds
	
	# Do it for all metrics
	metrics = ['active_hours', 'session_count', 'page_count', 'char_input_count', 'click_count']
	for metric in metrics:
		
		# Print progress
		print('.', end='')
		
		# Open file to write to
		with open(dfn.output_dir + metric + '.csv', 'w', newline='') as csvfile:
			output = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			
			# Write header
			output.writerow([metric] + date_range_string_list)
			
			# Go over users
			for user_data in user_data_list:
				
				# Go over complete range of days and look for data
				metric_value_dict = {}
				for date in date_range:
					
					# Check whether data is available for date
					day_string = hlp.from_date_to_day_string(date)
					if day_string in user_data.daily_use: # take available data
						metric_value_dict[day_string] = user_data.daily_use[day_string][metric]
					else:
						metric_value_dict[day_string] = 0 # float('nan') # take fallback
				
				# Bring metric values into list
				metric_value_list = []
				for key in metric_value_dict.keys():
					metric_value_list.append(metric_value_dict[key])
				
				# Write user data
				output.writerow([user_data.mid] + metric_value_list)