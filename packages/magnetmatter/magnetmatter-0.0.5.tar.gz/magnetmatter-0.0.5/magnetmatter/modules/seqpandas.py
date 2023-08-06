import os, numpy as np, pandas as pd, sys, re

from wrappers import TraceCalls
from datetime import datetime
from find_tools import findfile, findfiles

def natural_keys(text):
    """ returns a list of char and digit groups

    HOW  TO USE:
        alist.sort(key=natural_keys)"""
    atoi = lambda c: int(c) if c.isdigit() else c
    return [ atoi(c) for c in re.split('(\d+)', text) ]

# """ wrapper function """
# def time_response(func):
#     """ add @TraceCalls() in front of definitions of functions.
#     Adds printing and timetaking of function calls.
#
#     Is great for detecting infinite loops in a specific function. """
#     def function_wrapper(*args, **kwargs):
#         t1 = datetime.now()
#         print("#### " + func.__name__ + " ####")
#         res = func(*args, **kwargs)
#         # print(res)
#         t2 = datetime.now()
#         print(func.__name__, "took", t2-t1, "(hh:mm:ss.decimals)")
#         return res
#     return function_wrapper

""" helper function for consistent index preparation """
def to_append(sys = None, pcr = None, phase = None, var = None, vals = None):
    """ function to avoid bugs regarding appending to dataframes.
    The order of arguments is not important.
    Returns consistent order."""
    to_append = [sys, pcr, phase, var] + list(vals)
    return to_append

def find_time_zero():
    first_frame = min(os.listdir(r"..\tset"))
    with open(os.path.join(r"..\tset",first_frame), "r") as reading:
        for line in reading:
            if "Date='" in line:
                # lambda=  2.45750, T= 302.402, dT=  0.080, Date='2017-09-05 19:33:40'
                return datetime.strptime(re.search("Date='(.+)'",line).group(1), "%Y-%m-%d %H:%M:%S")

def generate_csv(path, df_init):
    """ combining mic_pandas and seq_pandas
    These extract information from sequenial refinement
    from Fullprof output files."""
    os.chdir(path)
    seq_pandas(path, df_init)
    mic_pandas(path, df_init)

@TraceCalls()
def read_csv(path):
    """ reads all found CSVs in a path
    returns a combined pd.dataframe-object """
    os.chdir(path)
    CSVs = [pd.read_csv(f) for f in findfiles(".csv")]

    df = _clean_csv(CSVs)
    return df

@TraceCalls()
def _clean_csv(*args):
    """ reads in pandas dataframe and sorts the columns.
    We assume that the same PCR file
    has been used to do the sequential refinement.
    otherwise the sorting will not be correct
    (the columns will not be the same)"""
    args = args[0]
    df = args[0]
    """appending remaining dataframes"""
    if len(args) > 1:
        for arg in args[1:]:
            cur_df = arg.append(df, ignore_index = True)
            df = cur_df
    """sort column values"""
    columns = df.columns.values
    columns = sorted(columns, key= natural_keys)
    df = df[columns]
    rev_columns = [columns[-i] for i in range(1,5)]
    # import pdb; pdb.set_trace()
    """ why no comment here??"""
    df = df.set_index(rev_columns).reset_index().drop_duplicates().sort_index()
    """ the result of above line: all values are strings.
    we remedy this in the next line:"""
    df.iloc[2:,4:] = df.iloc[2:,4:].astype(float)
    return df

@TraceCalls()
def sort_numbered_strings(files):
    """Sorts and return a string list with alphanumerical characters.

    Args:
        files: Takes a list of strings that containts alphanumerical characters.

    Returns:
        Ordered list of the alphanumerical strings.

    REASON:
        The built-in .sort() does not sort correctly, eg:
            frame60.dat, frame10.dat, frame100.dat
        come in the order
            frame10.dat, frame100.dat, frame60.dat
        which is obvious incorrect.

    """
    int_ending = [re.sub("\D+(\d+).*","\g<1>",f) for f in files]
    int_ending = np.array(int_ending, dtype=np.int32)
    ordered_indices = np.argsort(int_ending)
    files = np.array(files)[ordered_indices].tolist()
    return files

@TraceCalls()
def get_pcr():
    """Returns the full path to the shortest .pcr in current working folder."""
    pcrs = findfiles(".pcr")
    pcr = min(pcrs,key=len)
    return pcr


@TraceCalls()
def get_phase_names():
    """Returns a list of all phases found in the .pcr file of current working folder."""
    with open(get_pcr(), "r") as pcr:
        pcr = pcr.read().split("\n")
    phases = []
    trigger, found_phase = (0, 0)
    for num,line in enumerate(pcr):
        if found_phase:
            trigger += 1
            if trigger == 2:
                trigger, found_phase = (0, 0) # deactivate trigger and found_phase flags
                phases.append(line)
        if "!  Data for PHASE number:" in line:
            found_phase = 1
    return phases

