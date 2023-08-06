# errorbar.py

# other dependencies
import os, sys, numpy as np
import os, matplotlib.pyplot as plt

# homegrown dependencies
modules_lib = os.path.split(os.getcwd())[0]
if not modules_lib in sys.path:
    sys.path.append(modules_lib) # adds the modules folder to available folders for importing modules
from debug import get_linenumber # needed for .AHK macro:


class Errorbar():
    """
    A plot object. A list (not numpy.array) is expected as input.
    It should work with numpy.arrays, but it is not testes.
    """
    def __init__(self,
            frames = None,
            values = None,
            errors = None,
            outname = "NoOutName",
            outfolder = "NoOutFolderProvided",
            label = "label = none",
            title = "title = none",
            xaxis = "xaxis = none",
            xticks = None,
            xtick_labels = None,
            yaxis = "yaxis = none",
            size = 36):
        """
        Initialization of a plot object.
        It contains all data (waste of memory?)
        If several objects are created, each one can be inspected.
        """
        self.SIZE = size # general size
        scale1 = 1. / 1.5
        scale2 = 0.6
        self.FIGURE_SIZE = (self.SIZE, self.SIZE * scale1)
        self.TITLE_SIZE = self.SIZE * scale1
        self.XLABEL_SIZE = self.SIZE * scale2
        self.YLABEL_SIZE = self.SIZE * scale2
        self.TICK_SIZE = self.SIZE * scale2

        self.LEGEND_SIZE = self.SIZE * scale2 # size of legends
        self.TICK_SIZE = self.SIZE * scale2
        self.xaxis = xaxis
        self.xticks = xticks if xticks != None else frames
        self.xtick_labels = xtick_labels if xtick_labels != None else [str(f) for f in frames]
        self.yaxis = yaxis
        if outfolder != None:
            self.outfolder = outfolder
        self.outname = outname
        if label != None:
            self.label = label
        if title != None:
            self.title = title
        self.frames = frames
        self.errors = errors
        self.values = values


    def _set_general_plot(self):
        loc = 0 # matplotlib chooses the best position for the legends. fails for errorsbars.
        plt.legend(loc=loc,prop={'size':self.LEGEND_SIZE})
        plt.xlabel(self.xaxis, size = self.XLABEL_SIZE)
        plt.ylabel(self.yaxis, size = self.YLABEL_SIZE)
        plt.title(self.title, size = self.TITLE_SIZE)
        plt.xticks(self.xticks, self.xtick_labels, rotation = 0)
        ax = plt.gca()
        # X AND Y TICK SIZES
        for tick in ax.xaxis.get_major_ticks():
                    tick.label.set_fontsize(self.TICK_SIZE)

        for tick in ax.yaxis.get_major_ticks():
                    tick.label.set_fontsize(self.TICK_SIZE)
        # REMOVE YAXIS NUMBERS
        # ax.axes.get_yaxis().set_ticks([])
        #ymin, ymax = plt.ylim()
        #plt.ylim(0, 1.05)


    def initialize_fig(self, size = 36):
        """
        Initiliaze a figure object
        """
        self.size = size
        cm2inch = lambda tupl: tuple(i/2.54 for i in tupl) # inch2cm: converts a tuple of cm to inches.
        return plt.figure(figsize=cm2inch(self.FIGURE_SIZE))


    def plot_errorbar(self):
        """
        not updated.
        """
        # print(type(self.errors),self.errors)
        # import pdb; pdb.set_trace()
        if self.errors is not None:
            plt.errorbar(self.frames, self.values, yerr = self.errors, label=self.label)
        else:
            plt.plot(self.frames, self.values, label = self.label)
        self._set_general_plot()


    def save_and_clear(self):
        """
        save: saves the current open figure (matplotlib.pyplot)  to a subfolder "figures_seq".
        The figure has filename of "var_name" + .png.
        """
        folder = os.path.join("python_output",self.outfolder)
        try:
            os.stat(folder)
        except:
            os.makedirs(folder) # do not use makdir, as it does not supported rooted folder creation.
        figname = os.path.join(folder, self.outname + '.png')
        plt.savefig(figname, bbopx_inches='tight')
        # plt.savefig(figname)
        plt.close()
