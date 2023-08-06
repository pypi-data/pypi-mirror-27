
import os, sys, subprocess
"""adding path to look for modules"""
sys.path.append(r"C:\AU-PHD\General Data\_Python\modules")
from find_tools import findfile, findfiles, findfolders

p=r"C:\AU-PHD\General Data\Report R1D1\flow synthesis\FEN_F8-11_HH"
run_main = 0

def run_single_refinement():
    """automated single frame rietveld refinement with Fullprof"""
    # command PCRFILE DATFILE OUTLOG
    # Fp2k working_PCR gamma07 pblog
    # command = r'Fp2k working_PCR gamma07 pblog'
    folders = findfolders()
    path = os.getcwd()
    for folder in folders:
        os.chdir(path)
        os.chdir(folder)
        dat = findfile(".dat")
        try:
            seq = findfiles(".seq")
            os.remove(seq)
        except:
            pass
        pcr = findfile(".pcr")
        command = " ".join([
            # 'Fp2k',
            'wfp2k',
            pcr,
            dat,
            'pblog'])
        print("subprocess:", command)
        p = subprocess.Popen(command) # Python interpreter continues to read .py script
        # pppp = subprocess.run(command) # Python interpreter waits to read .py script

        # log = open('pblog.log', 'r') # if I use with open(...) a tap is required to proceed at running time with atom.
        # print("\n\nResult of Refinement:\n")
        # for line in log:
        #     if "error" in line.lower():
        #         print(line)
        #         import pdb; pdb.set_trace()
        #     if "normal end" in line.lower():
        #         print(line)
        # log.close()
if run_main:
    os.chdir(p)
    run_single_refinement()

if __name__ == "__main__":
    print("I am main!")
