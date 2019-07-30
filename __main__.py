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
	
	# Accumulate data over all users
	run_time_hours = 0.0
	active_hours = 0.0
	page_count = 0
	char_count = 0
	click_count = 0
	pause_count = 0
	tab_switching_count = 0
	url_input_count = 0
	recalibration_count = 0
	bookmark_adding_count = 0
	for user_data in user_data_list:
		
		# Go over daily use
		for day, use in user_data.daily_use.items():
			active_hours += use['general']['active_hours']
			page_count += use['general']['page_count']
			char_count += use['general']['char_input_count']
			click_count += use['general']['click_count']
			
		# General
		run_time_hours += user_data.total_run_time_hours
		pause_count += user_data.pause_count
		tab_switching_count += user_data.tab_switching_count
		url_input_count += user_data.url_input_count
		bookmark_adding_count += user_data.bookmark_adding_count
		
		# Recalibration
		for item in user_data.recalibrations_per_start:
			recalibration_count += item[1]
	
	rp.print_line('Run Time Hours: ', run_time_hours)
	rp.print_line('Active Hours: ', active_hours)
	rp.print_line('Page Count: ', page_count)
	rp.print_line('Char Input Count: ', char_count)
	rp.print_line('Click Count: ', click_count)
	rp.print_line('Pause Count: ', pause_count)
	rp.print_line('Tab Switching Count: ', tab_switching_count)
	rp.print_line('URL Input Count: ', url_input_count)
	rp.print_line('Recalibration Count: ', recalibration_count)
	rp.print_line('Bookmark Adding Count: ', bookmark_adding_count)
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
	# plt.youtube_hours(user_data_list)
	# print('.', end='')
	# plt.best_youtube_hours(user_data_list)
	# print('.', end='')
	# plt.start_day_times(user_data_list)
	# print('.', end='')
	# plt.run_time_after_each_start(user_data_list)
	# print('.', end='')
	# plt.active_hours_after_each_start(user_data_list)
	# print('.', end='')
	# plt.daily_use(user_data_list)
	# print('.', end='')
	# plt.general_metrics_counts(user_data_list)
	# print('.', end='')
	plt.normalized_daily_use(user_data_list)
	print('.', end='')
	# plt.accumulated_normalized_daily_use(user_data_list)
	# print('.', end='')
	plt.active_hours_over_time(user_data_list, "MDA 1")
	print('.', end='')
	plt.active_hours_over_time(user_data_list, "MDA 5")
	print('.', end='')
	plt.active_hours_over_time(user_data_list, "MDA 2")
	print('.', end='')
	plt.active_hours_over_time(user_data_list, "AUTH 10")
	print('.', end='')
	print('finished.')
	
	# Export
	# print('Export', end='')
	# ex.accumulated_data_per_user(user_data_list)
	# print('.', end='')
	# ex.daily_use_per_user(user_data_list)
	# print('.', end='')
	# ex.domain_infos(user_data_list)
	# print('.', end='')
	# print('finished.')