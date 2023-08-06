#!/usr/bin/env python
"""data_tests.py: Some correctness tests"""
__author__ = "Fabien Cromieres"
__license__ = "undecided"
__version__ = "1.0"
__email__ = "fabien.cromieres@gmail.com"
__status__ = "Development"

import numpy as np
import chainer
from chainer import Link, Chain, ChainList, Variable
import chainer.functions as F
import chainer.links as L

import nmt_chainer.models as models
import nmt_chainer.utils as utils

import nmt_chainer.make_data as make_data
import os.path

test_data_dir = "tests_data"

class TestMakeData:
    def test_data_creation(self):
        args = ["dummyscript.py", os.path.join(test_data_dir, "src.txt"), os.path.join(test_data_dir, "tgt.txt"), "test_data1" ]
        make_data.cmdline(arguments = args)
        