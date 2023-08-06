#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.1.3'

from .producer import FlavorApkProducer

def fromFile(filePath):
	return FlavorApkProducer().fromFile(filePath)