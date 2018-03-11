import json

# TODO
# Count of starts
# Last startups
# Time of active use

### Parameters ###

output_dir = './output/'

### User Filter ###

user_filter = ['sheba1']

### Global Variables ###

user_list = []

### Output ###

# Create output textfile
report = open(output_dir + 'report.txt', 'w')
report.write('MAMEM Phase 2 Report\n')

# Print output
def print_output(line):
	report.write(line + '\n')
	
###########

class UserData():

	# Initialization
	def __init__(self, data):
		self.data = data

# Load dataset into list of users
with open('mamem-phase2-fall17-export.json', encoding='utf-8') as data_file:
	data = json.load(data_file)
	
	# Go over users
	for uid, user in data['users'].items():
		
		# Check whether user is participant
		name = user['userDetails']['nickname']
		if any(name in x for x in user_filter): # go over users and check existence
			user_list.append(user)