import json

# Parameters
output_dir = './output/'

# Open dataset
with open('mamem-phase2-fall17-export.json', encoding='utf-8') as data_file:    
	data = json.load(data_file)

	# Open output
	with open(output_dir + 'report.txt', 'w') as report:
		report.write('MAMEM Phase 2 Report\n')
		for k,v in data.items():
			report.write(k)