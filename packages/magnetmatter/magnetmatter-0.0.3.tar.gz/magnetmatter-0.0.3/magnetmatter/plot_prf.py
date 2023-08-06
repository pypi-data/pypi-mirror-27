#prf_develop.py

from datetime import datetime
import os, numpy as np, pandas as pd, sys, re, math
import matplotlib.pyplot as plt

"""adding path to look for private modules"""
modules_lib = os.path.join(os.path.dirname(__file__), "modules")
if not modules_lib in sys.path:
    sys.path.append(modules_lib)
"""importing private modules"""
from wrappers import TraceCalls
from find_tools import findfile, findfiles
from prf_plot_tools import extract_out_file, calculate_size, excluded_regions
from prf_plot_tools import prepare_refinement_result, extract_pcr_file

@TraceCalls()
def main(path = ""):
    drag = 0 # figure is saved on keypress = x.
    width8cm = 1 # graphs are 8 cm wide, perfect for two in word
    width15cm = 0 # graphs are 17 cm wide, perfect for two in .ppt
    width17cm = 0 # graphs are 17 cm wide, perfect for one in word
    width32cm = 0 # single grpah in .ppt
    show = 0 # displays the data, but not interactive. still saves .png
    # method = "r1d1"
    # method = "dmc"
    """ if all zero, figure is saved """


    """ path bookkeeping """
    if path == "":
        p1=r"C:\AU-PHD\General_Data\Report DMC\3_DMC_nov2017\pre_refined"
        p2 =r"C:\AU-PHD\General_Data\Report DMC\3_DMC_nov2017\post_refined"
        p3 = r"C:\AU-PHD\General_Data\Report R1D1\DMC_sept2017\powder4DMC_september2017"
        p4 = r"C:\AU-PHD\General_Data\Report DMC\3_DMC_nov2017\pre_refined"
        p5 = r"C:\AU-PHD\General_Data\Report DMC\3_DMC_nov2017\post_refined"
        p6 = r"C:\AU-PHD\General_Data\Report R1D1\furnaces\Ofurnace"
        p7=r"C:\AU-PHD\General_Data\Report DMC\3_DMC_nov2017\pre_refined"
        p8=r"C:\AU-PHD\General_Data\Report R1D1\mixed_8_and_17nm_maghemite"
        path = p8
    os.chdir(path)
    folders = [folder for folder in os.listdir() if os.path.isdir(folder) ]
    # folders= [r"C:\AU-PHD\General Data\Report DMC\3_DMC_nov2017\post_refined\Ofur_NFC9_4bar"]
    for folder in folders:
        print("found folder {}".format(folder))
    print("")
    # folders = [r"C:\AU-PHD\General Data\Report R1D1\flow synthesis\gamma\gamma22_second_time - Copy"]
    # path = r"C:\AU-PHD\General Data\_Python\DMC_tools\PSI_dec2016\NFC_F4A"
    # folders = [r"C:\AU-PHD\General Data\_Python\DMC_tools\PSI_dec2016\NFC_F4A\24_to_1"]
    # p1 = r"C:\AU-PHD\General Data\_Python\DMC_tools\PSI_sep2017\DMC_Sept2017\refined_pre\Ofur_NFC7A_pre - w impurity - Copy"
    # path = r"C:\AU-PHD\General Data\_Python\DMC_tools\PSI_sep2017\DMC_Sept2017\refined_pre"
    # folders = [r"C:\AU-PHD\General Data\Report DMC\PSI_sep2017\refined_pre\NFC_Fsize8nm_pre", r"C:\AU-PHD\General Data\Report DMC\PSI_sep2017\refined_pre\NFC_Fsize17nm_pre"]

    transparacy_ref_info = 1
    specified_size = True
    if width8cm:
        ### USER INPUT FOR ADJUSTING GRAPH PROPERTIES ###
        graph_width = 8 # cm
        graph_height = 6 # cm
        bigger_text = 10 # do not use
        medium_text = 8 # still quite big
        smaller_text = 6 # better
        micro_text = 4 # 4 good for refinement info.
        subplot_right_space = 7
        dotsize = 1 #
        linewidth = 1
        text_xpos = 1.05
        text_ypos = -0.07
        ### END ###
    elif width15cm:
        graph_width = 15 # cm
        graph_height = graph_width*3/4 # cm
        bigger_text = 14 # do not use
        medium_text = 12 # still quite big
        smaller_text = 10 # better
        micro_text = 8 # 4 good for refinement info.
        dotsize = 2
        linewidth = 2
        subplot_right_space = 8
        text_xpos = 1.1
        text_ypos = -0.1
    elif width17cm:
        graph_width = 17 # cm
        graph_height = graph_width*3/4 # cm
        bigger_text = 14 # do not use
        medium_text = 12 # still quite big
        smaller_text = 10 # better
        micro_text = 8 # 4 good for refinement info.
        dotsize = 2
        linewidth = 2
        subplot_right_space = 7
        text_xpos = 1.1
        text_ypos = 0.1
    elif width32cm:
        graph_width = 32 # cm
        graph_height = graph_width*2/5 # cm
        bigger_text = 20 # do not use
        medium_text = 18 # still quite big
        smaller_text = 16 # better
        micro_text = 10 # 4 good for refinement info.
        dotsize = 3
        linewidth = 2
        subplot_right_space = 5.5
        text_xpos = 1.1
        text_ypos = -0.05

    else:
        graph_width = 17 # cm
        graph_height = graph_width*3/4 # cm
        bigger_text = 14 # do not use
        medium_text = 12 # still quite big
        smaller_text = 10 # better
        micro_text = 8 # 4 good for refinement info.
        dotsize = 2
        linewidth = 2
        subplot_right_space = 7
        text_xpos = 1.1
        text_ypos = 0.1
        specified_size = False
        transparacy_ref_info = 0.75





    fractional_position = [text_xpos, text_ypos]
    separation = ""
    for folder in folders:
        print("working on", folder); os.chdir(path); os.chdir(folder)

        """
        extracting observed and calculated intensities from FP neutron .prf
        DOES NOT WORK WITH X-RAY PRF. Only tested for DMC .prf
        """

        prf = findfile(".prf"); pcr = findfile(".pcr"); out = findfile(".out");
        if not os.path.exists(prf): print("!-!-!-! skipping \"" + folder + "\" + --> no .prf was found"); continue
        if not os.path.exists(pcr): print("!-!-!-! skipping \"" + folder + "\" + --> no .pcr was found"); continue
        if not os.path.exists(out): print("!-!-!-! skipping \"" + folder + "\" + --> no .out was found"); continue


        # if method == "dmc":
        try:
            with open(prf, "r") as reading:
                for num,line in enumerate(reading):
                    if num >= 5:
                        numbers = [float(number) for number in line.strip().split() ]
                        if len(yobs) != entries:
                            yobs += numbers
                        elif len(ycalc) != entries:
                            ycalc += numbers
                        else:
                            bragg_reflections += numbers
                    elif num == 2:
                        end,start,step = [float(number) for number in line.strip().split()[0:3]]
                        angles = np.arange(start,end+step,step)
                        entries = len(angles)
                        yobs = list()
                        ycalc = list()
                        bragg_reflections = list()
            """ UNDER DEVELOPMENT: plot indicating lines for bragg reflections """
            # last_value = 0
            # b_r = bragg_reflections
            # for i,value in enumerate(b_r):
            #     if value > 10000:
            #         continue
            #     elif value < last_value:
            #         b_r = b_r[:i]
            #         break
            #     last_value = value
            # br = pd.DataFrame()
            # midway = int(len(b_r)/2)
            # for col_name, col in zip(["ID","2theta"],[ b_r[:midway], b_r[midway:]]):
            #     br[col_name] = col
            """ UNDER DEVELOPMENT: plot indicating lines for bragg reflections """


            """ preparing dataframe """
            df = pd.DataFrame()
            for col_name, col in zip(["2Theta", "Yobs", "Ycal"], [angles, yobs, ycalc]):
                df[col_name] = col
            print("found a DMC .prf")

        # if method == "r1d1":
        except:
            nb_excluded_regions = excluded_regions()
            df = pd.read_csv(prf, skiprows = 3+nb_excluded_regions, delimiter="[\t]+", engine="python")
            df = df[["2Theta","Yobs","Ycal"]]
            for col in df.columns.values:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            df = df.dropna(axis=0)
            print("found a R1D1 .prf")

        if df.empty: sys.stdout.write("!-!-!-! skipping folder \"" + folder + "\". DataFrame is empty (values in prf might be NaNs)\n"); continue

        df["Yobs-Ycal"] = df["Yobs"]-df["Ycal"]

        """ shortening the view of the diffractogram """
        df = df[df["2Theta"] < 92.900]
        df = df[df["2Theta"] > 20.00]


        """ style of pandas plotting """
        plt.style.use("seaborn")

        """
        plot scatter and line plots of observed and calculated
        """
        if specified_size:
            # print(folder)
            # print(graph_width, graph_height)
            # fig, ax2 = plt.subplots(1,3,1)
            fig, ax1 = plt.subplots(figsize = cm2inch(graph_width, graph_height) )
            plt.subplots_adjust(right=subplot_right_space)


            # plt.subplots_adjust(left=0.1, right=9, top=0.9, bottom=0.1)

            # ax2.axis("off")
        else:
            fig, (ax1) = plt.subplots(figsize = cm2inch(graph_width, graph_height))

        """
        extraction of:
            phase names (dict)
            phase fractions (dict)
            wavelength (float)
            refined parameter value and error (dict)
        """
        wavelength, frac_info, phases, refined_par = extract_out_file()

        """
        calculates:
        ab and c-sizes (dict of dicts)
        """
        size_info = calculate_size(
            wavelength = wavelength,
            phases = phases,
            refined_par = refined_par)

        """
        extracting spacegroup from PCR file
        """
        spacegroups = extract_pcr_file()

        """
        preparing information such as refined parameters, phases, phase fractions
        crystallite sizes and so to be printed on canvas.
        """
        combined_text = prepare_refinement_result(
            phases = phases,
            refined_par = refined_par,
            size_info = size_info,
            frac_info = frac_info,
            separation = separation,
            spacegroups = spacegroups)



        """
        adjusting the position of refinement info.
        """
        # xmax = df["2Theta"].max()
        # xmin = df["2Theta"].min()
        # ymax = df[["Yobs","Ycal"]].max().max()
        # ymin = df[["Yobs-Ycal"]].min().min()
        # difymax = df[["Yobs-Ycal"]].max().max()
        # difymin = df[["Yobs-Ycal"]].min().min()
        text_xpos, text_ypos = fractional_position
        # print(difymin)
        # import pdb; pdb.set_trace()


        y = "Yobs"
        ax1 = df.plot(
            "2Theta",
            y,
            kind="scatter",
            s = dotsize,
            ax = ax1,
            fontsize = smaller_text,  # xtick and ytick labels
            label = y, # for legend
            c = "r",
            alpha=0.5)
        df.plot(
            "2Theta",
            "Ycal",
            linewidth=linewidth,
            ax = ax1,
            alpha=0.8)
        df.plot(
            "2Theta",
            "Yobs-Ycal",
            linewidth = linewidth,
            ax=ax1,
            alpha=0.3)

        """ plotting refinement info on canvas"""
        if specified_size:
            ttt = ax1.text(
                text_xpos,
                text_ypos,
                combined_text,
                size=micro_text,
                alpha = transparacy_ref_info,
                fontname = "monospace",
                picker=True,
                transform = ax1.transAxes)
            ttt.set_bbox(dict(facecolor='white', alpha=0.5, edgecolor='white'))
        elif drag:
            ttt = ax1.text(
                text_xpos,
                text_ypos,
                combined_text,
                size=micro_text,
                alpha = transparacy_ref_info,
                fontname = "monospace")


        # """
        # Fixing the shown ymin and ymax to make the annotated text
        # (refined parameters) appears consistently at the same pixel.
        # """
        # plt.ylim([difymin*1.05,ymax*1.05])


        """ changing the position of the legens to make Yobs appear at the top """
        handles,labels = ax1.get_legend_handles_labels()
        handles = [handles[2], handles[0], handles[1]]
        labels = [labels[2], labels[0], labels[1]]

        """ setting legend to top left corner """
        leg = plt.legend(handles,labels, loc="best", prop = {"size": micro_text})


        # plt.label(bbox_to_anchor = [0.0, 0.0])
        # plt.legend(prop = {"size": micro_text})
        """ setting title to folder name """
        title = os.path.basename(folder)
        if drag or width32cm:
            plt.title(title, size = medium_text)
        elif specified_size:
            # fig.suptitle(title, fontsize=medium_text)
            plt.title(title, size = medium_text)

        """ setting ylabel name """
        ylabel = plt.ylabel("Counts", size = smaller_text)
        """ setting xlabel name """
        plt.xlabel(r"2$\theta$", size = smaller_text)

        """ repositioning and rotation the ylabel """
        ax1.yaxis.set_label_coords(0.0,1.05)
        ylabel.set_rotation(0)
        """ Xlabel must be here otherwise plt.tight_layout is not given the
        additional white space for the ref_info text """
        ax1.xaxis.set_label_coords(1.05,0.05)
        """ setting ylim """
        # plt.ylim([-1000,11000])
        figname = folder+".png"
        figname = os.path.join(path,figname)

        """ scientific notation of major ytick values """
        import matplotlib.ticker as mtick
        ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
        """ ensure nothing is left outside the plot """
        plt.tight_layout()
        """ repositioning xlabel and ylabel """
        ylabel.set_rotation(90)
        ax1.yaxis.set_label_coords(-0.27,0.50)
        ax1.xaxis.set_label_coords(0.50,-0.12)
        plt.xlabel(r"scattering angle 2$\theta$", size = smaller_text)
        ylabel = plt.ylabel("signal count", size = smaller_text)
        # ax1.arrow(-0.1, -0.1, 0.0, -0.1, head_width=0.05, head_length=0.1, fc='k', ec='k')
        # ax1.arrow(-0.1, -0.1, -0.1, 0.0, head_width=0.05, head_length=0.1, fc='k', ec='k')

        if drag and not specified_size:
            # dragh = DragHandler(fig, folder =folder, path = path)
            def onclick(event):
                ttt._x = event.xdata
                ttt._y = event.ydata
                # ymin,ymax = plt.ylim()
                # xmin,xmax = plt.xlim()
                # ttt._x = event.xdata/(xmax-xmin)
                # ttt._y = event.ydata/(ymax-ymin)
                # plt.gca().set_title('Event at pixels {},{} \nand data {},{}'
                # .format(event.x, event.y, event.xdata, event.ydata))
                # import pdb; pdb.set_trace()

                plt.draw()
            ttt.separation = separation
            ttt.figname = figname
            ttt.titlesize = medium_text
            def press(event):
                print('press', event.key)
                sys.stdout.flush()
                if event.key == 'w':
                    ttt.separation += " "
                if event.key == "n" and ttt.separation != "":
                    ttt.separation = ttt.separation[:-1]
                if event.key == "x":
                    plt.gca().set_title(os.path.basename(ttt.figname)[:-4], size = ttt.titlesize)
                    fig.canvas.draw()
                    plt.savefig(ttt.figname, dpi=1000)
                    plt.gca().set_title("saving \"" + os.path.basename(ttt.figname) +"\" succesful!")
                combined_text = prepare_refinement_result(
                    phases = phases,
                    refined_par = refined_par,
                    size_info = size_info,
                    frac_info = frac_info,
                    spacegroups = spacegroups,
                    separation = ttt.separation)
                ttt._text = combined_text
                fig.canvas.draw()


            # tell mpl_connect we want to pass a 'button_press_event' into onclick when the event is detected
            plt.gcf().canvas.mpl_connect('button_press_event', onclick)
            fig.canvas.mpl_connect('key_press_event', press)

            plt.show()
            # print("saving plot to", path)
            xdata, ydata = ttt.get_position()
            separation = ttt.separation
            fractional_position = [xdata, ydata]
        elif show and not specified_size:
            plt.show()
        else:
            plt.savefig(figname, dpi=500, format = "png")

        """ avoid stackoverflow """
        plt.close()



def cm2inch(*tupl):
    """ helper function to convert figsize-cm-tuple to inches """
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)


# @TraceCalls()
# def test_length(filename):
#     with open(filename,"r") as file:
#         values = list()
#         for line in file:
#             line = [value for value in line.strip().split()]
#             values += line
#     print(len(values))
#     import pdb; pdb.set_trace()




if __name__ == "__main__":
    # import pdb; pdb.set_trace(); import time; time.sleep(1); print("sys.argv =\n",sys.argv,"\n")
    if len(sys.argv) > 1:
        main(path = sys.argv[1])
    else:
        main()
else:
    if len(sys.argv) > 1:
        main(path = sys.argv[1])
    # else:
    #     main(path=os.getcwd())










# print("\n\nEND_OF_SCRIPT")
# print(sys.version_info)
# print(sys.executable)
