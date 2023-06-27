import numpy
import MAFR
import math
from EigenTrainer import SimpleTrainer

class ProbabilityModel:
    def __init__(self,weights,classes,bins=25):
        self.bins = bins
        self.binSize = 1.0/(bins)
        self.probs = {}
        self.prior = {}
        for c in classes:
            ps = []
            samples = numpy.asarray([w[1] for w in weights if w[0] == c])
            number = len(samples)
            samples = numpy.transpose(samples)
            for s in samples:
                h,b = numpy.histogram(s, bins, range = (0,1))
                # b,h = self.ash1d(s,bins)
                 #ps.append(h)          
                ps.append(h/number)
            self.probs[c] = numpy.asarray(ps)
            self.prior[c] = number/len(weights)
        



    def pOf(self, val, cat=None):
        if cat not in self.probs:
            return 0
        rv = 1
        for i, x in enumerate(val):
            b = math.floor(x/self.binSize)
            rv *= self.probs[cat][i][b]
        return rv*self.prior[cat]


#https://github.com/ajdittmann/ash/blob/master/ash/ash.py
    def ash1d(self,vals, nbins=20, nshifts=10, weights=None):
        vmax = numpy.max(vals)
        vmax = 1
        vmin = numpy.min(vals)
        vmin = 0
        L = vmax-vmin
        h = L/(nbins)
        d = h/nshifts

        kgrid = numpy.linspace(vmin, vmax, nbins*nshifts + 1)
        khist, edges = numpy.histogram(vals, bins=kgrid, weights=weights)
        values = numpy.zeros(nbins*nshifts)
        for k in range(nbins*nshifts):
            for i in range(1-nshifts, nshifts):
                if k+i<0: 
                    value = 0
                elif k+i>=nbins*nshifts: 
                    value = 0
                else: 
                    value = khist[k+i]
                values[k] += value*(1 - numpy.abs(i)/nshifts)

        values = values*nshifts/(h*numpy.sum(values))
        return kgrid[:-1]+0.5*d, values





