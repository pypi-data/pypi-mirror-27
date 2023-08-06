#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import zipfile
import os
import sys
import re
import android_utils
from pack_config import AutoPackConfig

FILE_APK_BACK = '_back.apk'
APK_SUFFIX = '.apk'


def produceApks(autoPackConfig, appName):
    if autoPackConfig:
        originApkFileName = findOriginalApk()
        if not originApkFileName:
            print("找不到母包")
            return
        apkInfo = android_utils.getApkInfo(originApkFileName)
        if not autoPackConfig.dirName:
            print("需要设置输出目录")
        for flavorIndex in range(len(autoPackConfig.flavors)):
            flavor = autoPackConfig.flavors[flavorIndex]
            print(originApkFileName)
            print(flavor)
            os.system("cp %s %s" % (originApkFileName, FILE_APK_BACK))
            zipped = zipfile.ZipFile(FILE_APK_BACK, 'a', zipfile.ZIP_DEFLATED)
            empty_channel_file = "META-INF/topitchannel_{channel}".format(
                channel=flavor)
            zipped.write('empty_file', empty_channel_file)
            zipped.close()
            destDir = appName + "/" + apkInfo.versionCode + "/" + autoPackConfig.dirName
            if not os.path.exists(destDir):
                os.makedirs(destDir)
            destFileName = flavor
            if len(autoPackConfig.suffix) > 0:
                destFileName += "_" + autoPackConfig.suffix
            else:
                if autoPackConfig.useVersionSuffix:
                    destFileName += apkInfo.versionName
            os.system("mv %s %s" %
                      (FILE_APK_BACK, destDir + '/' + destFileName + APK_SUFFIX))


def findOriginalApk():
    files = os.listdir('.')
    for i in files:
        i = i.strip()
        if i.endswith(".apk"):
            return i
