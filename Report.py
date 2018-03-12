import json

# TODO
# Count of starts
# Last startups
# Time of active use
# Ignore datapoints before setup time
# Tell in header about creation of report / last datapoint / count of users etc.

### Parameters ###

output_dir = './output/'

### User Filter ###

user_filter = [
		'sheba1', 'sheba2', 'sheba3', 'sheba4', 'sheba5', 'sheba6', 'sheba7', 'sheba8', 'sheba9', 'sheba10',
		'mda1', 'mda2', 'mda3', 'mda4', 'mda5', 'mda6', 'mda7', 'mda8', 'mda9', 'mda10']

### Global Variables ###

user_data_list = []

### Output ###

# Create output textfile
report_file = open(output_dir + 'report.txt', 'w')
report_file.write('############################ \n') # Header
report_file.write('### MAMEM Phase 2 Report ### \n') # Header
report_file.write('############################ \n\n') # Header

# Print line to output
def do_report(*args):
	try:
		for arg in args:
			report_file.write(arg)
		report_file.write('\n')
	except Exception:
		print("Report file not available.")
	
### User Data Class ###

class UserData():

	# Initialization
	def __init__(self, data):
		self._data = data
		
	# Selfreport
	def self_report(self):
		do_report("Nickname: ", self._data['userDetails']['nickname'])
	
	# Comparator for sorting
	def __lt__(self, other):
		return self._data['userDetails']['nickname'] < other._data['userDetails']['nickname']
		
#######################

# Load dataset into list of users
with open('mamem-phase2-fall17-export.json', encoding='utf-8') as data_file:
	data = json.load(data_file)
	
	# Go over users in data set
	for uid, user in data['users'].items():
		
		# Check whether user is participant
		name = user['userDetails']['nickname']
		if any(name in x for x in user_filter): # go over users and check existence
			user_data_list.append(UserData(user))
			
	# Sort user data list
	user_data_list.sort();
			
	# First, report details about each user
	do_report("### Individual Users") # line to separate users
	do_report("---")
	for user_data in user_data_list:
		user_data.self_report()
		do_report("---")
		
### Clean Up ###
report_file.close()