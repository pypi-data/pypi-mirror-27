import os,sys, re, numpy as np
from find_tools import findfiles

p1 = r"C:\AU-PHD\General Data\Report R1D1\furnaces\Ofurnace\2017-11-01"
path=p1

run_main = 1
def main(path):
    os.chdir(path)
    rass = findfiles(".ras")
    for r in rass:
        dstHandler = re.sub(pattern = "\..+", repl = ".dat", string = r)
        makeDat(r, dstHandler)
        srcName = re.sub(pattern = "\..+", repl = "", string = r)
        dstFolder = os.path.join(os.getcwd(), srcName)
        os.makedirs(dstFolder)
        print(dstFolder)
        srcFiles = [f for f in os.listdir() if f.startswith(srcName) and os.path.isfile(f)]
        for f in srcFiles:
            dst = os.path.join(dstFolder, f)
            print(dst)
            os.rename(f,dst)

    # import pdb; pdb.set_trace()
    # ras = findfile(".ras")
    # df = pd.read_csv(ras,sep = "\s",engine="python",comment="*",names=["2Theta","Counts","none"])
    # df=df.drop("none",axis=1)
    # dat = ras[:-4] + ".dat"
    # df.to_csv(dat,sep="\t", index=False, header = False)

def makeDat(srcHandler, dstHandler):
    """Create a .dat file for Fullprof from a .ras files from Rigaku R1D1 at Aarhus University.

    Args:
        srcHandler: name of .ras file
        dstHandler: name of .dat file

    out:
        .dat file with th/2th values and counts.
    """
    b = np.genfromtxt(
        # skip_header = 356,
        # skip_footer = 3,
        comments = "*",
        unpack = False,
        # unpack = True,
        fname = srcHandler,
        dtype = "|U16", # 16 chars is way more than needed. but hey!
        # names = "a,b,c",
        # usecols = ("a","b")
        )
    # print(b[0::,0:2], type(b))

    np.savetxt(dstHandler,b[0::,0:2], fmt="%s")

if run_main:
    main(path)
