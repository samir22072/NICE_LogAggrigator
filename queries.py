import pandas as pd
import dataFrames as dfs
import ascwsFunctions as asf
import acdFunctions as acf
import swxevdFunctions as swf


def queryDateTime(startDateTime,endDateTime,df):
  resultSet = []

  if(startDateTime and endDateTime):
    resultSet = df.query(f"DateTime >= '{startDateTime}' and DateTime <='{endDateTime}'")
  elif(not startDateTime):
      resultSet = df.query(f"DateTime <= {endDateTime}")
  elif(not endDateTime):
      resultSet = df.query(f"DateTime >= {startDateTime}")

  return resultSet


def queryThreadId(threadIds,df):
    resultSet = []
    if (threadIds):
        resultSet = df.query(f"Thread in {threadIds}")

    return resultSet

def queryLogLevel(logLevels,df):
    resultSet = []
    if (logLevels):
        resultSet = df.query(f"LogLevel in {logLevels}")

    return resultSet


def queryFunction(ascwsDataFrames,acdDataFrames,swxevdDataFrames):

    agentId = str(input("Enter Agent Id you wish to filter by:"))
    agentStory = pd.DataFrame(columns=['DateTime', 'LogLevel', 'Thread', 'content', 'Type'])

    frames = []

    for df in acdDataFrames:
        frames.append(acf.queryACD(agentId,df))

    for df in ascwsDataFrames:
        frames.append(asf.queryASCWS(agentId,df))

    for df in swxevdDataFrames:
        frames.append((swf.querySWXEVD(agentId,df)))

    agentStory = pd.concat(frames)

    agentStoryCopy = agentStory


    while(True):
        print("1. Filter by DateTime")
        print("2. Filter by threadIds")
        print("3. Filter by Log Levels")

        option = int(input("Enter the option that you wish to filter by:"))

        if(option == 1):
            startDateTime = str(input("Enter starting dateTime:"))
            endDateTime = str(input("Enter ending dateTime:"))
            agentStoryCopy = queryDateTime(startDateTime,endDateTime,agentStoryCopy)

        elif(option == 2):
            threadIds = []
            n = int(input("Enter the number of threads you wish to track.(Enter 0 if not applicable):"))
            if (n > 0):
                print("Enter the threads to track:")
                for i in range(n):
                    threadIds.append(input())

            agentStoryCopy = queryThreadId(threadIds,agentStoryCopy)
        elif(option == 3):
            logLevels = []
            n = int(input("Enter the number of log levels you wish to track.(Enter 0 if not applicable):"))
            if (n > 0):
                print("Enter the log levels to track:")
                for i in range(n):
                    logLevels.append(input())

            agentStoryCopy = queryLogLevel(logLevels,agentStoryCopy)

        flag = int(input("Do you want to filter by any other field?(1 -> yes, 0 -> no):"))

        if(flag == 0):
            print(agentStoryCopy)
            break