import pandas as pd
import dataFrames as dfs
import ascwsFunctions as asf
import acdFunctions as acf
import swxevdFunctions as swf
from datetime import datetime

def queryDateTime(startDateTime, endDateTime, df):
    try:
        resultSet = []
        if(startDateTime):
            startDateTime = datetime.strptime(startDateTime, '%Y-%m-%d %H:%M:%S.%f')
        if(endDateTime):
            endDateTime = datetime.strptime(endDateTime, '%Y-%m-%d %H:%M:%S.%f')
        if(startDateTime and endDateTime):
            resultSet = df.query(f"DateTime >= '{startDateTime}' and DateTime <='{endDateTime}'")
        elif(not startDateTime):
            resultSet = df.query(f"DateTime <= '{endDateTime}'")
        elif(not endDateTime):
            resultSet = df.query(f"DateTime >= '{startDateTime}'")
        return resultSet
    except Exception as e:
        print(f"An error occurred while querying DateTime: {str(e)}")
        return pd.DataFrame()

def queryThreadId(threadIds, df):
    try:
        resultSet = []
        if (threadIds):
            resultSet = df.query(f"Thread in {threadIds}")
        return resultSet
    except Exception as e:
        print(f"An error occurred while querying ThreadId: {str(e)}")
        return pd.DataFrame()

def queryLogLevel(logLevels, df):
    try:
        resultSet = []
        if (logLevels):
            resultSet = df.query(f"LogLevel in {logLevels}")
        return resultSet
    except Exception as e:
        print(f"An error occurred while querying LogLevel: {str(e)}")
        return pd.DataFrame()

def queryFunction(ascwsDataFrames, acdDataFrames, swxevdDataFrames, agentId, filterList, startDateTime, endDateTime, threadIds, logLevels):
    try:
        agentStory = pd.DataFrame(columns=['DateTime', 'LogLevel', 'Thread', 'content', 'Type'])
        frames = []
        for df in acdDataFrames:
            frames.append(acf.queryACD(agentId,df))
        for df in ascwsDataFrames:
            frames.append(asf.queryASCWS(agentId,df))
        for df in swxevdDataFrames:
            frames.append(swf.querySWXEVD(agentId,df))
        agentStory = pd.concat(frames)
        agentStoryCopy = agentStory
        if('1' in filterList):
            if(startDateTime and endDateTime):
                agentStoryCopy = queryDateTime(startDateTime, endDateTime, agentStoryCopy)
        if('2' in filterList):
            if(threadIds):
                agentStoryCopy = queryThreadId(threadIds, agentStoryCopy)
        if('3' in filterList):
            if(logLevels):
                agentStoryCopy = queryLogLevel(logLevels, agentStoryCopy)
        return agentStoryCopy
    except Exception as e:
        print(f"An error occurred while querying function: {str(e)}")
        return pd.DataFrame()
