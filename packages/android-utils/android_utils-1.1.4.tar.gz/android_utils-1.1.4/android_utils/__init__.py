#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.1.4'

from .apkinfo import ApkInfo
from .CurlDownloadHelper import download

def getApkInfo(apkPath):
    return ApkInfo(apkPath)
def download(url, destDir, targetFileName):
	return CurlDownloadHelper.download(url, destDir, targetFileName)