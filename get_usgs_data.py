'''
File: get_usgs_data.py
Project: ChatUSGS
File Created: 03 April 2023 12:30:50 pm
Author: Perry Oddo (perry.oddo@nasa.gov)
-----
Last Modified: 17 April 2023 2:10:47 pm
Modified By: Perry Oddo (perry.oddo@nasa.gov>)
-----
Description: Combines USGS site data into dataframe, assigns parameter codes, and saves to file
'''

import pickle
import pandas as pd

# Read in site location data for different observations
gage_height = pd.read_table("data/observations/gage_height.txt", skiprows=26, index_col=0)
gage_height = gage_height[1:].reset_index()
gage_height["parameter_code"] = "00065"

precipitation = pd.read_table("data/observations/precipitation.txt", skiprows=26, index_col=0)
precipitation = precipitation[1:].reset_index()
precipitation["parameter_code"] = "00045"

wind_speed = pd.read_table("data/observations/wind_speed.txt", skiprows=26, index_col=0)
wind_speed = wind_speed[1:].reset_index()
wind_speed["parameter_code"] = "00035"

streamflow = pd.read_table("data/observations/streamflow.txt", skiprows=26, index_col=0)
streamflow = streamflow[1:].reset_index()
streamflow["parameter_code"] = "00060"

temperature = pd.read_table("data/observations/air_temperature.txt", skiprows=26, index_col=0)
temperature = temperature[1:].reset_index()
temperature["parameter_code"] = "00021"

dissolved_oxygen = pd.read_table("data/observations/dissolved_oxygen.txt", skiprows=26, index_col=0)
dissolved_oxygen = dissolved_oxygen[1:].reset_index()
dissolved_oxygen["parameter_code"] = "00300"

# Combine data frames
usgs_sites = pd.concat([gage_height, precipitation, wind_speed, streamflow, dissolved_oxygen, temperature])

# Clean
usgs_sites.dropna(subset=["dec_lat_va"], inplace=True)
usgs_sites = usgs_sites[1:].reset_index()

# Save to file
with open("data/usgs_sites.pkl", "wb") as _:
    pickle.dump(usgs_sites, _)

usgs_sites.to_csv("data/usgs_sites.csv")


