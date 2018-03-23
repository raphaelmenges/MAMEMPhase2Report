import UserData as ud
import Report as rp
import Defines as dfn
import Plotting as plt
import json
import datetime

with open('mamem-phase2-fall17-export.json', encoding='utf-8') as data_file:
	
	# Load dataset into list of users
	data = json.load(data_file)
	
	# Go over users in data set and store participants of MAMEM
	user_data_list = []
	print('Processing of users', end='')
	for uid, user in data['users'].items():
		
		# Check whether user is participant
		nickname = user['userDetails']['nickname']
		for x in dfn.user_filter: # go over participants
			if nickname == x.nickname: # nickname matches
				print('.', end='')
				user_data_list.append(ud.UserData(user, x.setup_date))
	print('finished.')
	
	# Sort user data list same as filter list
	sorted_user_data_list = []
	for user in dfn.user_filter:
		for user_data in user_data_list:
			if user_data.nickname == user.nickname:
				sorted_user_data_list.append(user_data)
				break
	user_data_list = sorted_user_data_list
	
	# Initialize report
	rp.init_file()
	
	# General information
	rp.print_line('Generation Date: ', datetime.datetime.now())
	rp.print_line('User Count: ', len(user_data_list))
	rp.print_line('')
	
	# Individual information
	print('Reporting individual users', end='')
	rp.print_line("### Individual Users") # line to separate users
	rp.print_line("---")
	for user_data in user_data_list:
		user_data.self_report()
		rp.print_line("---")
		print('.', end='')
	print('finished.')
		
	### Plotting
	print('Plotting', end='')
	plt.recalibrations(user_data_list)
	print('.', end='')
	plt.youtube_hours(user_data_list)
	print('.', end='')
	plt.start_day_times(user_data_list)
	print('.', end='')
	plt.run_time_after_each_start(user_data_list)
	print('.', end='')
	plt.active_hours_after_each_start(user_data_list)
	print('.', end='')
	plt.daily_use(user_data_list)
	print('.', end='')
	plt.general_metrics_counts(user_data_list)
	print('.', end='')
	print('finished.')