'''
File: usgs-graph-api.py
Project: ChatUSGS
File Created: 14 March 2023 5:38:23 pm
Author: Perry Oddo (perry.oddo@nasa.gov)
-----
Last Modified: 17 April 2023 2:09:31 pm
Modified By: Perry Oddo (perry.oddo@nasa.gov>)
-----
Description: Calculates closest USGS sites to a given AOI and submits Graph Image API to retrieve PNG
'''

import argparse
import pickle
import pandas as pd
import urllib.request
from math import radians, cos, sin, asin, sqrt

# Parse arguments
parser = argparse.ArgumentParser(description="Arguments for USGS Graph API")
parser.add_argument("--latitude", help="Latitude of AOI in decimal degrees")
parser.add_argument("--longitude", help="Longitude of AOI in decimal degrees")
parser.add_argument("--parameter", help="Hydrologic parameter to display")
parser.add_argument("--days", help="Past number of days to display in graph")
parser.add_argument("--keyword", help="Observation keyword for file name")

args = parser.parse_args()

# Read in USGS sites
with open("data/usgs_sites.pkl", "rb") as _:
    usgs_sites = pickle.load(_)

# Define functions
def distance(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return(km)

def find_nearest(lat, long):
    """Finds nearest USGS location to provided lat/long point. Returns site number of nearest location.

    Args:
        lat (float): Latitude in decimal degrees
        long (float): Longitude in decimal degrees
    """
    distances = usgs_sites.apply(
        lambda row: distance(lat, long, float(row["dec_lat_va"]), float(row["dec_long_va"])), 
        axis=1)
    
    return(usgs_sites.loc[distances.idxmin(), "site_no"])

def usgs_graph_api(site, parameter, days):
    """Downloads .png image of current hydrological conditions

    Args:
        site (str): USGS Site ID
        parameter (str): USGS paramter string
        days (str): Number of days to display in chart
    """
    # Format API request
    url = "https://labs.waterdata.usgs.gov/api/graph-images/monitoring-location/{0}/?parameterCode={1}&width=1200&title=true&compare=false&period=P{2}D".format(site, parameter, days)

    # Find site name
    site_index = usgs_sites.index[usgs_sites["site_no"] == site].tolist()
    site_name = usgs_sites["station_nm"][site_index].item()

    # Send request
    urllib.request.urlretrieve(url, filename="graph.png")
    

# Filter data frame for stations with desired parameter
usgs_sites = usgs_sites[usgs_sites["parameter_code"] == args.parameter]

# Select target
target = find_nearest(lat=float(args.latitude), long=float(args.longitude))

# This is the beef: once the arguments are parsed, pass them on
usgs_graph_api(site=target, parameter=args.parameter, days=args.days)
