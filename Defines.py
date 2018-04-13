import collections
import datetime

### Parameters ###

output_dir = './output/'
plot_format = ".pdf"

### User Filter ###

# Tuple of nickname and date of setup
User = collections.namedtuple('User', 'uid setup_date')
user_filter = [
		
		# Sheba users
		User('IsDen2M469alN7dZwCQtDRwqCGx1', datetime.datetime(2018, 2, 28, 9,  0,  0)),
		User('tVOpuSf1OqdES7eZYh306SFiAgi1', datetime.datetime(2018, 3, 2,  9,  0,  0)),
		User('R1YrNUybBGYxXYwMuqU4iqOEUdv1', datetime.datetime(2018, 3, 1,  13, 0,  0)),
		User('ch1tPHbBgXVgGDw3U9CIno4Y1zl2', datetime.datetime(2018, 3, 8,  13, 0,  0)),
		User('gZsrgnQLDodXkSrfwhZNNdN1bo73', datetime.datetime(2018, 3, 6,  18, 0,  0)),
		User('xK99Udpta0R7sVHqzediybTJyk82', datetime.datetime(2018, 3, 25, 12, 30, 0)),
		User('2kEYr9d57fZlIuqr24iUFkPgT1q2', datetime.datetime(2018, 3, 26, 13, 0,  0)),
		User('4cUfumadS2bekRC6absIbm6r4EU2', datetime.datetime(2018, 3, 1,  12, 0,  0)), # TODO: need setup date
		User('9RtuZr7hejbKhRzQ4ujYCWpgiV53', datetime.datetime(2018, 3, 1,  12, 0,  0)), # TODO: need setup date
		
		# MDA users
		User('Et6iZrHVAEMX8cLFv3ZdkGCoDXO2', datetime.datetime(2018, 3, 6,  11, 0,  0)),
		User('S2LlwONjtjdCqT9KHwfrlpgRzQC2', datetime.datetime(2018, 3, 7,  10, 0,  0)),
		User('fb9LcoNkCYRV4YWghICSVuevACi2', datetime.datetime(2018, 3, 8,  11, 0,  0)),
		User('LP95iDwWLcN3ocPdycXLpMeyUsW2', datetime.datetime(2018, 3, 9,  11, 0,  0)),
		User('M57gA3alSuPwhQPfKIBeIvNXZGb2', datetime.datetime(2018, 3, 9,  15, 0,  0)),
		User('gGAxlgXwqKckKwifcOqrhaNJISx2', datetime.datetime(2018, 3, 12, 10, 30, 0)),
		User('35gKe9T2HWR2ALkDQx3WZyNzdkB3', datetime.datetime(2018, 3, 12, 13, 30, 0)),
		User('CqWBuWtTJoeNbEl82XmfoFnxhs92', datetime.datetime(2018, 3, 14, 10, 0,  0)),
		User('72FFMu5qFHeg6DvYKVqNhrKOIcD2', datetime.datetime(2018, 3, 14, 15, 30, 0)),
		User('kKNcw6OhBPRScH7Hsef8jDpCIiE3', datetime.datetime(2018, 3, 15, 13, 0,  0))]