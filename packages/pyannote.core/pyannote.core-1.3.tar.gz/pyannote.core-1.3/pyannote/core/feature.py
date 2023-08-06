#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2014 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


"""
########
Features
########

See :class:`pyannote.core.SlidingWindowFeature` for the complete reference.
"""

from __future__ import unicode_literals

import numpy as np
from .segment import Segment
from .segment import SlidingWindow
from .timeline import Timeline


class SlidingWindowFeature(object):

    """Periodic feature vectors

    Parameters
    ----------
    data : (nSamples, nFeatures) numpy array

    sliding_window : SlidingWindow


    """

    def __init__(self, data, sliding_window):
        super(SlidingWindowFeature, self).__init__()
        self.sliding_window = sliding_window
        self.data = data
        self.__i = -1

    def __len__(self):
        return self.data.shape[0]

    def getNumber(self):
        """Number of feature vectors"""
        return self.data.shape[0]

    def getDimension(self):
        """Dimension of feature vectors"""
        return self.data.shape[1]

    def getExtent(self):
        return self.sliding_window.rangeToSegment(0, self.getNumber())

    def __getitem__(self, i):
        """Get ith feature vector"""
        return self.data[i]

    def __iter__(self):
        self.__i = -1
        return self

    def __next__(self):
        self.__i += 1
        try:
            return self.sliding_window[self.__i], self.data[self.__i]
        except IndexError as e:
            raise StopIteration()

    def next(self):
        return self.__next__()

    def iterfeatures(self, window=False):
        """Feature vector iterator

        Parameters
        ----------
        window : bool, optional
            When True, yield both feature vector and corresponding window.
            Default is to only yield feature vector

        """
        nSamples = self.data.shape[0]
        for i in range(nSamples):
            if window:
                yield self.data[i], self.sliding_window[i]
            else:
                yield self.data[i]

    def crop(self, focus, mode='loose', fixed=None, return_data=True):
        """Extract frames as numpy array

        Parameters
        ----------
        focus : Segment or Timeline
        mode : {'loose', 'strict', 'center', 'fixed'}, optional
            In 'strict' mode, only frames fully included in focus coverage are
            returned. In 'loose' mode, any intersecting frames are returned. In
            'center' mode, first and last frames are chosen to be the positions
            whose centers are the closest to the focus start and end times.
            Defaults to 'loose'.
        fixed : float, optional
            When provided and mode is 'center', override focus duration to make
            sure two `focus` with the same duration always result in the same
            (fixed) number of frames being selected.
        return_data : bool, optional
            Set to True (default) to return a numpy array.
            Set to False to return a SlidingWindowFeature instance.

        Returns
        -------
        data : numpy array
            (nSamples, nFeatures) numpy array

        See also
        --------
        SlidingWindow.crop

        """
        indices = self.sliding_window.crop(focus, mode=mode, fixed=fixed)

        # special case when 'fixed' duration cropping is requested
        # mode='clip' ensure the correct number of samples is returned
        # even in case of out-of-bounds indices
        if mode == 'center' and fixed is not None:
            return np.take(self.data, indices, axis=0, out=None, mode='clip')

        # in all other cases, out-of-bounds indices are removed first
        n = self.getNumber()
        indices = indices[np.where((indices > -1) * (indices < n))]

        if isinstance(self.data, np.ndarray):
            data = np.take(self.data, indices, axis=0, out=None)
        else:
            # in case self.data is a HDF5 dataset
            # this may lead to better performance
            data = self.data[indices, :]

        if return_data:
            return data

        sliding_window = SlidingWindow(
            start=self.sliding_window[indices[0]].start,
            duration=self.sliding_window.duration,
            step=self.sliding_window.step)
        return SlidingWindowFeature(data, sliding_window)


    def _repr_png_(self):
        from .notebook import repr_feature
        return repr_feature(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
