# Import required libraries
import dataFrames as dfs
import queries as q
import pandas as pd
import visualization as v
import os
import sys
import io
import base64
from flask import Flask, Response,jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS

# Create Flask app and API
app = Flask(__name__)
api = Api(app)
CORS(app)
# Set maximum content length for file uploads
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Create a resource for log aggregation
class LogAggreagator(Resource):
    def post(self):
        # Parse input arguments
        parser = reqparse.RequestParser()
        parser.add_argument('AgentId', type=str,help='Agent Id is required field',required=True)
        parser.add_argument('filterList', type=list, location='json',help='filterList is required field.',required=True)
        parser.add_argument('startDatetime', type=str)
        parser.add_argument('endDatetime', type=str)
        parser.add_argument('threadIds', type=list, location='json')
        parser.add_argument('logLevels', type=list, location='json')
        parser.add_argument('files', type=dict, location='json',help='files is a required field',required=True)
        args = parser.parse_args()

        # Extract input arguments
        AgentId = args['AgentId']
        filterList = args['filterList']
        startDatetime = args['startDatetime']
        endDatetime = args['endDatetime']
        threadIds = args['threadIds']
        logLevels = args['logLevels']
        files = args['files']


        # Initialize lists for each type of file
        ascwsList = []
        acdList = []
        swxevdList = []

        # Loop through the ascws files and add them to the ascws list
        for i in range(len(files['ascwsfiles'])):
            ascwsList.append(base64.b64decode(files['ascwsfiles'][i]).decode())

        # Loop through the acdavaya files and add them to the acd list
        for i in range(len(files['acdavayafiles'])):
            acdList.append(base64.b64decode(files['acdavayafiles'][i]).decode())

        # Loop through the swxevd files and add them to the swxevd list
        for i in range(len(files['swxevdfiles'])):
            swxevdList.append(base64.b64decode(files['swxevdfiles'][i]).decode())

        # Initialize data frames for each type of file
        [ascwsDataFrames, acdDataFrames, swxevdDataFrames] = dfs.initializeDataFrames(ascwsList, acdList, swxevdList)
        # Query the data frames to get agent story
        print(swxevdDataFrames)
        performanceData = q.performanceQuery(swxevdDataFrames)
        agentStory = q.queryFunction(ascwsDataFrames, acdDataFrames, swxevdDataFrames, AgentId, filterList, startDatetime, endDatetime, threadIds, logLevels)
        agentStory = agentStory.astype({"DateTime":str})
        # Reset index of agent story
        agentStory.reset_index(inplace=True)
        # Convert agent story to JSON format
        json = agentStory.to_json(orient='records')
        # val = v.plot(agentStory,'DateTime','LogLevel')
        performance = performanceData.to_json(orient='records')

        data = {
            'performanceData':performance,
            'agentStory':json
        }
        if(data):
            # Return JSON response
            return jsonify(data)
        else:
            return {'Error':'An error was generated'}

    def get(self):
        return {'Info': 'Get request does not do anything'}



# Add the log aggregator resource to the API
api.add_resource(LogAggreagator, "/logAggregator")



if __name__=="__main__":
    app.run(debug=True,port=8111)















































