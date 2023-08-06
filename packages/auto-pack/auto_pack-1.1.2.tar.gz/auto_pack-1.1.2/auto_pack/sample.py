#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pack_config import AutoPackConfig
import producer
from producer import FlavorApkProducer

apkProducer = FlavorApkProducer()

autoPackConfig = AutoPackConfig(
    ('baidu',
     'tencent'))
autoPackConfig.enableVersionSuffix()
autoPackConfig.setDestDirName('应用商店')
autoPackConfig.setPrefix("laifenqiApp")
apkProducer.produceApks(autoPackConfig)

autoPackConfig = AutoPackConfig(
    ('laifenqi',))
autoPackConfig.enableVersionSuffix()
autoPackConfig.setDestDirName('升级')
apkProducer.produceApks(autoPackConfig)

autoPackConfig = AutoPackConfig(
    ('laifenqi',))
autoPackConfig.setDestDirName('官网')
apkProducer.produceApks(autoPackConfig)

autoPackConfig = AutoPackConfig(
    ('sms', 'yl'))
autoPackConfig.setDestDirName('推广')
autoPackConfig.setPrefix("laifenqiApp")
apkProducer.produceApks(autoPackConfig)

autoPackConfig = AutoPackConfig(
    ('sms', 'yl'))
autoPackConfig.setDestDirName('推广')
autoPackConfig.useSpecificSuffix("1.7.0")
autoPackConfig.setPrefix("laifenqiApp")
apkProducer.produceApks(autoPackConfig)

apkProducer.finish()