@TraceCalls()
def refine_pcr_metadata(frames):
    """returns refined metadata from .pcr using get_metadata_from_pcr()

    Args:
        Frames: List with frame numbers. These are transformed to time depending on metadata in .pcr.
                If timeframe_sec, seconds is assumed. If timeframe_min, minutes assumed.
    Returns:
        Returns title, xaxis labels and transformed_frames.

    Returns title, xaxis, transformed_frames for plotting.
    """
    metadata_kwds = ["sample", "beamtime", "instrument", "experiment"]
    dic = get_metadata_from_pcr()
    title = ""
    for i in metadata_kwds:
        try:
            next = dic[i]
            title += "  "+next
        except:
            print("The key {0} was not in the .pcr metadata.".format(dic[i]))
    HoursOrMinutes = 3 # below three hours we will plot frames in minutes.

    try:
        timeframe = float(dic["timeframe_sec"])
        timeframe_str = str(timeframe).strip("0").strip(".")
        if len(frames) * timeframe / 60. / 60. > HoursOrMinutes:
            transformed_frames = [frame * timeframe / 60. / 60. for frame in frames]
            xaxis = "hours (frame = {0} sec)".format(timeframe_str)
        else:
            transformed_frames = [frame * timeframe / 60. for frame in frames]
            xaxis = "minutes (frame = {0} sec)".format(timeframe_str)
    except:
        try:
            timeframe = float(dic["timeframe_min"])
            if len(frames) * timeframe / 60. > HoursOrMinutes:
                transformed_frames = [frame * timeframe / 60. for frame in frames]
                xaxis = "hours (frame = {0} min)".format(timeframe_str)
            else:
                transformed_frames = [frame * timeframe for frame in frames]
                xaxis = "minutes (frame = {0} min)".format(timeframe_str)
        except:
            xaxis = "frames of unknown length"
            transformed_frames = frames
    return title, xaxis, transformed_frames

# def get_metadata_from_pcr():
#     """Returns a dictionary created from the metadata in .pcr file.
#
#     HOW WORKS:
#         reads the first line of a PCR file, EXAMPLE:
#             experiment=In_Situ_Reduction_DMC sample=NFC_F004_B beamtime=2016Dec timeframe_min=8
#         Each continues string is transformed to a key/value pair for a dictionary. RETURNED:
#             {'beamtime': '2016Dec',
#              'timeframe_min': '8',
#              'experiment': 'In_Situ_Reduction_DMC',
#              'sample': 'NFC_F004_B'}
#     """
#     with open(get_pcr(), "r") as pcr:
#         metadata = pcr.readline().split()
#     dic = dict()
#     for prop in metadata:
#         try:
#             d = prop.split("=")
#             dic[d[0]] = d[1]
#         except:
#             print("!!!!!!!!!!!\nPLEASE INSERT METADATA IN .PCR FILE.\n")
#             print("Examples:")
#             print("\nin first line:")
#             print(r"experiment=In_Situ_Reduction instrument=DMC sample=NFC_F004_A beamtime=2016Dec timeframe_min=8")
#             print("\nand for each phase:")
#             print(r"!-------------------------------------------------------------------------------")
#             print(r"!  Data for PHASE number:   1  ==> Current R_Bragg for Pattern#  1:     9.38")
#             print(r"!-------------------------------------------------------------------------------")
#             print(r"$\gamma$-Fe$_2$O$_3$ Nuclear")
#             print(r"!-------------------------------------------------------------------------------")
#             print(r"!  Data for PHASE number:   2  ==> Current R_Bragg for Pattern#  1:     9.38")
#             print(r"!-------------------------------------------------------------------------------")
#             print(r"$\gamma$-Fe$_2$O$_3$ Magnetic")
#             print(r"!-------------------------------------------------------------------------------")
#             print(r"!  Data for PHASE number:   3  ==> Current R_Bragg for Pattern#  1:     9.38")
#             print(r"!-------------------------------------------------------------------------------")
#             print(r"$\alpha$-Fe Nuclear")
#             print("!!!!!!!!!!!!\n")
#             sys.exit()
#     return dic

