#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import zipfile
import os
import sys
import re
import android_utils
from pack_config import AutoPackConfig
from pkg_resources import resource_string
FILE_APK_BACK = '_back.apk'
APK_SUFFIX = '.apk'
EMPTY_FILE = 'empty_file'


def produceApks(autoPackConfig, appName):
    if autoPackConfig:
        originApkFileName = findOriginalApk()
        if not originApkFileName:
            print("找不到母包")
            return
        apkInfo = android_utils.getApkInfo(originApkFileName)
        if not autoPackConfig.dirName:
            print("需要设置输出目录")
            return
        if not os.path.exists(EMPTY_FILE):
            emptyFile = open(EMPTY_FILE, "wb")
            emptyFile.close()
        for flavorIndex in range(len(autoPackConfig.flavors)):
            flavor = autoPackConfig.flavors[flavorIndex]
            os.system("cp %s %s" % (originApkFileName, FILE_APK_BACK))
            zipped = zipfile.ZipFile(FILE_APK_BACK, 'a', zipfile.ZIP_DEFLATED)
            empty_channel_file = "META-INF/topitchannel_{channel}".format(
                channel=flavor)
            zipped.write(EMPTY_FILE, empty_channel_file)
            zipped.close()
            destDir = 'exportApk/' + appName + "_" + \
                apkInfo.versionCode + "/" + autoPackConfig.dirName
            if not os.path.exists(destDir):
                os.makedirs(destDir)
            if len(autoPackConfig.fileName) > 0:
                destFileName = autoPackConfig.fileName
            else:
                destFileName = appName + "_" + flavor
                if len(autoPackConfig.suffix) > 0:
                    destFileName += ("_" + autoPackConfig.suffix)
                else:
                    if autoPackConfig.useVersionSuffix:
                        destFileName += ("_" + apkInfo.versionName)
            os.system("mv %s %s" %
                      (FILE_APK_BACK, destDir + '/' + destFileName + APK_SUFFIX))
        os.remove(EMPTY_FILE)


def findOriginalApk():
    files = os.listdir('.')
    for i in files:
        i = i.strip()
        if i.endswith(".apk"):
            return i
