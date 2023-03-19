import numpy as np
import re
import pandas as pd
pd.set_option('display.max_columns', None)

def initAgentFinderACD(input_text):
    pattern = re.compile(r"Definity agent state message")
    return pattern.search(input_text)

def dispatchAgentFinderACD(input_text):
    pattern = re.compile(r"Dispatching AgentStates to ASCWS.")
    return pattern.search(input_text)

def getAgentCodeACD(input_text):
    pattern = re.compile(r"([/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+)")
    return pattern.findall(input_text)

def getAgentIdsACD(input_text):
    agent_ids = []
    for y in input_text:
      agent_ids.append(y[3])
    return agent_ids



def queryACD(queryAgentId, df):
      data = []
      flag = False
      for ind in df.index:
        if(initAgentFinderACD(df['content'][ind]) ):
          agentCodes = getAgentCodeACD(df['content'][ind])
          agentIds = getAgentIdsACD(agentCodes)
          if(queryAgentId == None or queryAgentId in agentIds):
            flag = True

        elif(dispatchAgentFinderACD(df['content'][ind]) and flag == True):
          row = [df['DateTime'][ind],df['LogLevel'][ind],df['Thread'][ind],df['content'][ind],df['Type'][ind]]
          data.append(row)
          flag = False

        if(flag == True):
          row = [df['DateTime'][ind],df['LogLevel'][ind],df['Thread'][ind],df['content'][ind],df['Type'][ind]]
          data.append(row)

      agentSet = pd.DataFrame(data, columns=['DateTime', 'LogLevel', 'Thread', 'content','Type'])

      resultSet = agentSet
      return resultSet
import numpy as np
import re
import pandas as pd

pd.set_option('display.max_columns', None)

def initAgentFinderACD(input_text):
    pattern = re.compile(r"Definity agent state message")
    return pattern.search(input_text)

def dispatchAgentFinderACD(input_text):
    pattern = re.compile(r"Dispatching AgentStates to ASCWS.")
    return pattern.search(input_text)

def getAgentCodeACD(input_text):
    pattern = re.compile(r"([/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+\|[/-]*[0-9]+)")
    return pattern.findall(input_text)

def getAgentIdsACD(input_text):
    agent_ids = []
    for y in input_text:
        agent_ids.append(y[3])
    return agent_ids

def queryACD(queryAgentId, df):
    data = []
    flag = False
    try:
        for ind in df.index:
            if(initAgentFinderACD(df['content'][ind])):
                agentCodes = getAgentCodeACD(df['content'][ind])
                agentIds = getAgentIdsACD(agentCodes)
                if(queryAgentId == None or queryAgentId in agentIds):
                    flag = True

            elif(dispatchAgentFinderACD(df['content'][ind]) and flag == True):
                row = [df['DateTime'][ind],df['LogLevel'][ind],df['Thread'][ind],df['content'][ind],df['Type'][ind]]
                data.append(row)
                flag = False

            if(flag == True):
                row = [df['DateTime'][ind],df['LogLevel'][ind],df['Thread'][ind],df['content'][ind],df['Type'][ind]]
                data.append(row)

        agentSet = pd.DataFrame(data, columns=['DateTime', 'LogLevel', 'Thread', 'content','Type'])
        resultSet = agentSet
    except Exception as e:
        print("An error occurred: ", e)
        resultSet = None

    return resultSet

