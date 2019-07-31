import Keys
import Helpers as hlp
import Report as rp
import Defines as dfn
import math
from functools import reduce
from collections import OrderedDict
import operator
import datetime

class UserData():

	# Initialization
	def __init__(self, uid, mid, data, setup_date):
		
		# Private members
		self.uid = uid
		self.mid = mid
		self._data = data # dict pointer
		self._setup_date = setup_date
		
		# Initial metrics
		self.nickname = self._get_data(Keys.nickname)
		
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
		rp.print_line("MAMEM id: ", self.mid)
		rp.print_line("Nickname: ", self.nickname)
		rp.print_line("Google Maps Active Hours: ", self.google_maps_hours)
		'''
		rp.print_line("Setup Date: ", self._setup_date)
		rp.print_line("Start Count: ", self.start_count)
		rp.print_line("Latest Start: ", latest_start)
		rp.print_line("Total Active Hours (in Web): ", self.total_active_hours)
		rp.print_line("Total Active Hours (in Web with Drift Map): ", self.total_active_hours_drift_map)
		active_hours_drift_map_percentage = 0.0
		if self.total_active_hours > 0:
			active_hours_drift_map_percentage = self.total_active_hours_drift_map / self.total_active_hours
		rp.print_line("Active Hours with Drift Map in Percentage (in Web): ", active_hours_drift_map_percentage)
		rp.print_line("Bookmarks Adding Count: ", self.bookmark_adding_count)
		'''
	
		# Report about number of clicks
		click_sum = 0
		for day, value in self.daily_use.items():
			click_sum += value['general']['click_count']
		rp.print_line("Click Count: ", click_sum)
			
		# Report about: how many tries per attempt have been necessary to click something specific
		agg_click_tries = 0
		click_attempts_count = 0
		agg_click_tries_drift_map = 0
		click_attempts_count_drift_map = 0
		for day, value in self.daily_use.items():
			
			for click_attempts in value['general']['clicks_per_attempt']:
				for click_try in click_attempts:
					agg_click_tries += click_try # count of tries per attempt
				click_attempts_count += len(click_attempts) # count of attempts
				
			for click_attempts in value['general']['clicks_per_attempt_drift_map']:
				for click_try in click_attempts:
					agg_click_tries_drift_map += click_try # count of tries per attempt
				click_attempts_count_drift_map += len(click_attempts) # count of attempts
				
		if click_attempts_count > 0:
			rp.print_line("Average Tries per Click Attempt: ", agg_click_tries / click_attempts_count)
			
		if click_attempts_count_drift_map > 0:
			rp.print_line("Average Tries per Click Attempt With Drift Map: ", agg_click_tries_drift_map / click_attempts_count_drift_map)
	
	### Calculations ###
	
	# Calculate required metrics
	def _calc_required_metrics(self):
		
		### Metrics #############################################################
		self.start_dates = {} # key is start index, value is dict of start date and end date
		self.domain_frequency = {} # dictionary storing domain and visit frequency
		self.domain_activity = OrderedDict() # ordered dict of domain and dict about frequency, page_count,
		# active_hours, char_input_count, click_count, stay_count, further filled in _calc_page_acitivity_metrics
		self.daily_use = {} # day: {start_count,
		# task: {active_hours, session_count, page_count, char_input_count, char_input_seconds, click_count, clicks_per_attempt, clicks_per_attempt_drift_map, domains} };
		# day encoded as d-m-Y string; further filled in _calc_start_metrics and _calc_page_acitivity_metrics
		#########################################################################
		
		# List of all start and end dates
		date_list = []
		
		# Fill starts
		for key, start in self._data['general']['start'].items():
			if key != 'count': # there is always one count entry that we ignore
				
				# Helpers
				date = hlp.from_date_string_to_date(start['date'])
				
				# Store data about start
				self.start_dates[key] = {'start': date, 'end': date}
				
				# Remember date
				date_list.append(date)
				
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
							
						# Extract domain if date is within range
						if self._check_date(session['startDate']):
							domain = session['domain']
							
							# Update domain frequency
							if domain in self.domain_frequency:
								self.domain_frequency[domain] += 1
							else:
								self.domain_frequency[domain] = 1
							
						# Remember end date
						date_list.append(end_date)
							
		# Handle domain frequency
		domain_frequency_list = sorted(self.domain_frequency.items(), key=operator.itemgetter(1))
		domain_frequency_list.reverse()
		
		for domain, frequency in domain_frequency_list:
			self.domain_activity[domain] = {'frequency' : frequency, 'active_hours' : 0.0, 'page_count' : 0, 'char_input_count' : 0, 'click_count' : 0, 'stay_count' : 0}
			
		# Initialize daily use
		date_list.sort()
		for date in hlp.date_range(date_list[0], date_list[-1], True):
			
			day_string = hlp.from_date_to_day_string(date)
			self.daily_use[day_string] = {'start_count': 0}
						
			# Create metrics for every social task (like general, facebook...)
			for task in dfn.social_tasks.keys():
				self.daily_use[day_string][task] = {
						'active_hours': 0.0,
						'session_count': 0,
						'page_count': 0,
						'char_input_count': 0,
						'char_input_seconds': 0.0,
						'click_count': 0,
						'clicks_per_attempt': [],
						'clicks_per_attempt_drift_map': [],
						'domains': []}
			
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
			
			# Check, whether metric key exists in general struct from Firebase
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
							if self._check_date(entry['date']):
								
								# Update count
								general_metrics[idx][1] += 1
							
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
		self.start_day_times = [] # triples of hour, minute and second
		#########################################################################
		
		# Go over start structs
		for key, start in self._data['general']['start'].items():
			if key != 'count': # there is always one count entry that we ignore
				
				# Barrier to ignore before-setup data
				if self._check_date(start['date']):
					
					# Helpers
					date = hlp.from_date_string_to_date(start['date'])
					
					# Update count
					self.start_count += 1
					
					# Update daily use
					day_string = hlp.from_date_to_day_string(date)
					self.daily_use[day_string]['start_count'] += 1
					
					# Update start day times
					self.start_day_times.append((date.hour, date.minute, date.second))
					
	# Calculate metrics about calibrations
	def _calc_calibration_metrics(self):
		
		# Helpers
		calibration_counts = [0] * self._get_data(Keys.start_count)
		
		### Metrics #############################################################
		self.recalibrations_per_start = [] # triple of start index, re(!)calibration count and whether drift map was used
		self.calibration_life_times = [] # list of dicts holding start index, calibration life time in hours, drift map usage
		#########################################################################
		
		# Go over starts and collect calibrations
		for key, calibration in self._data['general']['recalibration'].items(): # naming in data structure bad....
			if key != 'count': # there is always one count entry that we ignore
				
				# Barrier to ignore before-setup data
				if self._check_date(calibration['date']):
					
					# TODO: count active time with calibration
					
					# Helpers
					start_index = calibration['startIndex']
					rum_time = (self.start_dates[str(start_index)]['end'] - self.start_dates[str(start_index)]['start'])
					rum_time_days, rum_time_seconds = rum_time.days, rum_time.seconds
					run_time_hours = rum_time_days * 24.0 + rum_time_seconds / 3600.0
					
					# Increase counts of recalibration
					calibration_counts[start_index] += 1
					
					# Set calibration life times list entries
					self.calibration_life_times.append(
							{'start_index': start_index,
							'run_time_hours': run_time_hours,
							'drift_map': self._data['general']['start'][str(start_index)]['useDriftMap']})
					
		# Filter all entries with zero count (either before setup or people exited the system)
		for start_index, count in enumerate(calibration_counts):
			if(count >= 1): # zero means there was no calibration for this start, at all
				self.recalibrations_per_start.append((start_index, count-1, self._data['general']['start'][str(start_index)]['useDriftMap'])) # re(!)calibrations, subtracting one
		
	# Go over page activity
	def _calc_page_acitivity_metrics(self):
		
		### Metrics #############################################################
		self.total_active_hours = 0.0
		self.total_active_hours_drift_map = 0.0
		self.total_run_time_hours = 0.0 # total run time in hours without training
		self.run_time_hours_per_start = [0.0] * self._get_data(Keys.start_count) # taking here the count of starts in database, including pre-setup. Those will have run-time of zero
		self.active_hours_per_start = [0.0] * self._get_data(Keys.start_count) # similar as for run time
		self.youtube_active_hours = 0.0
		self.youtube_foreground_hours = 0.0
		self.youtube_hours = 0.0
		self.google_maps_hours = 0.0
		self.domain_activity_non_social_task = OrderedDict()
		#########################################################################
		
		# Go over page activity items 
		if 'pageActivity' in self._data:
			for activity, sessions in self._data['pageActivity'].items():
				
				# Go into sessions
				for session in sessions['sessions']:
					
					# Barrier to ignore empty data point and before-setup data
					if (session is not None) and (self._check_date(session['startDate'])):
						
						# Extract domain
						domain = session['domain']
						
						# Some pre-computations
						active_hours = session['durationUserActive'] / (60.0 * 60.0) # from seconds to hours
						
						# Update total active hours
						self.total_active_hours += active_hours
						
						# Update total active hours with drift map
						drift_map_active = self._data['general']['start'][str(session['startIndex'])]['useDriftMap']
						if drift_map_active:
							self.total_active_hours_drift_map += active_hours
						
						# Update daily use
						day_string = hlp.from_date_to_day_string(hlp.from_date_string_to_date(session['startDate']))
						
						### Daily use ###
						
						# Go over tasks
						for task, keywords in dfn.social_tasks.items():
							
							# Check whether domain contains the keyword for specific task
							session_belongs_to_task = False
							for keyword in keywords:
								session_belongs_to_task = session_belongs_to_task or keyword in domain
							
							# If session belongs to specified task, add metrics measurement
							if session_belongs_to_task:
								
								# Active hours
								self.daily_use[day_string][task]['active_hours'] += active_hours
								
								# Session count
								self.daily_use[day_string][task]['session_count'] += 1
								
								# Page count
								self.daily_use[day_string][task]['page_count'] += session['pageCount']
								
								# Domains
								if domain not in self.daily_use[day_string][task]['domains']:
									self.daily_use[day_string][task]['domains'].append(domain)
									
						#################
						
						### Domain activity ###
						
						self.domain_activity[domain]['active_hours'] += active_hours
						
						self.domain_activity[domain]['page_count'] += session['pageCount']
						
						if active_hours > 1/60.0:
							self.domain_activity[domain]['stay_count'] += 1
						
						#######################
							
						# Update total run time
						runtime_hours = session['durationInForeground'] / (60.0 * 60.0) # accumulation of foreground should give runtime (without training)
						self.total_run_time_hours += runtime_hours
							
						# Update run time per start
						self.run_time_hours_per_start[session['startIndex']] += runtime_hours
						self.active_hours_per_start[session['startIndex']] += active_hours
						
						# Go over pages
						for page in session['pages']:
							
							### Daily use ###
							
							# Go over tasks
							for task, keywords in dfn.social_tasks.items():
								
								# Check whether domain contains the keyword for specific task
								session_belongs_to_task = False
								for keyword in keywords:
									session_belongs_to_task = session_belongs_to_task or keyword in domain
								
								# If session belongs to specified task, add metrics measurement
								if session_belongs_to_task:
								
									# Check for text input
									if 'textInputs' in page:
										
										# Go over text input entries
										for text_input in page['textInputs']:
											
											# Character distance
											char_input_count = text_input['charDistance']
										
											# Character input count
											self.daily_use[day_string][task]['char_input_count'] += char_input_count
											
											# Duration of character input
											if char_input_count > 0:
												self.daily_use[day_string][task]['char_input_seconds'] += text_input['duration']
									
									# Check for clicks
									if 'clicks' in page:
										
										# Euclidean distance
										def distance(p0, p1):
											return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
										
										# Collect click coordinates on page
										coords = []
										for click in page['clicks']:
											coord = click['coord'].split(',')
											coords.append([float(coord[0]), float(coord[1])])
										
										# Count how many tries have been used to attempt a click
										click_tries = []
										curr_click_try = 1
										last_coord = []
										for i in range(len(coords)):
											if i > 0:
												dist = distance(coords[i], last_coord)
												if dist == 0:
													curr_click_try += 0 # ignore if distance is zero
												elif dist < 50:
													curr_click_try += 1
												else:
													click_tries.append(curr_click_try)
													curr_click_try = 1
											last_coord = coords[i]
										click_tries.append(curr_click_try)

										# Clicks
										if drift_map_active: # drift map
											self.daily_use[day_string][task]['clicks_per_attempt_drift_map'].append(click_tries)
										else: # no drift map
											self.daily_use[day_string][task]['clicks_per_attempt'].append(click_tries)
										
										# Go over click entries
										for click in page['clicks']:
									
											# Click count
											self.daily_use[day_string][task]['click_count'] += 1
							
							#################
							
							### Domain activity ###
							
							# Check for text input
							if 'textInputs' in page:
								
								# Go over text input entries
								for text_input in page['textInputs']:
									
									self.domain_activity[domain]['char_input_count'] += text_input['charDistance']
									
							# Check for clicks
							if 'clicks' in page:
								
								# Go over click entries
								for click in page['clicks']:
									
									self.domain_activity[domain]['click_count'] += 1
									
							#######################
							
							# Update YouTube
							if 'youtube.com/watch?v=' in page['url']:
								self.youtube_active_hours += page['durationUserActive'] / (60.0 * 60.0)
								self.youtube_foreground_hours += page['durationInForeground'] / (60.0 * 60.0)
								self.youtube_hours += page['duration'] / (60.0 * 60.0)
								
							# Update Google Maps
							if 'google.com/maps' in page['url']:
								self.google_maps_hours += page['durationUserActive'] / (60.0 * 60.0)
		
		# Filter social tasks from domain activity
		for domain, activity in self.domain_activity.items():
			domain_is_social_task = False
			
			# Go over tasks
			for task, keywords in dfn.social_tasks.items():
				
				# Skip general task, as it accumulates everything and applies for all domains
				if task == 'general':
					continue
				
				# Check whether domain contains the keyword for specific task
				for keyword in keywords:
					domain_is_social_task = domain_is_social_task or keyword in domain
					
			# Only consider domains that are not in social tasks
			if not domain_is_social_task:
				self.domain_activity_non_social_task[domain] = activity
	
	# Check whether date was after setup and before end of considered trial time
	def _check_date(self, date_string):
		after_setup = hlp.from_date_string_to_date(date_string) >= self._setup_date
		before_end = hlp.from_date_string_to_date(date_string) <= self._setup_date + datetime.timedelta(days=30)
		return after_setup and before_end
	
	# Get data by key path into nested dict structure. Accepts additional custom keys
	def _get_data(self, key_path, *args):
		copy_path = list(key_path) # copy keys
		for arg in args: # append custom keys
			copy_path.append(str(arg))
		return reduce(operator.getitem, copy_path, self._data)