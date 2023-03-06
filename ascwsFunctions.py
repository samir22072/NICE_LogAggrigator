import numpy as np
import re
import pandas as pd


def getLoggingStartASCWS(input_text):
    pattern1 = re.compile(r"logonId = \'[0-9]+\'", re.IGNORECASE)
    pattern2 = re.compile(r"(START)")
    return pattern2.search(input_text) and pattern1.search(input_text)

def getLoggingEndASCWS(input_text):
    pattern1 = re.compile(r"logonId = \'[0-9]+\'", re.IGNORECASE)
    pattern2 = re.compile(r"(END)")
    return pattern2.search(input_text) and pattern1.search(input_text)





def queryASCWS(queryAgentId,df):
  data = []
  flag = False
  for ind in df.index:
    if(getLoggingStartASCWS(df['content'][ind])):
      logonId = getLoggingStartASCWS(df['content'][ind])
      [start,end] = logonId.span()
      if(queryAgentId == None or queryAgentId in df['content'][ind][start:end]):
        flag = True

    elif(getLoggingEndASCWS(df['content'][ind]) and flag == True):
      row = [df['DateTime'][ind],df['LogLevel'][ind],df['Thread'][ind],df['content'][ind],df['Type'][ind]]
      data.append(row)
      flag = False

    if(flag == True):
      row = [df['DateTime'][ind],df['LogLevel'][ind],df['Thread'][ind],df['content'][ind],df['Type'][ind]]
      data.append(row)

  agentSet = pd.DataFrame(data, columns=['DateTime', 'LogLevel', 'Thread', 'content','Type'])

  resultSet = agentSet
  return resultSet
