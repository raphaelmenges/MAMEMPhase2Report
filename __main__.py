import UserData as ud
import Report as rp
import Defines as dfn
import Helpers as hlp
import json
import datetime
import matplotlib.pyplot as plt

### Global Variables ###

user_data_list = []

### Program ###

with open('mamem-phase2-fall17-export.json', encoding='utf-8') as data_file:
	
	# Load dataset into list of users
	data = json.load(data_file)
	
	# Go over users in data set
	print('Processing of users', end='')
	for uid, user in data['users'].items():
		
		# Check whether user is participant
		nickname = user['userDetails']['nickname']
		for x in dfn.user_filter: # go over participants
			if nickname == x.nickname: # nickname matches
				print('.', end='')
				user_data_list.append(ud.UserData(user, x.setup_date))
	print('finished.')
			
	# Sort user data list
	user_data_list.sort();
	
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
	
	# x-axis, displaying the date range
	fig = plt.figure()
	ax = plt.gca()
	plt.xticks(range(len(date_range)), date_range)
	plt.xticks(rotation=90)
	
	# y-axis, displaying the participants
	y = range(len(user_data_list))
	plt.yticks(range(len(user_data_list)), [x.nickname for x in user_data_list])
	
	# Data
	plot_data_x = []
	plot_data_y = []
	for idx, user in enumerate(user_data_list): # go over users
		for day_string, use in user.daily_use.items(): # go over daily use of user
			x = (hlp.from_day_string_to_date(day_string) - min_date).days # dates since start of experiment used as index in x-axis
			y = idx # just the user index
			plot_data_x.append(x)
			plot_data_y.append(y)
			
			# Start count
			ax.annotate(str(use['start_count']), (x,y),
			   ha="center", va="bottom", size=7, weight='bold')
			
			# Active hours
			ax.annotate(format(use['active_hours'], '.2f'), (x,y),
			   ha="center", va="top", size=5)
	
	# Grid
	plt.rc('grid', linestyle='dashed', color='grey')
	ax.set_axisbelow(True)
	plt.grid(True)
	
	# Plot it
	plt.title('Daily Usage - Start Count (bold) and Active Hours')
	plt.scatter(plot_data_x,plot_data_y,s=175, color='lightgreen')
	fig.savefig(dfn.output_dir + 'daily_usage' + dfn.plot_format, bbox_inches='tight')