#!/usr/bin/env python
# -*- coding: utf-8 -*-

import android_utils
__version__ = '1.0.2'


def getApkInfo(apkPath):
    apkinfo = android_utils.getApkInfo(apkPath)
    print(apkinfo.versionCode, apkinfo.versionName)
