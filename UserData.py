import Keys
import Helpers as hlp
import Report as rp
import datetime
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
		
		# Calculate metrics used for computations of other metrics
		self._calc_required_metrics()
		
		# Calculate further metrics
		self._calc_general_metrics()
		self._calc_start_metrics()
		self._calc_calibration_metrics()
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
	
	# Calculate required metrics
	def _calc_required_metrics(self):
		
		### Metrics #############################################################
		self.start_dates = {} # key is start index, value is dict of start date and end date
		#########################################################################
		
		# Fill starts
		for key, start in self._data['general']['start'].items():
			if key != 'count': # there is always one count entry that we ignore
				
				# Helpers
				date = hlp.from_date_string_to_date(start['date'])
				
				# Store data about start
				self.start_dates[key] = {'start': date, 'end': date}
				
		# Go over page activity data and search of "oldest" entries for each end
		if 'pageActivity' in self._data:
			for activity, sessions in self._data['pageActivity'].items():
				
				# Go into sessions
				for session in sessions['sessions']:
					
					# Barrier to ignore empty data point
					if (session is not None):
					
						# End date for this session
						end_date = hlp.from_date_string_to_date(session['endDate'])
						
						# Get start index of this session
						start_index = session['startIndex']
						
						# Decide on update of end date
						if end_date > self.start_dates[str(start_index)]['end']:
							self.start_dates[str(start_index)]['end'] = end_date
						
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
						if key != 'count': # there is always one count entry that we ignore
							
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
		self.start_day_times = [] # triples of hour, minute and second
		#########################################################################
		
		# Go over start structs
		for key, start in self._data['general']['start'].items():
			if key != 'count': # there is always one count entry that we ignore
				
				# Barrier to ignore before-setup data
				if self._after_setup(start['date']):
					
					# Helpers
					date = hlp.from_date_string_to_date(start['date'])
					
					# Update count
					self.start_count += 1
					
					# Update daily use
					day_string = hlp.from_date_to_day_string(date)
					if day_string in self.daily_use:
						self.daily_use[day_string]['start_count'] += 1
					else:
						self.daily_use[day_string] = {'start_count': 1, 'active_hours': 0.0 }
						
					# Update start day times
					self.start_day_times.append((date.hour, date.minute, date.second))
					
	# Calculate metrics about calibrations
	def _calc_calibration_metrics(self):
		
		# Helpers
		calibration_counts = [0]* self._get_data(Keys.start_count)
		
		### Metrics #############################################################
		self.recalibrations_per_start = [] # triple of start index, re(!)calibration count and whether drift map was used
		self.calibration_life_times = [] # list of dicts holding start index, calibration life time in hours, drift map usage
		#########################################################################
		
		# Go over starts and collect calibrations
		for key, calibration in self._data['general']['recalibration'].items(): # naming in data structure bad....
			if key != 'count': # there is always one count entry that we ignore
				
				# Barrier to ignore before-setup data
				if self._after_setup(calibration['date']):
					
					# Helpers
					start_index = calibration['startIndex']
					life_time = (self.start_dates[str(start_index)]['end'] - self.start_dates[str(start_index)]['start'])
					life_time_days, life_time_seconds = life_time.days, life_time.seconds
					life_time_hours = life_time_days * 24.0 + life_time_seconds / 3600.0
					
					# Increase counts of recalibration
					calibration_counts[start_index] += 1
					
					# Set calibration life times list entries
					self.calibration_life_times.append(
							{'start_index': start_index,
							'life_time_hours': life_time_hours,
							'drift_map': self._data['general']['start'][str(start_index)]['useDriftMap']})
					
		# Filter all entries with zero count (either before setup or people exited the system)
		for start_index, count in enumerate(calibration_counts):
			if(count >= 1): # zero means there was no calibration for this start, at all
				self.recalibrations_per_start.append((start_index, count-1, self._data['general']['start'][str(start_index)]['useDriftMap'])) # re(!)calibrations, subtracting one
		
	# Total time in front of eye tracker TODO: make this method more abstract, like above
	def _calc_page_acitivity_metrics(self):
		
		### Metrics #############################################################
		self.total_active_hours = 0.0
		self.run_time_hours_per_start = [0.0] * self._get_data(Keys.start_count) # taking here the count of starts in database, including pre-setup. Those will have run-time of zero
		self.active_hours_per_start = [0.0] * self._get_data(Keys.start_count) # similar as for run time
		self.youtube_active_hours = 0.0
		self.youtube_foreground_hours = 0.0
		self.youtube_run_time_hours = 0.0
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
						self.run_time_hours_per_start[session['startIndex']] += session['durationInForeground'] / (60.0 * 60.0) # accumulation of foreground should give runtime
						self.active_hours_per_start[session['startIndex']] += session['durationUserActive'] / (60.0 * 60.0)
						
						# Go over pages
						for page in session['pages']:
							if 'youtube.com/watch?v=' in page['url']:
								self.youtube_active_hours += page['durationUserActive'] / (60.0 * 60.0)
								self.youtube_foreground_hours += page['durationInForeground'] / (60.0 * 60.0)
								self.youtube_run_time_hours += page['duration'] / (60.0 * 60.0)
	
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