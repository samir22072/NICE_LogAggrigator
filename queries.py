import pandas as pd
import dataFrames as dfs
import ascwsFunctions as asf
import acdFunctions as acf
import swxevdFunctions as swf
from datetime import datetime
import re

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
            print(threadIds)
            if(threadIds):
                agentStoryCopy = queryThreadId(threadIds, agentStoryCopy)
        if('3' in filterList):
            if(logLevels):
                agentStoryCopy = queryLogLevel(logLevels, agentStoryCopy)
        print(agentStoryCopy)
        return agentStoryCopy
    except Exception as e:
        print(f"An error occurred while querying function: {str(e)}")
        return pd.DataFrame()




def getTotalTime(input_text):
    pattern1 = re.compile(r"PT[0-9]+\.[0-9]{3}S")
    return pattern1.search(input_text)

def getIds(input_text):
    pattern1 = re.compile(r"CustOid=customer[0-9]+, AcdId=[0-9]+, AgentId=[0-9]+, AgentLogon=[0-9]+")
    return pattern1.search(input_text)


def performanceQuery(swxevdDataFrames):
    if(swxevdDataFrames):
        df = pd.concat(swxevdDataFrames)
        df = df.query(f'content.str.contains("STATS: RTA Msg Finished processing")')
        df.reset_index(inplace=True)
        performanceData = []
        for ind in df.index:
            if(getTotalTime(df['content'][ind]) and getIds(df['content'][ind])):
                time = getTotalTime(df['content'][ind])
                [x, y] = time.span()
                result = int(float(df['content'][ind][x+2:y-1])*1000)

                thread = df['Thread'][ind]

                ids = getIds(df['content'][ind])
                [x,y] = ids.span()
                text = df['content'][ind][x:y]
                text = text.split(', ')
                for i in range(len(text)):
                    s = text[i]
                    ind = s.find('=')
                    text[i] = s[ind+1:]
                customerId = text[0]
                acdId = text[1]
                agentId = text[2]
                agentLogonId = text[3]

                performanceData.append([thread,customerId,acdId,agentId,agentLogonId,result])

                pdf = pd.DataFrame(performanceData,columns=['thread','customerId','acdId','agentId','agentLogonId','performance_time'])

        return pdf
    return None






