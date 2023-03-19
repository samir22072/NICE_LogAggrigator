import numpy as np
import re
import pandas as pd


def getAgentIdSWXEVD(input_text):
    """
  This function searches for an AgentId pattern in a given string.

  Args:
  input_text (str): A string to search for the AgentId pattern.

  Returns:
  A match object if the pattern is found, None otherwise.
  """
    pattern1 = re.compile(r"AgentId=[0-9]+")
    return pattern1.search(input_text)


def querySWXEVD(queryAgentId, df):
    """
  This function queries the SWXEVD log for a given AgentId and returns a DataFrame containing the results.

  Args:
  queryAgentId (str): The AgentId to query for. If None, returns all results.
  df (DataFrame): The SWXEVD log DataFrame to query.

  Returns:
  A DataFrame containing the query results.
  """
    data = []
    # Iterate over each row in the DataFrame
    for ind in df.index:
        # Search for AgentId pattern in the row's content field
        if (getAgentIdSWXEVD(df['content'][ind])):
            agentId = getAgentIdSWXEVD(df['content'][ind])
            [x, y] = agentId.span()
            # If the queryAgentId matches the AgentId in the row's content field or queryAgentId is None,
            # append the row's DateTime, LogLevel, Thread, content, and Type fields to the data list
            if (queryAgentId == None or queryAgentId in df['content'][ind][x:y]):
                row = [df['DateTime'][ind], df['LogLevel'][ind], df['Thread'][ind], df['content'][ind], df['Type'][ind]]
                data.append(row)

    # Convert the data list to a DataFrame with columns for DateTime, LogLevel, Thread, content, and Type
    agentSet = pd.DataFrame(data, columns=['DateTime', 'LogLevel', 'Thread', 'content', 'Type'])

    # Set the resultSet to the agentSet
    resultSet = agentSet

    return resultSet
