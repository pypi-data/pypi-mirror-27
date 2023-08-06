#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pack_config import AutoPackConfig
from FlavorApkProducer import produceApks
autoPackConfig = AutoPackConfig(
    ('baidu',
     'tencent',
     'xiaomi',
     'oppo',
     'meizu',
     'ppzhushou',
     'anzhi',
     'appchina',
     'Nduonet',
     'mumayi',
     'sougou',
     'liantongwowstore',
     'eoemarket',
     'wandoujia',
     'lenovo',
     '_360',
     'huawei',
     'laifenqi'))

autoPackConfig.enableVersionSuffix(True)
autoPackConfig.setDirName('应用商店')

produceApks(autoPackConfig, "laifenqiApp")
