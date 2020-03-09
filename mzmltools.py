#!/usr/bin/env python3
# 
# Project: OpenMS compatible MzML file utility
# Developer: Michael A. Freitas
#
# Description: Python script to filter / transform MzML files
# Copyright (c) 2020, Michael A. Freitas, The Ohio State University
#
# # All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 

import argparse 
import logging
from pyopenms import *
import time

NAME = 'mzml_tools' 
MAJOR_VERSION = '0.1'
MINOR_VERSION = '202003003.1'
DEBUG = True

def timing(f):
    """
    Helper function for timing other functions

    Parameters
    ----------
    f : function

    Returns
    -------
    function
        new function wrap with timer and logging 
    """
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        logging.debug('{:s} function took {:.3f} s'.format(f.__name__, (time2-time1)))
        return ret
    
    return wrap

class FilteringConsumer():
    """
    Consumer that forwards all calls the internal consumer (after
    filtering

    Parameters
    ----------
    consumer: consumer
    params: namespace arguments

    Returns
    -------
    None
    """
    def __init__(self, consumer, params):
        self._internal_consumer = consumer
        self.params = params

    def setExperimentalSettings(self, s):
        self._internal_consumer.setExperimentalSettings(s)

    def setExpectedSize(self, a, b):
        self._internal_consumer.setExpectedSize(a, b)

    def consumeChromatogram(self, c):
        if c.getNativeID().find(self.filter_string) != -1:
            self._internal_consumer.consumeChromatogram(c)

    def consumeSpectrum(self, s):
        s.setFloatDataArrays([])
        #print (self.ms1_filter)
        if s.getMSLevel() == 1:
            if self.params.ms1_threshold > 0:
                tm = ThresholdMower()
                param = tm.getDefaults()
                param.setValue("threshold", float(self.params.ms1_threshold))
                tm.setParameters(param)
                tm.filterSpectrum(s)

        elif s.getMSLevel() > 1:
            if self.params.ms2_threshold > 0:
                tm = ThresholdMower()
                param = tm.getDefaults()
                param.setValue("threshold", float(self.params.ms2_threshold))
                tm.setParameters(param)
                tm.filterSpectrum(s)

        self._internal_consumer.consumeSpectrum(s) 

        
@timing
def main():
    """
    Main Function

    Parse arguments and start writing

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    parser = argparse.ArgumentParser(description="mzmltools")

    parser.add_argument(
        "-i","--input",
        action="store",
        type=str,
        metavar="filename",
        required=True
    )

    parser.add_argument(
        "-o","--output",
        action="store",
        type=str,
        metavar="filename",
        required=True
    )

    parser.add_argument(
        "--ms1_threshold",
        action="store",
        type=float,
        metavar="value",
        default=200.0,
    )

    parser.add_argument(
        "--ms2_threshold",
        action="store",
        type=float,
        metavar="value",
        default=50.0,
    )

    logging.basicConfig(level=logging.DEBUG)

    args = parser.parse_args()

    pmsdw_consumer = PlainMSDataWritingConsumer(args.output)
    f_consumer = FilteringConsumer(pmsdw_consumer, args)
    MzMLFile().transform(bytes(args.input, 'utf-8'), f_consumer)

if __name__ == "__main__":

    main()

