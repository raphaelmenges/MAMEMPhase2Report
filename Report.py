### Report Singleton ###

import Defines as dfn

def init_file():
	with open(dfn.output_dir + 'report.txt', 'w') as f:
		f.write('############################ \n') # Header
		f.write('### MAMEM Phase 2 Report ### \n') # Header
		f.write('############################ \n\n') # Header
	
def print_line(*args):
	with open(dfn.output_dir + 'report.txt', 'a') as f:
		for arg in args:
			f.write(arg)
		f.write('\n')