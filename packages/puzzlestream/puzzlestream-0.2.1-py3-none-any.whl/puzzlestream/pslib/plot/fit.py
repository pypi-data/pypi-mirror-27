import numpy as np

from puzzlestream.pslib.plot import Plot


class FitPlot(Plot):

    def __init__(self, fit, figsize=(7, 4), dpi=150):
        super().__init__(nrows=2, figsize=figsize, dpi=dpi)
        self.__fit = fit
        self.replot()

    def replot(self):
        fit = self.__fit
        self.plot(fit.xc, fit.yc, e_x=fit.e_xc, e_y=fit.e_yc)

        x = np.linspace(np.min(fit.xc), np.max(fit.xc), 2500)
        self.plot(x, fit.fitFunctionFitted(x))
