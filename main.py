import pandas as pd
import dataFrames as dfs
import queries as q
import os

#'/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/swxevd'
#/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/acd-avaya'
#'/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/ascws'

#2023-01-27 14:30:21.220 2023-01-27 15:30:21.0


[ascwsDataFrames,acdDataFrames,swxevdDataFrames] = dfs.initializeDataFrames()
q.queryFunction(ascwsDataFrames,acdDataFrames,swxevdDataFrames)





































