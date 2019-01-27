import Defines as dfn
import Helpers as hlp
from collections import OrderedDict
import csv
from collections import Counter
import operator

# Export information about domains
def domain_infos(user_data_list):
	
	# Sort domains by frequencies
	domain_frequency = Counter({})
	for user_data in user_data_list:
		domain_frequency = domain_frequency + Counter(user_data.domain_frequency)
	domain_frequency_list = sorted(domain_frequency.items(), key=operator.itemgetter(1))
	domain_frequency_list.reverse()
	
	# Collect information for each domain
	domain_activity = OrderedDict()
	
	# Go over sorted domains
	for item in domain_frequency_list:
		domain = item[0] # get domain name
		
		# Go over domains as stored per user
		for user_data in user_data_list:
			for key, value in user_data.domain_activity.items():
				
				# Check whether it is sorted domain
				if(key == domain):
					if domain in domain_activity:
						domain_activity[domain]['frequency'] += value['frequency']
						domain_activity[domain]['page_count'] += value['page_count']
						domain_activity[domain]['active_hours'] += value['active_hours']
						domain_activity[domain]['stay_count'] += value['stay_count']
					else:
						domain_activity[domain] = {'frequency': value['frequency'], 'page_count': value['page_count'], 'active_hours': value['active_hours'], 'stay_count': value['stay_count'] }
	# Print to CSV
	with open(dfn.output_dir + 'domains.csv', 'w', newline='') as csvfile:
		output = csv.DictWriter(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, fieldnames=['domain', 'visits', 'page_count', 'active_hours', 'stay_count'])
		output.writeheader()
		
		for domain, info in domain_activity.items():
			output.writerow({'domain': domain, 'visits': info['frequency'], 'page_count': info['page_count'], 'active_hours': info['active_hours'], 'stay_count': info['stay_count']})
			

# Export accumulated data per user
def accumulated_data_per_user(user_data_list):
	fieldnames = [
			'id', 'start_count', 'run_time_hours', 'total_active_hours',
			'bookmarkAdding', 'bookmarkUsage', 'goBackUsage', 'goForwardUsage',
			'historyUsage', 'pause', 'tabClosing', 'tabCreation', 'tabReloading',
			'tabSwitching', 'unpause', 'urlInput']
	with open(dfn.output_dir + 'users.csv', 'w', newline='') as csvfile:
		output = csv.DictWriter(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
		output.writeheader()
		
		# Go over users
		for user_data in user_data_list:
			
			# Write user data
			output.writerow({
					'id': user_data.mid, 'start_count': user_data.start_count, 'run_time_hours': user_data.total_run_time_hours, 'total_active_hours': user_data.total_active_hours,
					'bookmarkAdding': user_data.bookmark_adding_count, 'bookmarkUsage': user_data.bookmark_usage_count, 'goBackUsage': user_data.go_back_usage_count, 'goForwardUsage': user_data.go_forward_usage_count,
					'historyUsage': user_data.history_usage_count, 'pause': user_data.pause_count, 'tabClosing': user_data.tab_closing_count, 'tabCreation': user_data.tab_creation_count, 'tabReloading': user_data.tab_reloading_count,
					'tabSwitching': user_data.tab_switching_count, 'unpause': user_data.unpause_count, 'urlInput': user_data.url_input_count})
			
# Export different daily use metrics per user
def daily_use_per_user(user_data_list):
	
	# Get days of the experiment as range
	date_range = hlp.date_range_from_user_data_list(user_data_list)
	date_range_string_list =  [str(x.day) + '/' + str(x.month) for x in date_range]
	
	# Do it for all social tasks of the users
	for task in dfn.social_tasks.keys():
		
		# Do it for all metrics per task
		task_metrics = ['active_hours', 'session_count', 'page_count', 'char_input_count', 'seconds_per_char', 'click_count', 'domain_count']
		for metric in task_metrics:
			
			# Print progress
			print('.', end='')
			
			# Open file to write to
			with open(dfn.output_dir + task + '_' + metric + '.csv', 'w', newline='') as csvfile:
				output = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
				
				# Write header
				output.writerow([task + '_' + metric] + date_range_string_list)
				
				# Go over users to write rows
				for user_data in user_data_list:
					
					# Go over complete range of days and look for data
					metric_value_dict = OrderedDict()
					for date in date_range:
						
						# Check whether data is available for date
						day_string = hlp.from_date_to_day_string(date)
						if day_string in user_data.daily_use: # take available data
							
							# Decide on action per metric
							if metric == 'seconds_per_char':
								
								# Seconds per character
								char_input_count = user_data.daily_use[day_string][task]['char_input_count']
								if char_input_count > 0:
									metric_value_dict[day_string] = float(user_data.daily_use[day_string][task]['char_input_seconds']) / char_input_count
								else:
									metric_value_dict[day_string] = float('nan') # take fallback
							elif metric == 'domain_count':
								metric_value_dict[day_string] = len(user_data.daily_use[day_string][task]['domains'])
							else:
								# Other metric
								metric_value_dict[day_string] = user_data.daily_use[day_string][task][metric]
						else:
							
							# Decide on action per metric
							if metric == 'seconds_per_char':
								metric_value_dict[day_string] = float('nan') # take fallback
							elif metric == 'active_hours' or metric == 'seconds_per_char':
								metric_value_dict[day_string] = 0.0 # take fallback
							else:
								metric_value_dict[day_string] = 0 # take fallback
					
					# Bring metric values into list (which fits the dates in header)
					metric_value_list = []
					for key in metric_value_dict.keys():
						metric_value_list.append(metric_value_dict[key])
					
					# Write user data
					output.writerow([user_data.mid] + metric_value_list)
					
	# Do it for the most visited domain which are not social tasks
	domain_metrics = ['frequency', 'page_count', 'active_hours', 'char_input_count', 'click_count']

	# Go over users to write files about activity on non-social domains
	for user_data in user_data_list:
	
		# Print progress
		print('.', end='')
		
		# Open file to write to
		with open(dfn.output_dir + 'non_social_' + user_data.mid + '.csv', 'w', newline='') as csvfile:
			output = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			
			# Write header
			output.writerow(['non_social_' + user_data.mid] + domain_metrics)
			
			# Go over all domains
			for domain, activity in user_data.domain_activity_non_social_task.items():
				
				# Collect row
				row = [domain]
				for metric in domain_metrics:
					row.append(activity[metric])
			
				# Write domain data
				output.writerow(row)