@TraceCalls()
def mic_pandas(path, df_init):
    """ extract appearent sizes+errors from .mic to pandas DataFrame and saved.

    """
    import numpy as np
    import pandas as pd
    import re, math
    # from tools import sort_numbered_strings
    # from tools import refine_pcr_metadata
    import os, sys

    """path related work"""
    old_path = os.getcwd()
    os.chdir(path)

    """finding phases"""
    name = '_'
    phase_names = get_phase_names()
    number_of_phases = len(phase_names)
    phases = ["_" + str(num) +"\.mic" for num in range(1,number_of_phases+1)]

    """finding .mic files"""
    exten = '.mic'
    all_files = os.listdir()
    filelist = [f for f in all_files if exten in f and not re.match(name,f)]
    filelist.sort(key = natural_keys)
    """extracting sizes, size_errors and frame numbers"""
    phase_list=[]
    for phase in phases:
        phase_list.append([f for f in filelist if re.search(phase,f)])
    for num,file in enumerate(phases):
        phase_list[num] = sorted(phase_list[num], key = natural_keys)
    sizes = []
    errors = []
    frames = []
    for phase in phase_list:
        size = []
        error = []
        for file in phase:
            with open(file, "r") as f:
                try:
                    index_match = float(re.search(".*(\d+)_\d{1,2}"+exten,file).group(1))
                except Exception as ex:
                    print("\n",ex,"\n")
                    import pdb; pdb.set_trace()
                    print("uuuuups, debugging time")
                for line in f:
                    match = re.search("\s+Average apparent size.*:\s+([\d.]+)\s*\(\s*([-\d.]+)\s*\)",line)
                    failure1 = "(no size broadening)"
                    failure2 = "NaN (      NaN)"
                    for failure in [failure1, failure2]:
                        if failure in line:
                            print("{}: {}".format(file, line))
                            if not index_match in frames:
                                frames.append(index_match)
                            size.append(float("0.0"))
                            error.append(float("0.0"))
                            break
                    if match:
                        if not index_match in frames:
                            frames.append(index_match)
                        extracted_size = float(match.group(1))
                        size.append(extracted_size)
                        error.append(float(match.group(2)))
                        break
                    else:
                        continue
        sizes.append(size)
        #title, xaxis, transformed_frames = refine_pcr_metadata(frames)
        errors.append(error)

    """defining pandas DataFrame"""
    df_mic = df_init.copy(deep=True)#prepare_dataframe(path)

    """preparing columns (frames from data acquisition)"""
    num_frames = len(sizes[0])
    frames = ["".join(["frame ", str(num)]) for num in range(1, num_frames + 1)]

    """preparing extracted values for sizes and their errors"""
    size_of_np = len(sizes)*len(sizes[0]) * 2 # times 2 for errors.
    tmp_np = np.zeros(size_of_np)
    for i in range(number_of_phases):
        tmp_np[i*num_frames*2:(i+1)*num_frames*2] = np.array(sizes[i] + errors[i])
    tmp_np = tmp_np.reshape((number_of_phases*2,num_frames))

    """preparing metadata"""
    path_list = path.split("\\")
    sample = path_list[-2]
    refinement = path_list[-1]

    """applying sizes and errors to pandas DataFrame"""
    for num, np_serie in enumerate(tmp_np):
        maxindex = df_mic.index.max()
        index = 0 if math.isnan( maxindex ) else maxindex + 1
        phase_name = phase_names.pop(0) if num % 2 == 0 else phase_name
        parameter = "size" if num % 2 == 0 else "size_error"
        ready_append = to_append(sys = sample, pcr = refinement, phase = phase_name, var = parameter, vals = np_serie)
        df_mic.loc[index] = ready_append

    """writing DataFrame to .csv"""
    df_mic.to_csv("mic_pandas.csv", index = False) # otherwise index is applied in .csv
    """restoring working directory"""
    os.chdir(old_path)

    return df_mic # success




