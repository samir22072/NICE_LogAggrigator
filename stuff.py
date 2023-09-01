import tkinter as tk
import pandas as pd
import dataFrames as dfs
import queries as q
from tkinter import ttk
import numpy
import ascwsFunctions as asf
import acdFunctions as acf
import swxevdFunctions as swf
import os
import sys

# import textwrap
# def wrap(string, length=100):
#     return '\n'.join(textwrap.wrap(string, length))

#'/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/swxevd'
#/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/acd-avaya'
#'/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/ascws'

#2023-01-27 14:30:21.220

#receiver.2 Service6 indexDeleteSchld1

#TRACE DEBUG





def savetoFolder(agentStoryCopy,path):
    file_name = 'Result.xlsx'
    agentStoryCopy.to_excel(f'{path}/{file_name}', index=False)
    labelText = tk.StringVar()
    labelText.set("Excel file returned successfully.")
    labelDir = tk.Label(my_w, textvariable=labelText)
    labelDir.grid(row=15,column=0)

def filterDate(start,end):
    global agentStoryCopy
    agentStoryCopy = q.queryDateTime(startDateTime.get(), endDateTime.get(), agentStoryCopy)

def queryParameters(option,agentId):
    print(option)
    global agentStoryCopy
    if (1 in option):

        # startDateTime = str(input("Enter starting dateTime:"))
        # endDateTime = str(input("Enter ending dateTime:"))
        labelStart.grid(row=10,column=0)
        startDateTime.grid(row=10,column=1)
        labelEnd.grid(row=11,column=0)
        endDateTime.grid(row=11,column=1)
        b3.grid(row=12,column=0)

    if (2 in option):
        threadIds = []
        print(agentStoryCopy.Thread.unique())
        n = int(input("Enter the number of threads you wish to track.(Enter 0 if not applicable):"))
        if (n > 0):
            print("Enter the threads to track:")
            for i in range(n):
                threadIds.append(input())
        agentStoryCopy = q.queryThreadId(threadIds, agentStoryCopy)
    if (3 in option):
        logLevels = []
        n = int(input("Enter the number of log levels you wish to track.(Enter 0 if not applicable):"))
        if (n > 0):
            print("Enter the log levels to track:")
            for i in range(n):
                logLevels.append(input())

        agentStoryCopy = q.queryLogLevel(logLevels, agentStoryCopy)


    agentStoryCopy = agentStoryCopy.astype({'DateTime':str})
    labelText = tk.StringVar()
    labelText.set("Result Directory path:")
    labelDir = tk.Label(my_w, textvariable=labelText)
    labelDir.grid(row=13,column=0)
    fpath.grid(row=13,column=1)

    b4.grid(row=14,column=0)




    # flag = int(input("Do you want to filter by any other field?(1 -> yes, 0 -> no):"))
    #
    # if(flag == 0):

    # l1 = list(agentStoryCopy)  # list of column names

    # rset = agentStoryCopy.to_numpy().tolist()
    #
    # global trv
    #
    # trv['height'] = 3000
    # trv['show'] = 'headings'
    # trv['columns'] = l1
    #
    # s = ttk.Style()
    # s.configure('Treeview', rowheight=150)
    #
    # for i in l1:
    #     if (i != 'content'):
    #         trv.column(i, width=int(my_w.winfo_screenwidth() / 8), anchor='c')
    #         trv.heading(i, text=i)
    #     else:
    #         trv.column(i, width=int(my_w.winfo_screenwidth() / 2), anchor='c')
    #         trv.heading(i, text=i)
    #
    # for dt in rset:
    #     v = [wrap(str(r)) for r in dt]
    #     print(v)
    #     trv.insert("", 'end', values=v)
    #
    # trv.pack()
    # vsb = ttk.Scrollbar(my_w, orient="vertical", command=trv.yview)
    # vsb.pack(side='right',fill='both')
    # trv.config(yscrollcommand=vsb.set)


def sel():
    global var
    print(var1.get(),var2.get(),var3.get())
    if(var1.get() == 1):
        var.append(1)
    if(var1.get() == 0):
        if(1 in var):
            var = [v for v in var if v!=1]
    if (var2.get() == 1):
        var.append(2)
    if (var2.get() == 0):
        if (2 in var):
            var = [v for v in var if v != 2]
    if(var3.get() == 1):
        var.append(3)
    if (var3.get() == 0):
        if (3 in var):
            var = [v for v in var if v != 3]

    var = list(set(var))


