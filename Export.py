import Defines as dfn
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