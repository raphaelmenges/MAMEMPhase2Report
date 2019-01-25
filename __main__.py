import UserData as ud
import Report as rp
import Defines as dfn
import Plotting as plt
import Export as ex
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
		for entry in dfn.user_filter: # go over known participants
			if uid == entry.uid: # uid matches
				print('.', end='')
				user_data_list.append(ud.UserData(uid, entry.mid, user, entry.setup_date))
				
	print('finished.')
	
	# Sort user data list same as filter list
	sorted_user_data_list = []
	for entry in dfn.user_filter:
		for user_data in user_data_list:
			if user_data.uid == entry.uid:
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
	rp.print_line("### Individual Users")
	rp.print_line("---")
	for user_data in user_data_list:
		user_data.self_report()
		rp.print_line("---") # line to separate users
		print('.', end='')
	print('finished.')
		
	### Plotting
	print('Plotting', end='')
	# plt.calibration_life_times(user_data_list)
	# print('.', end='')
	# plt.recalibrations(user_data_list)
	# print('.', end='')
	plt.youtube_hours(user_data_list)
	print('.', end='')
	plt.start_day_times(user_data_list)
	print('.', end='')
	# plt.run_time_after_each_start(user_data_list)
	# print('.', end='')
	# plt.active_hours_after_each_start(user_data_list)
	# print('.', end='')
	# plt.daily_use(user_data_list)
	# print('.', end='')
	plt.general_metrics_counts(user_data_list)
	print('.', end='')
	plt.normalized_daily_use(user_data_list)
	print('.', end='')
	# plt.accumulated_normalized_daily_use(user_data_list)
	# print('.', end='')
	print('finished.')
	
	# Export
	print('Export', end='')
	# ex.accumulated_data_per_user(user_data_list)
	# print('.', end='')
	# ex.daily_use_per_user(user_data_list)
	# print('.', end='')
	ex.domain_infos(user_data_list)
	print('.', end='')
	print('finished.')