#!/usr/bin/env python
#
#  Copyright (c) 2016 The Yews Consulting
#
from __future__ import print_function
import os

from AnimalTesting.selenium_extentions_keywords import AnimalTestingKeywords
__version_file_path__ = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()


class AnimalTesting(AnimalTestingKeywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

