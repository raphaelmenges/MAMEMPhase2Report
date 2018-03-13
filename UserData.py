### User Data Class ###

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
		self._calc_start_metrics()
		self._calc_page_acitivity_metrics()
		
	# Selfreport
	def self_report(self):
		
		# Some on-the-fly computations
		latest_start = hlp.to_date_DMYHMS(self._get_data(Keys.start_list, self._get_data(Keys.start_count)-1, 'date'))
		
		# Do written report
		rp.print_line("Nickname: ", self.nickname)
		rp.print_line("Setup Date: ", self._setup_date)
		rp.print_line("Start Count: ", self.start_count)
		rp.print_line("Latest Start: ", latest_start)
		rp.print_line("Total Active Hours (in Web): ", self.total_active_hours)
	
	### Calculations ###
	
	# Go over starts
	def _calc_start_metrics(self):
		
		### Metrics #############################################################
		self.start_count = 0
		self.daily_use_starts = {} # day:count; day encoded as d-m-Y string
		#########################################################################
		
		# Go over start structs
		for key, start in self._data['general']['start'].items():
			if key != 'count': # there is alway one count entry that we ignore
				if self._after_setup(start['date']): # barrier to include only after-setup data
					
					# Update count
					self.start_count += 1
					
					# Update daily use
					date = hlp.to_date_DMYHMS(start['date'])
					day = str(date.day) + '-' + str(date.month) + '-' + str(date.year)
					if day in self.daily_use_starts:
						self.daily_use_starts[day] += 1
					else:
						self.daily_use_starts[day] = 1
					
	# Total time in front of eye tracker TODO: make this method more abstract, like above
	def _calc_page_acitivity_metrics(self):
		
		### Metrics #############################################################
		self.total_active_hours = 0.0
		#########################################################################
		
		# Go over page activity entries 
		if 'pageActivity' in self._data:
			for page, activity in self._data['pageActivity'].items():
				
				# Go over session per activitiy (email, shopping, etc.)
				for session in activity['sessions']:
					
					# Barrier to ignore before-setup data
					if self._after_setup(session['startDate']):
						
						# Update total active hours
						self.total_active_hours += session['durationUserActive'] / (60.0 * 60.0) # from seconds to hours
	
	####################
	
	# Check whether date was after setup
	def _after_setup(self, date_string):
		return hlp.to_date_DMYHMS(date_string) >= self._setup_date
	
	# Get data by key path into nested dict structure. Accepts additional custom keys
	def _get_data(self, key_path, *args):
		copy_path = list(key_path) # copy keys
		for arg in args: # append custom keys
			copy_path.append(str(arg))
		return reduce(getitem, copy_path, self._data)
	
	# Comparator for sorting
	def __lt__(self, other):
		return self._get_data(Keys.nickname) < other._get_data(Keys.nickname)