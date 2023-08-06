#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .FlavorApkProducer import produceApks
__version__ = '1.1.0'

def produceApks(autoPackConfig, appName):
	FlavorApkProducer.produceApks(autoPackConfig, appName)