#!/usr/bin/env python
# -*- coding: utf-8 -*-
import android_utils
import subprocess
import os

def reportApkFilesInfo(destFiles):
    result = {}
    for i in range(0, len(destFiles)):
        apkPath = destFiles[i]
        apkInfo = android_utils.getApkInfo(apkPath)
        if len(apkInfo.packageName) <= 0:
            apkInfo.versionCode = "notfound"
        if apkInfo.versionCode in result.keys():
            result[apkInfo.versionCode].append(os.path.basename(apkPath))
        else:
            result[apkInfo.versionCode] = [os.path.basename(apkPath), ]

    logFileName = "checklog.json"
    logFile = open(logFileName, "wb")
    logFile.write((str(result)).encode('utf-8'))
    logFile.close()
    subprocess.call(["open", os.path.realpath(logFileName)])
