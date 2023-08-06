# encoding: utf-8
import re
import sys

import subprocess
import shlex
import os


def combine(base, fname):
    return base + "/" + fname


def filesize(filePath):
    return os.stat(filePath).st_size


def png2webp(folder, keepPng):
    try:
        arr = os.listdir(folder)
        fullPathList = map(lambda f: (folder + '/' + f), arr)
        for f in fullPathList:
            fname = str(f)
            if fname.endswith(".png"):
                idx = fname.index(".png")
                if idx > 0:
                    name = fname[0:idx]
                    webPName = name + '.webp'
                    comd = 'cwebp -q 80 -o ' + webPName + ' ' + fname
                    subprocess.call(comd, shell=True)
                    pngSize = filesize(fname)
                    webpSize = filesize(webPName)
                    if keepPng == True and pngSize < webpSize:
                        subprocess.call('rm -f ' + webPName, shell=True)
                        print("keep png " + str(pngSize) + " " + str(webpSize))
                    else:
                        subprocess.call('rm -f ' + fname, shell=True)
                        print("keep webp")
    except:
        print("folder is not valid: " + folder)


path_list = []
path_list.append("./app/src/main/res/drawable-xhdpi")
path_list.append("./app/src/main/res/drawable-xxhdpi")
path_list.append("./app/src/main/res/drawable-xxxhdpi")

for p in path_list:
    png2webp(p, True)

#
