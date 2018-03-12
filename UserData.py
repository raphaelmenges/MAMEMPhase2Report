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
		rp.print_line("Nickname: ", self.get_data(Keys.nickname))
		rp.print_line("Starts: ", str(self.get_data(Keys.start_count)))
		rp.print_line("Last Start: ", str(hlp.to_date(self.get_data(Keys.start_list, self.get_data(Keys.start_count)-1, 'date'))))
		
	# Get data by key path into nested dict structure. Accepts additional custom keys
	def get_data(self, key_path, *args):
		copy_path = list(key_path) # copy keys
		for arg in args: # append custom keys
			copy_path.append(str(arg))
		return reduce(getitem, copy_path, self._data)
	
	# Comparator for sorting
	def __lt__(self, other):
		return self.get_data(Keys.nickname) < other.get_data(Keys.nickname)