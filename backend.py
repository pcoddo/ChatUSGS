'''
File: backend.py
Project: ChatUSGS
File Created: 18 March 2023 3:36:40 pm
Author: Perry Oddo (perry.oddo@nasa.gov)
-----
Last Modified: 17 April 2023 2:15:19 pm
Modified By: Perry Oddo (perry.oddo@nasa.gov>)
-----
Description: Submits GPT-3.5 request, parses response, and sends output to USGS Graph Image API script
'''

import os
import inspect
import requests
import subprocess
import pandas as pd

# Open lookup table to match request to parameter codes
lookup = pd.read_csv("data/lookup_table.csv")

def submit_prompt(prompt):

    # Set API information
    api_endpoint = "https://api.openai.com/v1/completions"
    api_key = "Insert OPENAI API KEY here"

    request_header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
    }

    # Format instructions for GPT engine
    instructions = """I want you to extract three pieces of information from the following prompt. 
    The first is a tuple containing the latitude and longitude in decimal degrees, 
    the second is the observation parameter, 
    and the third is the number of days requested. 
    Return these three values, separated by commas. 
    The prompt is here: """

    request_data = {
    "model": "text-davinci-003",
    "prompt": instructions + prompt,
    "max_tokens": 30,
    "temperature": 0.15
    }

    # Send request
    response = requests.post(api_endpoint, headers=request_header, json=request_data)

    # Check for errors
    if response.status_code == 200:
        
        # Extract response
        parsed = response.json()["choices"][0]["text"]

        # Clean response
        output = inspect.cleandoc(parsed)
        output = output.split(",")

    else:
        print(f"Request failed with status code: {str(response.status_code)}")

    # Check that output is formatted correctly:
    # e.g. list containing [lat, long, observation, n_days]
    if len(output) != 4:
        chat_response = "Response not formatted correctly. Try submitting a new request."

    else:
        try:
            isinstance(float(output[0]), float)
            isinstance(float(output[1]), float)
            isinstance(output[2], str)
            isinstance(int(output[3]), int)
        
        except ValueError:
            chat_response = "Response not formatted correctly. Try submitting a new request."

        else:
            chat_response = "Let's get your data!"

    # Strip white space and make lowercase
    output = [s.strip() for s in output]
    output = [s.lower() for s in output]

    # Find matching index
    try:
        code_idx = lookup.loc[lookup["Keyword"] == output[2]].index[0]

    except IndexError:
        print("Requested observation not available. Try submitting new request")

    else:
        pass

    # Find parameter code
    param_code = lookup["Code"][code_idx]
    param_code = param_code.strip('\"')

    # Run USGS graph API using subprocess
    subprocess.call(["python", "scripts/usgs-graph-api.py", 
                    "--latitude", output[0], 
                    "--longitude", output[1], 
                    "--parameter", param_code, 
                    "--days", output[3],
                    "--keyword", output[2]])
    
    graph = "graph.png"

    return chat_response, graph