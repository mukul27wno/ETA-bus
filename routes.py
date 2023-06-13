from app import app 
from flask import render_template
import tweepy 
from textblob import TextBlob
from openpyxl import load_workbook
from wordcloud import WordCloud
import pandas as pd
import re
import os
import forms
import pandas as pd  # for reading and manipulating data
import folium  # for plotting data on maps
import random  # random sampling 
from geopy.distance import distance  # geo spatial distance computations
import requests  # for making API requests
from google.transit import gtfs_realtime_pb2  # for reading realtime GTFS data
from collections import defaultdict  # python's special distionary data structure
from flask import Flask, render_template, request

import urllib.request
import zipfile
import os





@app.route('/',methods=['GET','POST'])
@app.route('/index.html', methods=['GET','POST'])


def index():
    per_route=5553
    curr_time_str = "19:24:30"
    curr_time = "19:24:30"
    alldic = {}
    near_stop = {}
    
    import urllib.request
    import zipfile
    import os

    

    if request.method == 'POST':
        per_route = int(request.form['per_route'])
        curr_time_str = request.form['date']

        
        import pandas as pd  # A library for reading and manipulating data in Python
        import folium  # A library for creating interactive maps with Python
        import random  # A library for generating random numbers and selecting random samples from data
        from geopy.distance import distance  # A library for computing geospatial distances between two points
        import requests  # A library for making HTTP requests in Python
        from google.transit import gtfs_realtime_pb2  # A library for working with real-time General Transit Feed Specification (GTFS) data
        from collections import defaultdict  # A built-in Python data structure that provides default values for missing keys in a dictionary

        # Importing necessary libraries
        import pandas as pd

        # Set the URL of the zip file to be downloaded
        url = "https://github.com/kshitijsriv/csm-gtfs-workshop/raw/master/GTFS.zip"

        # Set the name of the zip file to be downloaded
        filename = "GTFS.zip"

        # Download the zip file from the URL
        urllib.request.urlretrieve(url, filename)

         # Setting the directory for GTFS files
        gtfs_files_dir = "GTFS/"

        # Extract the contents of the zip file to the current directory
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd() + "/GTFS")

        # Remove the zip file after extraction
        os.remove(filename)

        


       

        # Reading the GTFS files into pandas dataframes

        # routes.txt - contains information about transit routes
        routes = pd.read_csv(gtfs_files_dir + "routes.txt")

        # trips.txt - contains information about trips, i.e., a sequence of stops that occurs at specific times on a given route
        trips = pd.read_csv(gtfs_files_dir + "trips.txt")

        # stops.txt - contains information about transit stops
        stops = pd.read_csv(gtfs_files_dir + "stops.txt")

        # stop_times.txt - contains information about the times that a vehicle arrives at and departs from each stop on a trip.
        stop_times = pd.read_csv(gtfs_files_dir + "stop_times.txt")

        # Printing the first few rows of each dataframe
        print(f"""
        routes:
        {routes.head()}

        trips:
        {trips.head()}

        stops:
        {stops.head()}

        stop_times:
        {stop_times.head()}
        """)

        # Merging dataframes to create a single dataframe with all necessary information

        # Merging routes and trips dataframes on the "route_id" column
        merged_df = pd.merge(routes, trips, on=f"route_id")

        # Merging the stop_times dataframe with the merged routes/trips dataframe on the "trip_id" column
        merged_df = pd.merge(merged_df, stop_times, on=f"trip_id")

        # Merging the stops dataframe with the previously merged dataframe on the "stop_id" column
        merged_df = pd.merge(merged_df, stops, on=f"stop_id")

        merged_df

        all_route_details = merged_df[merged_df['route_id']==per_route]
        print(f"Name of the route - {all_route_details['route_long_name'].unique()}")

        all_trips = all_route_details['trip_id'].reset_index(drop=True).unique()
        all_trips

        # for i in range(len(all_trips)):
        #   single_trip_id = all_trips[i]
        #   arr_time = (all_route_details['arrival_time'].loc[all_route_details['trip_id'] == all_trips[i]]).reset_index(drop=True).unique()

        # arr_time[0]

        # class my_dictionary(dict):
        
        # # __init__ function
        # def __init__(self):
        #     self = dict()
        
        # # Function to add key:value
        # def add(self, key, value):
        #     self[key] = value
        
        
        # Main Function
        # df = my_dictionary()

        # for i in range(len(all_trips)):
        # f_arr_time = merged_df[merged_df['trip_id']==all_trips[i]].sort_values('stop_sequence')['arrival_time'].reset_index(drop=True)[0]
        # l_arr_time = merged_df[merged_df['trip_id']==all_trips[i]].sort_values('stop_sequence')['arrival_time'].reset_index(drop=True)[len(merged_df[merged_df['trip_id']==all_trips[i]].sort_values('stop_sequence'))-1]
        # df.add(all_trips[i], [f_arr_time, l_arr_time])
        # df


        # print(len(all_trips['stop_sequence']))



        merged_df[merged_df['trip_id']==all_trips[3]].sort_values('stop_sequence')



        """# Step 1 -> Identify Buses running on route {per_route}"""

        from datetime import datetime

        # Get all buses on a particular route
        all_buses = merged_df[merged_df['route_id'] == per_route]

        # Sort the buses by arrival time
        all_buses = all_buses.sort_values('stop_sequence')

        # Get unique trip IDs
        all_trips_id = all_buses['trip_id'].unique()

        # Initialize variables for counting buses and repeat buses
        count = 0
        rep_bus = 0

        # Initialize empty lists to store arrival and departure times
        time1 = []
        time2 = []

        # Get the first and last arrival time for each trip
        for i in range(len(all_trips_id)):
            all_busess = all_buses[all_buses['trip_id']==all_trips_id[i]]
            time1.append(all_busess['arrival_time'].reset_index(drop=True)[0])
            time2.append(all_busess['arrival_time'].reset_index(drop=True)[len(all_busess['arrival_time'])-1])

        # Define the bus times
        trip_id = all_trips_id
        arrival_time = time1
        departure_time = time2

        # Convert the times to minutes since midnight
        arrival_minutes = [int(t.split(':')[0]) * 60 + int(t.split(':')[1]) for t in arrival_time]
        departure_minutes = [int(t.split(':')[0]) * 60 + int(t.split(':')[1]) for t in departure_time]

        # Sort the points by arrival time
        points = sorted(zip(trip_id, arrival_minutes, departure_minutes), key=lambda x: x[1])

        # Initialize the bus schedule
        bus_schedule = []

        # Loop through the points and assign them to buses
        for point in points:
            assigned = False
            # Try to assign the point to an existing bus
            for i, bus in enumerate(bus_schedule):
                if bus[-1][2] <= point[1]:
                    # If the bus can make it to the point before its arrival time, assign the point to the bus
                    bus_schedule[i].append(point)
                    assigned = True
                    break
            # If the point could not be assigned to an existing bus, add a new bus
            if not assigned:
                bus_schedule.append([point])

        # Print the number of buses needed
        print(len(bus_schedule))


        print(f'in the route {per_route} have atleast {len(bus_schedule)} buses')
        print(f'in the route {per_route} have atmax {len(all_trips_id)} buses')

        """#Step 2 -> Get stops for the route"""

        # Get unique stop IDs for the route
        all_stops_route = all_buses['stop_id'].unique()

        # Print all stops and total number of stops for the route
        print(f"""
        All stops for the route {per_route} 
        {all_buses['stop_id'].unique()}

        Total Stops on route {per_route} - {len(all_stops_route)}""")

        import folium

        def plot_points_on_map(map_obj, stops_df):
            """
            Plots points on a folium map based on coordinates provided in a pandas dataframe.

            Args:
            - map_obj: a folium map object where points will be plotted
            - stops_df: a pandas dataframe containing stop information (latitude, longitude, stop name)

            Returns:
            None
            """
            
            # Iterate through each row of the stops dataframe.
            for index, row in stops_df.iterrows():
                # Get the latitude and longitude coordinates for the current row.
                coord = (row['stop_lat'], row['stop_lon'])
                # Get the name of the stop for the current row.
                stop_name = row['stop_name']
                # Choose a random color from the colormap for the marker.
                marker_color = 'black'
                # Create a circle marker at the coordinate location with the stop name as a tooltip.
                folium.CircleMarker(location=coord,
                                    radius=3,
                                    fill=True,
                                    tooltip=stop_name,
                                    color=marker_color,
                                    fill_opacity=0.7).add_to(map_obj)
            # Print a message to indicate that the points have been plotted on the map.
            print(f"Plotted {stops_df.shape[0]} points on the map.")

        stops_map = folium.Map(location=[28.628833, 77.206805], zoom_start=10, width=400, height=400)
        plot_points_on_map(stops_map, all_buses)
        map_html = stops_map.get_root().render()

        # Display the map in the Jupyter notebook.
        stops_map

        """# Step 3 -> For each bus on the route

        ## 3.1 -> Identify nearest stop

        for accessing the each bus we use trip_id <br>
        trip_id is unique for the each bus <br>
        <br>
        To find the nearest point to the bus we use the time - current time and the time from which bus leave from previous stop ['departure_time'] and the bus reached to next stop ['arrival_time']
        <br>
        We will check which one is more close to current time and find the stop_id of that stop which is closer to bus
        <br>
        <br>
        first we are checking <br> what is the next stop of the bus using current time and the arrival time of next stop of the bus, <br>from the next stop we use the coordinates to check which stop is closer to the bus
        """

        # Set the current time as a string.
        
        # Prompt the user to enter the current time as a string and store it in the curr_time_str variable.
        
        # for i in range(len(all_trips_id)):
        #   trip_id_de = all_buses[all_buses['trip_id']==all_trips_id[i]].sort_value('stop_sequence')
        #   if curr_time_str > trip_id_de['arrival_time'][0]:
        #     if curr_time_str < trip_id_de['departure_time'][len(trip_id_de['trip_id'])-1]:
        #       print(i)

        # print(trip_id_de['trip_id'].unique())

        # Importing datetime module to work with time values
        from datetime import datetime

        # Creating empty dictionaries to store bus stop information and ETA values
        etadic = {}
        upcstop = {}
        alldic = {}
        

        # Looping through all the trips in the data
        for i in range(len(all_trips_id)):
            # Getting the ID of the current trip
            single_trip_id = all_trips_id[i]

            # Getting all the stops for the current trip
            all_stops_single_bus_route = all_buses[all_buses['trip_id'] == single_trip_id]

            # Checking where the bus currently is and what the previous and next stops are
            for j in range(1, len(all_stops_route)):
                pre_dep_time = all_stops_single_bus_route['departure_time'].reset_index(drop=True)[j-1]
                curr_time = curr_time_str
                nxt_arr_time = all_stops_single_bus_route['arrival_time'].reset_index(drop=True)[j]

                # Checking if the current time is between the previous and next stop times
                if pre_dep_time < curr_time_str and curr_time_str < nxt_arr_time:
                    pre_stop = all_stops_route[j-1]
                    next_stop = all_stops_route[j]

                    from datetime import datetime
                    # Converting the time values to datetime objects to perform calculations
                    pre_dep_time = datetime.strptime(f"{pre_dep_time}", "%H:%M:%S")
                    curr_time = datetime.strptime(f"{curr_time}", "%H:%M:%S")
                    curr_time_r = curr_time
                    nxt_arr_time = datetime.strptime(f"{nxt_arr_time}", "%H:%M:%S")

                    # Calculating the distance from the previous stop to the bus's current location
                    dis_pre_stop = (curr_time - pre_dep_time) * 20 # d = t * s, where s = 20 m/s
                    print(curr_time - pre_dep_time)
                    print(type(curr_time))
                    print(type(curr_time - pre_dep_time))

                    # Calculating the distance from the bus's current location to the next stop
                    nxt_arr_stop = (nxt_arr_time - curr_time) * 20  # d = t * s, where s = 20 m/s
                    # nxt_arr_stop = (nxt_arr_time - curr_time).seconds * ((20*1000)/3600)  # d = t * s, where s = 20 m/s

                    # Checking which stop is closer to the bus's current location and printing its details
                    if dis_pre_stop < nxt_arr_stop:
                        near_stopp = all_stops_route[j-1]
                        print(f"""For the Bus trip_id {single_trip_id} 
                            {all_stops_route[j-1]} stop is closest point 
                            Name of the Stop - {(all_buses['stop_name'].loc[all_buses['stop_id']==all_stops_route[j-1]]).unique()}
                            and coordinates points  
                            stop_lat - {(all_buses['stop_lat'].loc[all_buses['stop_id']==all_stops_route[j-1]]).unique()} 
                            stop_lon - {(all_buses['stop_lon'].loc[all_buses['stop_id']==all_stops_route[j-1]]).unique()}
                            Time - {pre_dep_time}
                            """)
                    else:
                        near_stopp = all_stops_route[j]
                        print(f"""For the Bus trip_id {single_trip_id} 
                            {all_stops_route[j]} stop is closest point 
                            Name of the Stop - {(all_buses['stop_name'].loc[all_buses['stop_id']==all_stops_route[j]]).unique()}
                            and coordinates points  
                            stop_lat - {(all_buses['stop_lat'].loc[all_buses['stop_id']==all_stops_route[j]]).unique()} 
                            stop_lon - {(all_buses['stop_lon'].loc[all_buses['stop_id']==all_stops_route[j]]).unique()}
                            Time - {nxt_arr_time}
                            """)

                    # Adding the stop information to the dictionary using the trip ID
                    a = [all_stops_route[j-1],(all_buses['stop_name'].loc[all_buses['stop_id']==all_stops_route[j-1]]).unique(),(all_buses['stop_lat'].loc[all_buses['stop_id']==all_stops_route[j-1]]).unique(),(all_buses['stop_lon'].loc[all_buses['stop_id']==all_stops_route[j-1]]).unique(),pre_dep_time]
                    alldic.update({single_trip_id:a})
                    
                    # print(f'upcoming stops - {all_stops_route[j:]}')
                    ETA = nxt_arr_stop/20
                    import datetime
                    # ETA = curr_time_r+datetime.timedelta(seconds=ETA)
                    upcstop.update({f"{single_trip_id}": f"{all_stops_route[j:]}"})
                    etadic.update({f"{single_trip_id}": f"{ curr_time+ETA }"})
                    near_stop.update({f"{single_trip_id}":f'{near_stopp}'})
        return f"""
                <center>
                    <h3>Step 1. Identify the buses running on the route {per_route}</h2><br>
                    the buses running on the route {per_route} is <b>atleast {len(bus_schedule)}</b><br><br>
                    <h3>Step 2. Get Stops in the route {per_route}</h3>
                    the total number of stops in the route is {len(all_stops_route)}<br><br>
                    All stops list for the route {per_route} <br>
                    <b>{all_stops_route}</b><br><br>
                    {map_html}
                    <h3>Step 3. For each bus on the route</h3>
                    <h4>1. Identify nearest stop</h4>
                    the nearest stop is <b>{near_stop}</b><br>
                    the starting stop of route is {all_stops_route[0]} - {(all_buses['stop_name'].loc[all_buses['stop_id']==all_stops_route[0]]).unique()}<br>
                    the ending stop of route is {all_stops_route[len(all_stops_route)-1]} - {(all_buses['stop_name'].loc[all_buses['stop_id']==all_stops_route[len(all_stops_route)-1]]).unique()}<br>
                    if the nearest stop is empty that means at this time no bus is in the route<br><br>
                    <h4>2. Upcoming Stops - </h4>
                    {upcstop}<br><br>
                    <h4>3. Expected time to reach</h4>
                    {etadic}
                    <br>
                    </center>
                    """

                
        # print(alldic)
        print(upcstop)
        print(etadic)
        print("Rest all busses are not in the route at current time")

        print(dis_pre_stop)

        # print(type(ETA))

        from datetime import datetime
        abc = datetime.strptime(f"{curr_time}", "%H:%M:%S")

        # print(curr_time++datetime.timedelta(seconds=ETA))

        # import datetime
        # print(curr_time_r+datetime.timedelta(seconds=ETA))

        # print(curr_time_r - pre_dep_time)

        """## 3.2 -> Get upcoming stops

        """



        print(f"""
        Upcoming Stops - 
        {upcstop}
        """)

        # import datetime
        # print(type(curr_time_r.seconds))

        print(f'Estimate time - {etadic}')






    return render_template('index.html')