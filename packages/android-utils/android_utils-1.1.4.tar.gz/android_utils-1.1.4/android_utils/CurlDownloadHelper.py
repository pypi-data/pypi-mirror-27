#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil


def download(url, destDir, targetFileName):
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    if targetFileName:
        fileName = targetFileName
        pass
    else:
        fileName = url.split("/", url.count("/"))[url.count("/")]
    filePath = destDir + "/" + fileName
    if os.path.exists(filePath):
        os.remove(filePath)
    os.system("curl -o %s %s" % (filePath, url))
    return filePath
