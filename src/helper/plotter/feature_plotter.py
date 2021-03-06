'''
Created on 09.08.2016

@author: Paul Pasler
'''

import os

from config.config import ConfigProvider
import matplotlib.pyplot as plt
import numpy as np
import logging
from helper.statistic.signal_statistic_plotter import AbstractSignalPlotter
from posdbos.util.file_util import FileUtil


scriptPath = os.path.dirname(os.path.abspath(__file__))
probands = ConfigProvider().getExperimentConfig().get("probands")

SCREEN_SIZE = (24, 12)

class FeaturePlotter(AbstractSignalPlotter):
    '''
    Plots feature vector
    '''
    def __init__(self, data, header, filePath):
        AbstractSignalPlotter.__init__(self, "featureset", "test", data, header, filePath, False, True, False)
        self.data = data
        self.figsize = SCREEN_SIZE
        
    def _configurePlot(self):
        mng = plt.get_current_fig_manager()
        mng.window.wm_geometry("+0+0")
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.1, hspace=0.1)

    def doPlot(self):
        fig, axes = self._initPlot()
        fig.canvas.set_window_title(self.title)

        for i, signal in enumerate(self.signals):
            self._plotSignal(signal, self.data[:,i], axes[i])

        self._configurePlot()

        self.savePlot()
        self.showPlot()
        logging.info("plotting done")

    def _initPlot(self):
        signalCount = self._calcSignalCount()

        fig, axes = plt.subplots(signalCount, figsize=self.figsize, dpi=80, sharex=True, sharey=False)
        return fig, axes

    def _plotSignal(self, header, data, axis):
        axis.yaxis.set_label_position("right")
        axis.set_ylabel(header)

        axis.plot(data)
        mean = np.nanmean(data)
        logging.info(header, mean)
        axis.plot([mean]*len(data))



def plotAll(filename):
    for proband in probands:
        plot(proband, filename)

def plot(proband, filename):
    experiments = ConfigProvider().getExperimentConfig()
    experimentDir = experiments["filePath"]
    #filePath = "%s/test/%s" % (experimentDir, "awake_full.csv")
    filePath = "%s/%s/%s" % (experimentDir, proband, filename)

    dto = FileUtil().getDto(filePath)
    fp = FeaturePlotter(dto.getData(), dto.getHeader(), filePath)
    fp.doPlot()

def plotOld():
    #filePath = scriptPath + "/../../data/awake_full_.csv"
    filePath = scriptPath + "/../../data/classes.csv"
    dto = FileUtil().getDto(filePath)
    fp = FeaturePlotter(dto.getData(), dto.getHeader(), filePath)
    fp.doPlot()

if __name__ == '__main__': # pragma: no cover
    plot("test", "drowsies_proc_new4.csv")
    #plot("test", "awakes_proc_new4.csv")