@TraceCalls()
def seq_pandas(path, df_init):
    """ exract information from .seq to pandas DataFrame and saved.

    works 2017-09-18"""
    import pandas as pd
    import math
    # from tools import get_files_from_subfolders
    import re, os, sys
    # from tools import get_phase_names
    flatten = lambda l: [item for sublist in l for item in sublist]

    """path related"""
    old_path=os.getcwd()
    os.chdir(path)

    """finding .seq file"""
    seq_file = [i for i in os.listdir() if i.endswith(".seq")]
    seq_file = seq_file[0] if len(seq_file) == 1 else "ERRORR!"
    if seq_file == "ERRORR!":
        print(seq_file)
        import pdb; pdb.set_trace()

    """extracting information from seq file"""
    flags = {'NUMPAR': 0, 'NPHASE': 0, 'N_PATT': 0}
    global_chi_2 = []
    r_bragg = []
    unit_cell_volume = []
    weight_fraction = []
    frames = []
    var_names = {}
    var_values = []
    with open(seq_file,"r") as reading:
            for line in reading:
                words = line.split()
                if words[0] == "NEW_REFINEMENT":
                    index = re.search("\d+$",words[1]).group(0) # matches end of string.
                    frames.append(int(index))
                    continue
                if 0 in flags.values():
                    flag_key, flag_value = words[0:2]
                    if flag_key in flags.keys():
                        flags[flag_key] = int(flag_value)
                    if flags['N_PATT'] > 1:
                        print("Number of patterns is not equal to 1.\n\
                            Number of variables in .seq file may vary.\n\
                            This script EXITS!\n\
                            (fix any problems in code regarding to additional patterns ...\n\
                            before removing the sys.exit() safeguard.")
                        sys.exit()
                    if flags['NUMPAR'] > 0 and len(var_values) == 0:
                        for i in range(flags['NUMPAR']):
                            var_values.append([]) # Empty lists are appended according to the value of NUMPAR
                    continue
                if words[0] == "GLOBAL_CHI_2":
                    global_chi_2.append(float(words[1]))
                    continue
                floats = [float(i) for i in words[2:4]]
                if words[1] == "R_Bragg(%):":
                    r_bragg.append(floats)
                    continue
                if words[1] == "Unit_Cell_Volume:":
                    unit_cell_volume.append(floats)
                    continue
                if words[1] == "Weight_Fraction:":
                    weight_fraction.append(floats)
                    continue
                if not words[1].isdigit():
                    index = int(words[0])-1 # to take care of python 0.list start
                    if not words[1] in var_names:
                        var_names[words[1]] = index
                    var_values[index].append(floats)

    """ prepare pandas DataFrame"""
    df_seq = df_init.copy(deep=True)#prepare_dataframe(path)

    """preparing metadata"""
    special_var_names = ["r_bragg", "unit_cell_volume", "weight_fraction"]
    phase_names = get_phase_names()
    number_of_phases = len(phase_names)
    path_list = path.split("\\")
    sample = path_list[-2]
    refinement = path_list[-1]
    list_of_lists = [r_bragg, unit_cell_volume, weight_fraction]
    """applying r_braggs, unit_cell_volumnes, weight_fractions to pd.DataFrame"""
    for num, var in enumerate(special_var_names):
        current_list = list_of_lists[num]
        for i, phase in enumerate(phase_names):
            """ extracting special_var values """
            values = flatten(current_list[i::number_of_phases])[::2]
            """ refinement was done from last to first, therefore values is reversed"""
            values = values[::-1] if frames[-1] < frames[0] else values

            """ appending for value """
            ready_append = to_append(sys = sample, pcr = refinement, phase = phase, var = var, vals = values)
            index = 0 if math.isnan( df_seq.index.max() ) else df_seq.index.max() + 1
            try:
                df_seq.loc[index] = ready_append
            except Exception as ex:
                print("\n",ex,"\n")
                print("uuups... something is wrong... debugging time!")
                print("len(ready_append) =", len(ready_append), "df_seq.shape =", df_seq.shape)
                import pdb; pdb.set_trace()

            """ appending for errors"""
            errors = flatten(current_list[i::number_of_phases])[1::2]
            var_error = "".join([var, "_error"])
            ready_append = to_append(sys = sample, pcr = refinement, phase = phase, var = var_error, vals = errors)
            index_error = index+i+1 # use value index + current phase, we add 1 for python list system.
            df_seq.loc[index_error] = ready_append

    """applying global_chi_2 to pd.DataFrame"""
    index = 0 if math.isnan( df_seq.index.max() ) else df_seq.index.max() + 1
    var = "global_chi_2"
    """ refinement was done from last to first, therefore global_chi_2 is reversed"""
    global_chi_2 = global_chi_2[::-1] if frames[-1] < frames[0] else global_chi_2
    ready_append = to_append(sys = sample, pcr = refinement, phase = var, var = var, vals = global_chi_2)
    df_seq.loc[index] = ready_append

    """applying all other refined parameters to pd.DataFrame"""
    for var_name, var_index in var_names.items():
        match = re.search("_ph(\d{1,2})", var_name)
        if match:
            phase_index = int(match.group(1))
            phase = phase_names[phase_index-1] # -1 for python 0.listindex
        values_and_errors = flatten(var_values[var_index])
        values = values_and_errors[::2]
        """ refinement was done from last to first, therefore values list is reversed"""
        values = values[::-1] if frames[-1] < frames[0] else values
        ready_append = to_append(sys = sample, pcr = refinement, phase = phase, var = var_name, vals = values)
        index = 0 if math.isnan( df_seq.index.max() ) else df_seq.index.max() + 1
        df_seq.loc[index] = ready_append
        errors = values_and_errors[1::2]
        """ refinement was done from last to first, therefore errors is reversed"""
        errors = errors[::-1] if frames[-1] < frames[0] else errors
        var_error = "".join([var_name, "_error"])
        ready_append = to_append(sys = sample, pcr = refinement, phase = phase, var = var_error, vals = errors)
        df_seq.loc[index+i] = ready_append
        # print(to_append)
        # import pdb; pdb.set_trace()

    """write DataFrame to .csv"""
    df_seq.to_csv("seq_pandas.csv", index = False) # otherwise index is applied in .csv

    """restore working directory"""
    os.chdir(old_path)

    return df_seq # success




# end of file.
