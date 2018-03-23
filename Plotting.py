import Helpers as hlp
import Defines as dfn
import matplotlib.pyplot as plt
import numpy as np

# Bar chart showing recalibrations
def recalibrations(user_data_list):
	
	# Collect data
	nicknames = []
	recalibration_counts = []
	recalibration_with_drift_map_counts = [] 
	for user_data in user_data_list:
		
		# Aggregate data per user
		recalibration_count = 0
		recalibration_with_drift_map_count = 0
		for (start_index, count, drift_map) in user_data.recalibrations_per_start:
			if drift_map:
				recalibration_with_drift_map_count += count
			else:
				recalibration_count += count
		
		# Append data
		nicknames.append(user_data.nickname)
		recalibration_counts.append(recalibration_count)
		recalibration_with_drift_map_counts.append(recalibration_with_drift_map_count)
	
	# Plot data
	fig = plt.figure()
	ax = plt.gca()
	ax.set_axisbelow(True)
	plt.grid(True, axis='y')
	plt.xticks(range(len(nicknames)), nicknames, rotation=45)
	plt.title('Recalibration Counts')
	ind = np.arange(len(nicknames))
	width = 0.4
	bar_recalibration = plt.bar(ind - (width / 2.0), recalibration_counts, width, color="darkgreen")
	bar_recalibration_with_drift_map = plt.bar(ind + (width / 2.0), recalibration_with_drift_map_counts, width, color="lightgreen")
	ax.legend((bar_recalibration[0], bar_recalibration_with_drift_map[0]), ('No Drift Map', 'Drift Map'))
	fig.savefig(dfn.output_dir + 'recalibration_counts' + dfn.plot_format, bbox_inches='tight')

# Bar chart showing youtube foreground hours
def youtube_hours(user_data_list):
	
	# Collect data
	nicknames = []
	active_hours = []
	foreground_hours = []
	run_time_hours = []
	for user_data in user_data_list:
		nicknames.append(user_data.nickname)
		active_hours.append(user_data.youtube_active_hours)
		foreground_hours.append(user_data.youtube_foreground_hours)
		run_time_hours.append(user_data.youtube_run_time_hours)
	
	# Plot data
	fig = plt.figure()
	ax = plt.gca()
	ax.set_axisbelow(True)
	plt.grid(True, axis='y')
	plt.xticks(range(len(nicknames)), nicknames, rotation=45)
	plt.title('YouTube Hours')
	bar_run_time = plt.bar(range(len(nicknames)), run_time_hours, 0.5, color="black")
	bar_foregound = plt.bar(range(len(nicknames)), foreground_hours, 0.5, color="darkgreen")
	bar_active = plt.bar(range(len(nicknames)), active_hours, 0.5, color="lightgreen")
	ax.legend((bar_run_time[0], bar_foregound[0], bar_active[0]), ('Run Time', 'Foreground', 'Active'))
	fig.savefig(dfn.output_dir + 'youtube_hours' + dfn.plot_format, bbox_inches='tight')

# Bar chart showing day time of starts
def start_day_times(user_data_list):
	
	# Count starts per day time hour
	bins = [0] * 24
	for user in user_data_list:
		for (hour, minute, second) in user.start_day_times:
			bins[hour] += 1
	
	# Plot it
	fig = plt.figure()
	ax = plt.gca()
	ax.set_axisbelow(True)
	plt.grid(True)
	plt.title('Day Times of Starts')
	plt.bar(range(24), bins, 0.5, color="lightgreen")
	fig.savefig(dfn.output_dir + 'start_day_times' + dfn.plot_format, bbox_inches='tight')

# Scatter plot about run times after each start
def run_time_after_each_start(user_data_list):
	
	# Prepare plotting
	fig = plt.figure()
	ax = plt.gca()
	
	# y-axis, displaying the users
	plt.yticks(range(len(user_data_list)), [x.nickname for x in user_data_list])
	
	# Data
	plot_data_x = []
	plot_data_y = []
	for idx, user in enumerate(user_data_list): # go over users
		for hours in user.run_time_hours_per_start: # go over run times
			
			# Ignore zero run time
			if hours <= 0:
				continue
			
			# Attach
			plot_data_x.append(hours) # run time hours
			plot_data_y.append(idx) # just the user index
			
	# Grid
	plt.rc('grid', linestyle='dashed', color='grey')
	ax.set_axisbelow(True)
	plt.grid(True)
	
	# Plot it
	plt.title('Run Times After Start in Hours')
	plt.scatter(plot_data_x,plot_data_y,s=25, color='lightgreen')
	fig.savefig(dfn.output_dir + 'run_times_after_each_start' + dfn.plot_format, bbox_inches='tight')
	
