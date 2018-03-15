import Defines as dfn
import os

def init_file():
	
	# Create the output folder if necessary
	if not os.path.exists(dfn.output_dir):
		os.makedirs(dfn.output_dir)
	
	with open(dfn.output_dir + 'report.txt', 'w') as f:
		f.write('############################ \n') # Header
		f.write('### MAMEM Phase 2 Report ### \n') # Header
		f.write('############################ \n\n') # Header
	
def print_line(*args):
	with open(dfn.output_dir + 'report.txt', 'a') as f:
		for arg in args:
			f.write(str(arg))
		f.write('\n')