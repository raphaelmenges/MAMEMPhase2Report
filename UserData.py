### User Data Class ###

import Keys
import Helpers as hlp
import Report as rp

from functools import reduce
from operator import getitem

class UserData():

	# Initialization
	def __init__(self, data):
		self._data = data
		
	# Selfreport
	def self_report(self):
		rp.print_line("Nickname: ", self._get_data(Keys.nickname))
		rp.print_line("Starts: ", str(self._get_data(Keys.start_count)))
		rp.print_line("Latest Start: ", str(hlp.to_date(self._get_data(Keys.start_list, self._get_data(Keys.start_count)-1, 'date'))))
		rp.print_line("Total Active Hours: ", str(self._total_active_hours()))
		
	# Get data by key path into nested dict structure. Accepts additional custom keys
	def _get_data(self, key_path, *args):
		copy_path = list(key_path) # copy keys
		for arg in args: # append custom keys
			copy_path.append(str(arg))
		return reduce(getitem, copy_path, self._data)
	
	# Comparator for sorting
	def __lt__(self, other):
		return self._get_data(Keys.nickname) < other._get_data(Keys.nickname)
	
	### Further calculations ###
	
	# Total time in front of eye tracker
	def _total_active_hours(self):
		total_active_hours = 0.0
		if 'pageActivity' in self._data:
			for page, activity in self._data['pageActivity'].items():
				for session in activity['sessions']:
					total_active_hours += session['durationUserActive'] / (60.0 * 60.0) # from seconds to hours
		return total_active_hours
	
	####################