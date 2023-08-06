#!/usr/bin/env python
# -*- coding: utf-8 -*-


class AutoPackConfig(object):
    """docstring for AutoPackConfig"""

    def __init__(self, flavors):
        super(AutoPackConfig, self).__init__()
        self.flavors = flavors
        self.suffix = ''
        self.dirName = 'default'
        self.useVersionSuffix = False

    def setDirName(self, dirName):
        self.dirName = dirName

    def setSuffix(self, suffix):
        self.suffix = suffix

    def enableVersionSuffix(self, enable):
        self.useVersionSuffix = enable

    def setFixedFileName(fileName):
        self.fileName = fileName
