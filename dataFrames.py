import numpy as np
import re
import pandas as pd
import os
import dataFrames as dfs
import ascwsFunctions as asf
import acdFunctions as acf
import swxevdFunctions as swf


def getInfo(input_text):
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?,[0-9]+\s+(TRACE|DEBUG|INFO|NOTICE|WARN|WARNING|ERROR|SEVERE|FATAL)\s+[A-Za-z0-9\-\.]+", re.IGNORECASE)
    return pattern.match(input_text)


def createDataframe(file, typelog):
    f = open(file, 'r')

    val = 0
    data = []
    line = f.readline()
    while (line):
        matchObj = getInfo(line)
        index = matchObj.span()[1]
        meta = line[0:index]
        content = line[index:]

        metaList = meta.split()
        [time, milliseconds] = metaList[1].split(',')
        metaList.remove(metaList[1])

        date = metaList[0]
        metaList.remove(metaList[0])
        metaList.insert(0, date + ' ' + time + "-" + milliseconds);

        metaList.append(content)
        metaList.append(typelog)
        data.append(metaList)

        line = f.readline()
        val += 1
    df = pd.DataFrame(data, columns=['DateTime', 'LogLevel', 'Thread', 'content', 'Type'])
    df['DateTime'] = df['DateTime'].str.rsplit('-', n=1).str[0] + '-' + df['DateTime'].str.rsplit('-', n=1).str[
        -1].str.zfill(3)
    df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S-%f')

    return df

def initializeDataFrames():

    pathswxevd = str(input("Enter the directory path for swxevd(Leave empty if not applicable):"))
    pathacd = str(input("Enter the directory path for acd-avaya node(Leave empty if not applicable):"))
    pathascws = str(input("Enter the directory path for ascws(Leave empty if not applicable):"))

    ascwsList = []
    acdList = []
    swxevdList = []
    if(pathascws):
        ascwsList = os.listdir(pathascws)
    if(pathacd):
        acdList = os.listdir(pathacd)
    if(pathswxevd):
        swxevdList = os.listdir(pathswxevd)

    ascwsDataFrames = []
    acdDataFrames = []
    swxevdDataFrames = []
    if(ascwsList and pathascws):
        for f in ascwsList:
            ascwsDataFrames.append(dfs.createDataframe(f'{pathascws}/{f}','ascws'))

    if(acdList and pathacd):
        for f in acdList:
            acdDataFrames.append(dfs.createDataframe(f'{pathacd}/{f}','acd'))

    if(swxevdList and pathswxevd):
        for f in swxevdList:
            swxevdDataFrames.append(dfs.createDataframe(f'{pathswxevd}/{f}','swxevd'))

    return [ascwsDataFrames,acdDataFrames,swxevdDataFrames]