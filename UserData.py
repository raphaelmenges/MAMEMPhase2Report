import Keys
import Helpers as hlp
import Report as rp
from functools import reduce
from operator import getitem

class UserData():

	# Initialization
	def __init__(self, data, setup_date):
		
		# Private members
		self._data = data # dict pointer
		self._setup_date = setup_date
		
		### Metrics #############################################################
		self.nickname = self._get_data(Keys.nickname)
		#########################################################################
		
		# Calculate further metrics
		self._calc_general_metrics()
		self._calc_start_metrics()
		self._calc_page_acitivity_metrics()
		
	# Selfreport
	def self_report(self):
		
		# Some on-the-fly computations
		latest_start = hlp.from_date_string_to_date(self._get_data(Keys.start_list, self._get_data(Keys.start_count)-1, 'date'))
		
		# Do written report
		rp.print_line("Nickname: ", self.nickname)
		rp.print_line("Setup Date: ", self._setup_date)
		rp.print_line("Start Count: ", self.start_count)
		rp.print_line("Latest Start: ", latest_start)
		rp.print_line("Total Active Hours (in Web): ", self.total_active_hours)
		rp.print_line("Bookmarks Adding Count: ", self.bookmark_adding_count)
	
	### Calculations ###
	
	# Go over general metrics
	def _calc_general_metrics(self):
		
		# List of 'key' and 'count' pairs
		general_metrics = [
				['bookmarkAdding', 0],
				['bookmarkUsage', 0],
				['goBackUsage', 0],
				['goForwardUsage', 0],
				['historyUsage', 0],
				['pause', 0],
				['tabClosing', 0],
				['tabCreation', 0],
				['tabReloading', 0],
				['tabSwitching', 0],
				['unpause', 0],
				['urlInput', 0]]
		
		# Go over general metrics
		for idx in range(len(general_metrics)):
			
			# Check, whether metric key exists in general struct
			metric_key = general_metrics[idx][0]
			general_dict = self._data['general']
			if metric_key in general_dict:
				
				# Check whether data recording is ok
				metric_dict = general_dict[metric_key]
				if type(metric_dict) is dict:
				
					# Go over entries in metric struct
					for key, entry in metric_dict.items():
						if key != 'count': # there is alway one count entry that we ignore
							
							# Barrier to ignore before-setup data
							if self._after_setup(entry['date']):
								
								# Update count
								general_metrics[idx][1] += 1
								
								# TODO: update metric specific values
							
		# Make a dictionary out of the list
		general_metrics_dict = dict(general_metrics)
		
		### Metrics #############################################################
		self.bookmark_adding_count = general_metrics_dict['bookmarkAdding']
		self.bookmark_usage_count = general_metrics_dict['bookmarkUsage']
		self.go_back_usage_count = general_metrics_dict['goBackUsage']
		self.go_forward_usage_count = general_metrics_dict['goForwardUsage']
		self.history_usage_count = general_metrics_dict['historyUsage']
		self.pause_count = general_metrics_dict['pause']
		self.tab_closing_count = general_metrics_dict['tabClosing']
		self.tab_creation_count = general_metrics_dict['tabCreation']
		self.tab_reloading_count = general_metrics_dict['tabReloading']
		self.tab_switching_count = general_metrics_dict['tabSwitching']
		self.unpause_count = general_metrics_dict['unpause']
		self.url_input_count = general_metrics_dict['urlInput']
		#########################################################################
						
	# Go over starts
	def _calc_start_metrics(self):
		
		### Metrics #############################################################
		self.start_count = 0
		self.daily_use = {} # day: {start_count, active_hours};
		# day encoded as d-m-Y string; active_hours filled in _calc_page_acitivity_metrics
		#########################################################################
		
		# Go over start structs
		for key, start in self._data['general']['start'].items():
			if key != 'count': # there is alway one count entry that we ignore
				
				# Barrier to ignore before-setup data
				if self._after_setup(start['date']):
					
					# Update count
					self.start_count += 1
					
					# Update daily use
					day_string = hlp.from_date_to_day_string(hlp.from_date_string_to_date(start['date']))
					if day_string in self.daily_use:
						self.daily_use[day_string]['start_count'] += 1
					else:
						self.daily_use[day_string] = {'start_count': 1, 'active_hours': 0.0 }
					
	# Total time in front of eye tracker TODO: make this method more abstract, like above
	def _calc_page_acitivity_metrics(self):
		
		### Metrics #############################################################
		self.total_active_hours = 0.0
		self.run_time_hours_per_start = [0.0] * self._get_data(Keys.start_count) # taking here the count of starts in database, including pre-setup. Those will have run-time of zero
		#########################################################################
		
		# Go over page activity items 
		if 'pageActivity' in self._data:
			for activity, sessions in self._data['pageActivity'].items():
				
				# Go into sessions
				for session in sessions['sessions']:
					
					# Barrier to ignore empty data point and before-setup data
					if (session is not None) and (self._after_setup(session['startDate'])):
						
						# Some pre-computations
						active_hours = session['durationUserActive'] / (60.0 * 60.0)
						
						# Update total active hours
						self.total_active_hours +=  active_hours # from seconds to hours
						
						# Update daily use
						day_string = hlp.from_date_to_day_string(hlp.from_date_string_to_date(session['startDate']))
						if day_string in self.daily_use:
							self.daily_use[day_string]['active_hours'] += active_hours
							
						# Update run time per start
						self.run_time_hours_per_start[session['startIndex']] += session['durationInForeground']  / (60.0 * 60.0)
	
	####################
	
	# Check whether date was after setup
	def _after_setup(self, date_string):
		return hlp.from_date_string_to_date(date_string) >= self._setup_date
	
	# Get data by key path into nested dict structure. Accepts additional custom keys
	def _get_data(self, key_path, *args):
		copy_path = list(key_path) # copy keys
		for arg in args: # append custom keys
			copy_path.append(str(arg))
		return reduce(getitem, copy_path, self._data)