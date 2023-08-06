# __init__.py

import pip

def install(package):
    pip.main(['install', package])

# Example
if __name__ == '__main__':
    install('numpy')
    install('matplotlib')
    install('pandas')

import os, sys
modules_lib = os.path.join(os.path.dirname(__file__), "modules")
if not modules_lib in sys.path:
    sys.path.append(modules_lib) # adds the modules folder to available folders for importing modules
    sys.path.append(os.path.dirname(__file__)) # adds the modules folder to available folders for importing modules

from wrappers import TraceCalls
from find_tools import findfile, findfiles
from prf_plot_tools import extract_out_file, calculate_size, excluded_regions
from prf_plot_tools import prepare_refinement_result, extract_pcr_file
from plot_prf import main as plot_prf
