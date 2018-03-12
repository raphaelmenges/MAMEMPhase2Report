import UserData as ud
import Report as rp
import Defines as dfn
import json

# TODO
# Ignore datapoints before setup time
# Tell in header about creation of report / last datapoint / count of users etc.

### Global Variables ###

user_data_list = []

### Program ###

with open('mamem-phase2-fall17-export.json', encoding='utf-8') as data_file:
	
	# Load dataset into list of users
	data = json.load(data_file)
	
	# Go over users in data set
	for uid, user in data['users'].items():
		
		# Check whether user is participant
		name = user['userDetails']['nickname']
		if any(name in x for x in dfn.user_filter): # go over users and check existence
			user_data_list.append(ud.UserData(user))
			
	# Sort user data list
	user_data_list.sort();
	
	# Initialize report
	rp.init_file()
	
	# First, report details about each user
	rp.print_line("### Individual Users") # line to separate users
	rp.print_line("---")
	for user_data in user_data_list:
		user_data.self_report()
		rp.print_line("---")