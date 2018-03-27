import collections
import datetime

### Parameters ###

output_dir = './output/'
plot_format = ".pdf"

### User Filter ###

# Tuple of nickname and date of setup
User = collections.namedtuple('User', 'nickname setup_date')
user_filter = [
		
		# Sheba users
		User('sheba1', 	datetime.datetime(2018, 2, 28, 9,  0,  0)),
		User('sheba2', 	datetime.datetime(2018, 3, 2,  9,  0,  0)),
		User('sheba3', 	datetime.datetime(2018, 3, 1,  13, 0,  0)),
		User('sheba4', 	datetime.datetime(2018, 3, 8,  13, 0,  0)),
		User('sheba5', 	datetime.datetime(2018, 3, 6,  18, 0,  0)),
		User('Timor', 		datetime.datetime(2018, 3, 25, 12, 30, 0)), # sheba6 -> think about mapping from "custom nicknames" to something like "user id". Or change nickname later back to sheba6
		User('sheba7', 	datetime.datetime(2018, 3, 26, 13, 0,  0)),
		
		# MDA users
		User('mda1', 		datetime.datetime(2018, 3, 6,  11, 0,  0)),
		User('mda2', 		datetime.datetime(2018, 3, 7,  10, 0,  0)),
		User('mda3', 		datetime.datetime(2018, 3, 8,  11, 0,  0)),
		User('mda4', 		datetime.datetime(2018, 3, 9,  11, 0,  0)),
		User('mda5', 		datetime.datetime(2018, 3, 9,  15, 0,  0)),
		User('mda6', 		datetime.datetime(2018, 3, 12, 10, 30, 0)),
		User('mda7', 		datetime.datetime(2018, 3, 12, 13, 30, 0)),
		User('mda8', 		datetime.datetime(2018, 3, 14, 10, 0,  0)),
		User('mda9', 		datetime.datetime(2018, 3, 14, 15, 30, 0)),
		User('mda10', 		datetime.datetime(2018, 3, 15, 13, 0,  0))]