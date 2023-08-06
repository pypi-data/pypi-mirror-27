#!/usr/bin/env python
# -*- coding: utf-8 -*-
from producer import FlavorApkProducer

FILE_FLAVORS_MKT = 'flavors-mkt.txt'
FILE_FLAVORS_SMS = 'flavors-sms.txt'
FILE_FLAVORS_UPG = 'flavors-upg.txt'
DABAICARAPP = 'dabaicarApp'

FlavorApkProducer().fromFile(FILE_FLAVORS_UPG).intoDir('官网')

FlavorApkProducer().fromFile(FILE_FLAVORS_UPG).enableVersionSuffix().intoDir('升级')

FlavorApkProducer().fromFile(FILE_FLAVORS_MKT).withPrefix(
    DABAICARAPP).enableVersionSuffix().intoDir('应用商店')

FlavorApkProducer().fromFile(FILE_FLAVORS_SMS).withPrefix(DABAICARAPP).intoDir('推广')
