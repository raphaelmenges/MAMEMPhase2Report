import collections
import datetime

### (Social) Tasks with corresponding keywords in domain ###
social_tasks = {
		'general' : [''],
		'facebook' : ['facebook.com', 'facebook.co.il', 'he-il.facebook.com', 'facebook.gr'],
		'twitter' : ['twitter.com', 'twitter.co.il'],
		'instagram' : ['instagram.com'],
		'youtube' : ['youtube.com', 'youtu.be'],
		'email' : ['mail.ru', 'live.com', 'outlook.live.com', 'mail.google.com', 'mail.yahoo.com', 'mail.walla.co.il', 'webmail01.uoa.gr']
		}

### Parameters ###

output_dir = './output/'
plot_format = ".pdf"

### User Filter ###

# Tuple of nickname and date of setup
User = collections.namedtuple('User', 'uid mid setup_date')
user_filter = [
		
		# Sheba users
		User('IsDen2M469alN7dZwCQtDRwqCGx1', 'sheba 1',  datetime.datetime(2018, 2, 28, 9,  0,  0)),
		User('tVOpuSf1OqdES7eZYh306SFiAgi1', 'sheba 2',  datetime.datetime(2018, 3, 2,  9,  0,  0)),
		User('R1YrNUybBGYxXYwMuqU4iqOEUdv1', 'sheba 3',  datetime.datetime(2018, 3, 1,  13, 0,  0)),
		User('ch1tPHbBgXVgGDw3U9CIno4Y1zl2', 'sheba 4',  datetime.datetime(2018, 3, 8,  13, 0,  0)),
		User('gZsrgnQLDodXkSrfwhZNNdN1bo73', 'sheba 5',  datetime.datetime(2018, 3, 6,  18, 0,  0)),
		User('xK99Udpta0R7sVHqzediybTJyk82', 'sheba 6',  datetime.datetime(2018, 3, 25, 12, 30, 0)),
		User('2kEYr9d57fZlIuqr24iUFkPgT1q2', 'sheba 7',  datetime.datetime(2018, 3, 26, 13, 0,  0)),
		User('4cUfumadS2bekRC6absIbm6r4EU2', 'sheba 8',  datetime.datetime(2018, 4, 3,  12, 30, 0)),
		User('9RtuZr7hejbKhRzQ4ujYCWpgiV53', 'sheba 9',  datetime.datetime(2018, 4, 9,  14, 0,  0)),
		User('k5qaRZ6HWeZRakZ48UP878TUQBU2', 'sheba10', datetime.datetime(2018, 4, 30, 13, 0,  0)),
		
		# MDA users
		User('Et6iZrHVAEMX8cLFv3ZdkGCoDXO2', 'mda 1',  datetime.datetime(2018, 3, 6,  11, 0,  0)),
		User('S2LlwONjtjdCqT9KHwfrlpgRzQC2', 'mda 2',  datetime.datetime(2018, 3, 7,  10, 0,  0)),
		User('fb9LcoNkCYRV4YWghICSVuevACi2', 'mda 3',  datetime.datetime(2018, 3, 8,  11, 0,  0)),
		User('LP95iDwWLcN3ocPdycXLpMeyUsW2', 'mda 4',  datetime.datetime(2018, 3, 9,  11, 0,  0)),
		User('M57gA3alSuPwhQPfKIBeIvNXZGb2', 'mda 5',  datetime.datetime(2018, 3, 9,  15, 0,  0)),
		User('gGAxlgXwqKckKwifcOqrhaNJISx2', 'mda 6',  datetime.datetime(2018, 3, 12, 10, 30, 0)),
		User('35gKe9T2HWR2ALkDQx3WZyNzdkB3', 'mda 7',  datetime.datetime(2018, 3, 12, 13, 30, 0)),
		User('CqWBuWtTJoeNbEl82XmfoFnxhs92', 'mda 8',  datetime.datetime(2018, 3, 14, 10, 0,  0)),
		User('72FFMu5qFHeg6DvYKVqNhrKOIcD2', 'mda 9',  datetime.datetime(2018, 3, 14, 15, 30, 0)),
		User('kKNcw6OhBPRScH7Hsef8jDpCIiE3', 'mda10', datetime.datetime(2018, 3, 15, 13, 0,  0)),
		
		# AUTH users
		User('PUfBB1yhJJSCx6OaaBFXmtLtkJ32', 'auth 1',  datetime.datetime(2018, 4, 17, 0, 0,  0)),
		User('siD57H6QaQVmqb57hMT5jVHEo4Q2', 'auth 2',  datetime.datetime(2018, 4, 19, 0, 0,  0)),
		User('R502LmAck2X9lXKaOsbJV4lfuuh1', 'auth 3',  datetime.datetime(2018, 4, 20, 0, 0,  0)),
		User('igPH8ZdGj3ME1ZoYnLRT7s91BDj2', 'auth 4',  datetime.datetime(2018, 4, 26, 0, 0,  0)),
		User('lDg0IeZLPjeKDGGc3o6YrBVy7I42', 'auth 5',  datetime.datetime(2018, 4, 20, 0, 0,  0)),
		User('3sUIPYYLFmOhofvxYoxHctEiRm33', 'auth 6',  datetime.datetime(2018, 4, 22, 0, 0,  0)),
		User('l1pZIRtcMMcFaPxaIOACmJcPWhg1', 'auth 7',  datetime.datetime(2018, 4, 18, 0, 0,  0)),
		User('teSV3bsOaDQvkfunabo7NhncCjq1', 'auth 8',  datetime.datetime(2018, 4, 19, 0, 0,  0)),
		User('BUgwE9grEVVlYDeZmwV2jRWFxcU2', 'auth 9',  datetime.datetime(2018, 4, 25, 0, 0,  0)),
		User('JM0ZNcnNziSAOWnSIkCjxsJ29DF3', 'auth10', datetime.datetime(2018, 4, 27, 0, 0,  0))
		
		]