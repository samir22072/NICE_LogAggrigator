import numpy as np
import re
import pandas as pd
import os

# importing custom modules
import dataFrames as dfs
import ascwsFunctions as asf
import acdFunctions as acf
import swxevdFunctions as swf

# function to extract information from a log file
def getInfo(input_text):
    pattern = re.compile(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?,[0-9]+\s+(TRACE|DEBUG|INFO|NOTICE|WARN|WARNING|ERROR|SEVERE|FATAL)\s+[A-Za-z0-9]+",
        re.IGNORECASE)
    return pattern.match(input_text)

# function to create a dataframe from a log file
def createDataframe(file, typelog):
    val = 0
    data = []
    try:
        # split the log file into lines

        file = file.split('\n')

        # process each line in the log file
        for line in file:
            # remove extra spaces from each line
            line = re.sub(' +', ' ', line)
            l = line.split(' ')
            date = l[0]
            # only process lines that start with a date
            if(date!=''):
                time = l[1].replace(',','-')
                dateTime = date+" "+time
                logLevel = l[2]
                threadId = l[3]
                content = ' '.join(l[4:])
                data.append([dateTime,logLevel,threadId,content,typelog])

        # create a pandas dataframe from the processed data
        df = pd.DataFrame(data, columns=['DateTime', 'LogLevel', 'Thread', 'content', 'Type'])
        df['DateTime'] = df['DateTime'].str.rsplit('-', n=1).str[0] + '-' + df['DateTime'].str.rsplit('-', n=1).str[-1].str.zfill(3)
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S-%f')
        df = df.astype({'LogLevel':'category','Thread':'category','Type':'category'})
        return df

    # handle any exceptions that occur while creating the dataframe
    except Exception as e:
        print(f"Error occurred while creating dataframe from file {file}: {e}")

# function to initialize dataframes from log files
def initializeDataFrames(ascwsList, acdList, swxevdList):

    ascwsDataFrames = []
    acdDataFrames = []
    swxevdDataFrames = []

    try:
        # create dataframes for ASCWS logs
        if(ascwsList):
            for f in ascwsList:
                ascwsDataFrames.append(dfs.createDataframe(f,'ascws'))

        # create dataframes for ACD logs
        if(acdList):
            for f in acdList:
                acdDataFrames.append(dfs.createDataframe(f,'acd'))

        # create dataframes for SWXEVD logs
        if(swxevdList):
            for f in swxevdList:
                swxevdDataFrames.append(dfs.createDataframe(f,'swxevd'))

    # handle any exceptions that occur while initializing the dataframes
    except Exception as e:
        print(f"Error occurred while initializing dataframes: {e}")

    return [ascwsDataFrames, acdDataFrames, swxevdDataFrames]
