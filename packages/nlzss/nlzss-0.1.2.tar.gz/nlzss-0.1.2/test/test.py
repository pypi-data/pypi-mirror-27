#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

ddir = os.path.split(os.path.abspath(sys.argv[0]))[0]

sys.path.insert(0, os.path.normpath(os.path.join(ddir, '..')))

import nlzss

IN_FILE = 'smrpgu_cutscene_skip.1510418360.smc'
OUT_FILE = 'test.smc'

# TODO
