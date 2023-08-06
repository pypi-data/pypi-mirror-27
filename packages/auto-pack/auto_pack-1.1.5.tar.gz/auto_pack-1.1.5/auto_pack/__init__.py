#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.1.5'

from .producer import FlavorApkProducer

def fromFile(filePath):
	return FlavorApkProducer().fromFile(filePath)