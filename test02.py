#!/usr/bin/env python
# coding: utf-8

import datetime
import getopt
import os
import sys
import shutil
import tarfile

def done():
	pass
	print("done.")

def getOpts():
	argv = sys.argv[1:]
	#argv = ["-s", "./v0.0.1/", "-t", "./target/"]
	opts, args = getopt.getopt(argv, "hs:t:")
	opts2 = {}
	for opt in opts:
		opts2[opt[0]] = opt[1]

	if "-h" in opts2.keys():
		print("usage: ./test02.py [-h | -s <sourcePath> -t <targetPath>]")
		print("e.g. : ./test02.py -s ./v5.1.1/ -t ../exist-distribution-5.1.1/")
		return(None)

	count = 0
	if "-s" in opts2.keys():
		count += 1
	if "-t" in opts2.keys():
		count += 1
	if count!=2:
		print("must set both '-s' and '-t' with parameters, see '-h'")
		return(None)
	return(opts2)

def getReplaceFileNames(opts2):
	replaceFileNames = []
	for (subDir, subSubDir, fileNames) in os.walk(opts2["-s"]):
		replaceFileNames.extend(list(map(lambda n: os.path.join(*n), zip([os.path.join(*(subDir.split(os.path.sep)[2:]))]*len(fileNames), fileNames))))
	return(replaceFileNames)

def checkFilePermissions(replaceFileNames, opts2):
	for file in replaceFileNames:
		dstPathFileName = os.path.join(opts2["-t"], file)
		srcPathFileName = os.path.join(opts2["-s"], file)
		tmpPathFileName = "".join([dstPathFileName, "_test02_temp"])
		if (os.access(srcPathFileName, os.F_OK|os.R_OK), os.access(os.path.dirname(tmpPathFileName), os.F_OK|os.W_OK), os.access(dstPathFileName, os.F_OK|os.W_OK)) != (True, True, True):
			raise Exception("permission error")

def createBackup(replaceFileNames, opts2):
	tarFileName = os.path.join(opts2["-t"], "test02_%s.tar" % (datetime.datetime.utcnow().replace(microsecond=0).isoformat().replace(":", "")))
	if os.path.isfile(tarFileName):
		raise Exception("backup tar already exists")
	with tarfile.open(tarFileName, mode='w') as tf:
		_ = list(map(lambda x: tf.add(os.path.join(opts2["-t"], x), arcname=x), replaceFileNames))
	print("created backup in target folder: %s" % (tarFileName))

def createTmpFiles(replaceFileNames, opts2):
	for file in replaceFileNames:
		dstPathFileName = os.path.join(opts2["-t"], file)
		srcPathFileName = os.path.join(opts2["-s"], file)
		tmpPathFileName = "".join([dstPathFileName, "_test02_temp"])
		shutil.copyfile(srcPathFileName, tmpPathFileName)

def switchToNewFiles(replaceFileNames, opts2):
	for file in replaceFileNames:
		dstPathFileName = os.path.join(opts2["-t"], file)
		srcPathFileName = os.path.join(opts2["-s"], file)
		tmpPathFileName = "".join([dstPathFileName, "_test02_temp"])
		shutil.move(tmpPathFileName, dstPathFileName)

if __name__=="__main__":
	opts = getOpts()
	if opts == None:
		exit(0)
	replaceFileNames = getReplaceFileNames(opts)
	checkFilePermissions(replaceFileNames, opts)
	createBackup(replaceFileNames, opts)
	createTmpFiles(replaceFileNames, opts)
	switchToNewFiles(replaceFileNames, opts)
	done()
	exit(0)
