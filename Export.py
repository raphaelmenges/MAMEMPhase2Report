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
	date_range = hlp.date_range_from_user_data_list(user_data_list)
	date_range_string_list =  [str(x.day) + '/' + str(x.month) for x in date_range]
	
	# Do it for all metrics
	metrics = ['active_hours', 'session_count', 'page_count', 'char_input_count', 'seconds_per_char', 'click_count']
	for metric in metrics:
		
		# Print progress
		print('.', end='')
		
		# Open file to write to
		with open(dfn.output_dir + metric + '.csv', 'w', newline='') as csvfile:
			output = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			
			# Write header
			output.writerow([metric] + date_range_string_list)
			
			# Go over users to write rows
			for user_data in user_data_list:
				
				# Go over complete range of days and look for data
				metric_value_dict = {}
				for date in date_range:
					
					# Check whether data is available for date
					day_string = hlp.from_date_to_day_string(date)
					if day_string in user_data.daily_use: # take available data
						
						# Decide on action per metric
						if metric == 'seconds_per_char':
							
							# Seconds per character
							char_input_count = metric_value_dict[day_string] = user_data.daily_use[day_string]['char_input_count']
							if char_input_count > 0:
								metric_value_dict[day_string] = float(user_data.daily_use[day_string]['char_input_seconds']) / char_input_count
							else:
								metric_value_dict[day_string] = float('nan') # take fallback
							
						else:
							
							# Other metric
							metric_value_dict[day_string] = user_data.daily_use[day_string][metric]
						
					else:
						
						# Decide on action per metric
						if metric == 'seconds_per_char':
							metric_value_dict[day_string] = float('nan') # take fallback
						else:
							metric_value_dict[day_string] = 0 # take fallback
				
				# Bring metric values into list (which fits the dates in header)
				metric_value_list = []
				for key in metric_value_dict.keys():
					metric_value_list.append(metric_value_dict[key])
				
				# Write user data
				output.writerow([user_data.mid] + metric_value_list)