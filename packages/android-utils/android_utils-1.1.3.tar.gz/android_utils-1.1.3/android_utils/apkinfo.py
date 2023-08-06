#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re


class ApkInfo:

    def __init__(self, apkpath):
        output = os.popen("aapt d badging %s" % apkpath).read()
        match = re.compile(
            "package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output)
        if not match:
            print("\n无法获取apk信息，请检查aapt环境变量，参考如下:")
            print("1.命令行终端输入：vi .bash_profile")
            print("2.添加环境变量配置，正确的appt环境变量大致如下：\nexport AAPT_HOME=/Users/mengweiping/Library/Android/sdk/build-tools/25.0.2")
            print("export export PATH=$PATH:$AAPT_HOME/\n")
            exit()
        self.packageName = match.group(1)
        self.versionCode = match.group(2)
        self.versionName = match.group(3)