def queryFunction(ascwsDataFrames,acdDataFrames,swxevdDataFrames,agentId):

    # agentId = str(input("Enter Agent Id you wish to filter by:"))


    agentStory = pd.DataFrame(columns=['DateTime', 'LogLevel', 'Thread', 'content', 'Type'])

    frames = []

    for df in acdDataFrames:
        frames.append(acf.queryACD(agentId,df))

    for df in ascwsDataFrames:
        frames.append(asf.queryASCWS(agentId,df))

    for df in swxevdDataFrames:
        frames.append(swf.querySWXEVD(agentId,df))

    agentStory = pd.concat(frames)

    global agentStoryCopy
    agentStoryCopy= agentStory

    labelText = tk.StringVar()
    labelText.set("Choose Filtering Criteria:")
    labelDir = tk.Label(my_w, textvariable=labelText)
    labelDir.grid(row=4,column=0)
    global var1,var2,var3
    R1 = tk.Checkbutton(master=my_w, text="Filter by dateTime", variable=var1,onvalue = 1, offvalue = 0,command=sel)
    R1.grid(row=5,column=0)
    R2 = tk.Checkbutton(master=my_w, text="Filter by threadIds", variable=var2, onvalue = 1, offvalue = 0,command=sel)
    R2.grid(row=6,column=0)
    R3 = tk.Checkbutton(master=my_w, text="Filter by Log Levels", variable=var3, onvalue = 1, offvalue = 0,command=sel)
    R3.grid(row=7,column=0)


    # print("1. Filter by DateTime")
    # print("2. Filter by threadIds")
    # print("3. Filter by Log Levels")

    # option = str(input())

    # labelText = tk.StringVar()
    # labelText.set("Filtering Criteria:")
    # labelDir = tk.Label(my_w, textvariable=labelText)
    # labelDir.grid(row=5, column=0)
    #
    # filter = tk.StringVar()
    # filter.set("Filter by DateTime")
    # drop = tk.OptionMenu(my_w, filter, "Filter by DateTime", "Filter by Thread Ids", "Filter by Log Levels")
    # drop.grid(row=5,column=1)
    # option = filter.get()
    # print(option)

    b2.grid(row=8,column=0)






def filter(ascwspath,acdpath,swxevdpath,agentId):
    [ascwsDataFrames,acdDataFrames,swxevdDataFrames] = dfs.initializeDataFrames(ascwspath,acdpath,swxevdpath)
    agentStory = queryFunction(ascwsDataFrames,acdDataFrames,swxevdDataFrames,agentId)




my_w = tk.Tk()
width = my_w.winfo_screenwidth()
height = my_w.winfo_screenheight()
my_w.geometry("%dx%d" % (700, 700))

my_w.title("Result")



var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
agentStoryCopy = []
var = []
# trv = ttk.Treeview(my_w, selectmode='browse')
# l1 = tk.Label(my_w,text="ACD path",width = 5,font = 18)
# l1.grid(row=1,column=1,padx=3,pady=10)
#
# e1 = tk.Entry(my_w,width=35,bg='yellow',font=18)
# e1.grid(row=1,column=2,padx=1)
#
#
# l2 = tk.Label(my_w,text="ASCWS path",width = 5,font = 18)
# l2.grid(row=2,column=1,padx=3,pady=10)
#
# e2 = tk.Entry(my_w,width=35,bg='yellow',font=18)
# e2.grid(row=2,column=2,padx=1)
#
# l3 = tk.Label(my_w,text="SWXEVD path",width = 5,font = 18)
# l3.grid(row=3,column=1,padx=3,pady=10)
#
# e3 = tk.Entry(my_w,width=35,bg='yellow',font=18)
# e3.grid(row=3,column=2,padx=1)

labelText=tk.StringVar()
labelText.set("ASCWS Directory: ")
labelDir=tk.Label(my_w, textvariable=labelText)
labelDir.grid(row=0,column=0)
ascwspath = tk.Entry(my_w,width = 50)
ascwspath.grid(row=0,column=1)


labelText=tk.StringVar()
labelText.set("ACD-AVAYA Directory: ")
labelDir=tk.Label(my_w, textvariable=labelText)
labelDir.grid(row=1,column=0)
acdpath = tk.Entry(my_w,width = 50)
acdpath.grid(row=1,column=1)


labelText=tk.StringVar()
labelText.set("SWXEVD Directory: ")
labelDir=tk.Label(my_w, textvariable=labelText)
labelDir.grid(row=2,column=0)
swxevdpath = tk.Entry(my_w,width = 50)
swxevdpath.grid(row=2,column=1)

labelText = tk.StringVar()
labelText.set("Agent Id: ")
labelDir = tk.Label(my_w, textvariable=labelText)
labelDir.grid(row=3,column=0)
agentId = tk.Entry(my_w,width=50)
agentId.grid(row=3,column=1)

labelText = tk.StringVar()
labelText.set("Starting dateTime: ")
labelStart = tk.Label(my_w, textvariable=labelText)
startDateTime = tk.Entry(my_w,width=50)

labelText = tk.StringVar()
labelText.set("Ending dateTime: ")
labelEnd = tk.Label(my_w, textvariable=labelText)
endDateTime = tk.Entry(my_w,width=50)

fpath = tk.Entry(my_w, width=50)


b1 = tk.Button(my_w,text = 'Search',width=7,font = 18,command=lambda:filter(ascwspath.get(),acdpath.get(),swxevdpath.get(),agentId.get()))
b1.grid(row=4,column=0)

b2 = tk.Button(my_w, text='Filter', width=7, font=18,
                   command=lambda : queryParameters(var,agentId))

b3 = tk.Button(my_w, text='Filter by dateTime', width=15, font=18,
                       command=lambda: filterDate(startDateTime.get(),endDateTime.get()))

b4 = tk.Button(my_w, text='Generate excel file', width=15, font=18,
                   command=lambda: savetoFolder(agentStoryCopy,fpath.get()))

my_w.mainloop()