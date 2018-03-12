### User Data Class ###

import Keys
import Helpers as hlp
import Report as rp

from functools import reduce
from operator import getitem

class UserData():

	# Initialization
	def __init__(self, data, setup_date):
		self._data = data # dict pointer
		self._setup_date = setup_date
		
	# Selfreport
	def self_report(self):
		rp.print_line("Nickname: ", self._get_data(Keys.nickname))
		rp.print_line("Setup Date: ", self._setup_date)
		rp.print_line("Start Count: ", self._count_starts())
		# rp.print_line("Latest Start: ", hlp.to_date(self._get_data(Keys.start_list, self._get_data(Keys.start_count)-1, 'date')))
		rp.print_line("Total Active Hours (in Web): ", self._total_active_hours())
	
	### Calculations ###
	
	# Count starts
	def _count_starts(self):
		start_count = 0
		for key, start in self._data['general']['start'].items():
			if key != 'count': # there is alway one count entry that we ignore
				if self._after_setup(start['date']): # only count starts after setup
					start_count += 1
		return start_count
	
	# Total time in front of eye tracker
	def _total_active_hours(self):
		total_active_hours = 0.0
		if 'pageActivity' in self._data:
			for page, activity in self._data['pageActivity'].items():
				for session in activity['sessions']:
					
					# Barrier to ignore before-setup data
					if self._after_setup(session['startDate']):
						total_active_hours += session['durationUserActive'] / (60.0 * 60.0) # from seconds to hours
					
		return total_active_hours
	
	####################
	
	# Check whether date was after setup
	def _after_setup(self, date_string):
		return hlp.to_date(date_string) >= self._setup_date
	
	# Get data by key path into nested dict structure. Accepts additional custom keys
	def _get_data(self, key_path, *args):
		copy_path = list(key_path) # copy keys
		for arg in args: # append custom keys
			copy_path.append(str(arg))
		return reduce(getitem, copy_path, self._data)
	
	# Comparator for sorting
	def __lt__(self, other):
		return self._get_data(Keys.nickname) < other._get_data(Keys.nickname)