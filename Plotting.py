import Helpers as hlp
import Defines as dfn
import matplotlib.pyplot as plt

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
	
	# y-axis, displaying the participants
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