# Scatter plot about active time after each start
def active_hours_after_each_start(user_data_list):
	
	# Prepare plotting
	fig = plt.figure()
	ax = plt.gca()
	
	# y-axis, displaying the users
	plt.yticks(range(len(user_data_list)), [x.nickname for x in user_data_list])
	
	# Data
	plot_data_x = []
	plot_data_y = []
	for idx, user in enumerate(user_data_list): # go over users
		for hours in user.active_hours_per_start: # go over active hours
			
			# Ignore zero run time
			if hours <= 0:
				continue
			
			# Attach
			plot_data_x.append(hours) # active hours
			plot_data_y.append(idx) # just the user index
			
	# Grid
	plt.rc('grid', linestyle='dashed', color='grey')
	ax.set_axisbelow(True)
	plt.grid(True)
	
	# Plot it
	plt.title('Active Hours After Start')
	plt.scatter(plot_data_x,plot_data_y,s=25, color='lightgreen')
	fig.savefig(dfn.output_dir + 'active_hours_after_each_start' + dfn.plot_format, bbox_inches='tight')

# Plot general metrics counts across users as bar chart
def general_metrics_counts(user_data_list):
	
	# Collect data
	nicknames = []
	counts = {
			'bookmarkAdding': ['bookmark_adding_count', 'Bookmark Adding Count', []],
			'bookmarkUsage': ['bookmark_usage_count', 'Bookmark Usage Count', []],
			'goBackUsage': ['go_back_usage_count', 'Go Back Usage Count', []],
			'goForwardUsage': ['go_forward_usage_count', 'Go Forward Usage Count', []],
			'historyUsage': ['history_usage_count', 'Histroy Usage Count', []],
			'pause': ['pause_count', 'Pause Count', []],
			'tabClosing': ['tab_closing_count', 'Tab Closing Count', []],
			'tabCreation': ['tab_creation_count', 'Tab Creation Count', []],
			'tabReloading': ['tab_reloading_count', 'Tab Reloading Count', []],
			'tabSwitching': ['tab_switching_count', 'Tab Switching Count', []],
			'unpause': ['unpause_count', 'Unpause Count', []],
			'urlInput': ['url_input_count', 'URL Input Count', []]}
	for user_data in user_data_list:
		nicknames.append(user_data.nickname)
		counts['bookmarkAdding'][2].append(user_data.bookmark_adding_count)
		counts['bookmarkUsage'][2].append(user_data.bookmark_usage_count)
		counts['goBackUsage'][2].append(user_data.go_back_usage_count)
		counts['goForwardUsage'][2].append(user_data.go_forward_usage_count)
		counts['historyUsage'][2].append(user_data.history_usage_count)
		counts['pause'][2].append(user_data.pause_count)
		counts['tabClosing'][2].append(user_data.tab_closing_count)
		counts['tabCreation'][2].append(user_data.tab_creation_count)
		counts['tabReloading'][2].append(user_data.tab_reloading_count)
		counts['tabSwitching'][2].append(user_data.tab_switching_count)
		counts['unpause'][2].append(user_data.unpause_count)
		counts['urlInput'][2].append(user_data.url_input_count)
	
	# Plot all global metrics
	for key, item in counts.items():
		fig = plt.figure()
		ax = plt.gca()
		ax.set_axisbelow(True)
		plt.grid(True)
		plt.xticks(range(len(nicknames)), nicknames, rotation=45)
		plt.title('Global Metrics: ' + item[1])
		plt.bar(range(len(nicknames)), item[2], 0.5, color="lightgreen")
		fig.savefig(dfn.output_dir + item[0] + dfn.plot_format, bbox_inches='tight')
		print('.', end='')
	
# Daily usage plot
def daily_use(user_data_list):
	
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
	plt.xticks(range(len(date_range)), [str(x.day) + '/' + str(x.month) for x in date_range], rotation=45)
	
	# y-axis, displaying the users
	y = range(len(user_data_list))
	plt.yticks(range(len(user_data_list)), [x.nickname for x in user_data_list])
	
	# Data
	plot_data_x = []
	plot_data_y = []
	for idx, user in enumerate(user_data_list): # go over users
		for day_string, use in user.daily_use.items(): # go over daily use of user
			
			# Gather coordinate
			x = (hlp.from_day_string_to_date(day_string) - min_date).days # dates since start of experiment used as index in x-axis
			y = idx # just the user index
			
			# Render big dot
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
	plt.title('Daily Usage - Start Count (bold) and Active Hours (in Web)')
	plt.scatter(plot_data_x,plot_data_y,s=175, color='lightgreen')
	fig.savefig(dfn.output_dir + 'daily_usage' + dfn.plot_format, bbox_inches='tight')