import numpy as np
import re
import pandas as pd


def getAgentIdSWXEVD(input_text):
    pattern1 = re.compile(r"AgentId=[0-9]+")
    return pattern1.search(input_text)



def querySWXEVD(queryAgentId, df):
  data = []
  for ind in df.index:
    if(getAgentIdSWXEVD(df['content'][ind])):
      agentId = getAgentIdSWXEVD(df['content'][ind])
      [x,y] = agentId.span()
      if(queryAgentId == None or queryAgentId in df['content'][ind][x:y]):
        row = [df['DateTime'][ind],df['LogLevel'][ind],df['Thread'][ind],df['content'][ind],df['Type'][ind]]
        data.append(row)

  agentSet = pd.DataFrame(data, columns=['DateTime', 'LogLevel', 'Thread', 'content','Type'])

  resultSet = agentSet

  return resultSet
