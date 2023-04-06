# %%
import numpy as np
np.float = float 
import pandas as pd
import csv
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import networkx as nx
import json
from shapely.geometry import Polygon

# %%
# load stats from cin_stats.csv as a list of lists
with open('cin_stats.csv', 'r') as f:
    reader = csv.reader(f)
    stats = list(reader)

# %%
# find areas of each zone
with open('cincinnati_censustracts.json') as f:
    areas = []
    data = json.load(f)
    for i in data['features']:
        # find the area of each zone
        area = Polygon(i['geometry']['coordinates'][0]).area
        movement_id = i['properties']['MOVEMENT_ID']
        # append the area to the list
        areas.append([movement_id, area])

# %%
# load cincinnati_censustracts.json as a GeoDataFrame
zones = gpd.read_file('cincinnati_censustracts.json')
# convert to graph objects
graph = []
for i in range(len(zones)):
    print(i+1, "/" , str(len(zones)))
    # append the graph to the list
    graph.append([zones.MOVEMENT_ID[i], ox.graph_from_polygon(zones.geometry[i], network_type='drive', retain_all=False, simplify=False, truncate_by_edge=True)])
G = nx.compose_all([x[1] for x in graph])

# %%
# replace the strings in the first two columns with the corresponding graphs from cincinnati_censustracts.json
for i in range(len(stats)):
    # find MOVEMENT_ID in first two columns
    for j in range(2):
        id = stats[i][j].split()[1]
        # find the index of the graph with the same MOVEMENT_ID
        for k in range(len(zones)):
            if id == str(zones.MOVEMENT_ID[k]):
                stats[i][j] = graph[k]
                break
            else:
                continue

 
# %%
# combine and replace all the distances into one list, so len(stats[i]) = 3
for i in range(len(stats)):
    stats[i] = stats[i][:2] + [int(float(x[1:-1])) for x in stats[i][2:]]
    stats[i] = [stats[i][0], stats[i][1], stats[i][2:]]

# %%
#average distance between the two zones
for i in range(len(stats)):
    stats[i].append(sum(stats[i][2])/len(stats[i][2]))

# %%
# ratio of the area of the first zone to the area of the second zone from areas list
for i in range(len(stats)):
    # find MOVEMENT_ID in first two columns
    area = []
    for j in range(2):
        # find the MOVEMENT_ID
        id = stats[i][j][0]
        # find the index of the graph with the same MOVEMENT_ID
        for k in range(len(areas)):
            if id == str(areas[k][0]):
                area.append(areas[k][1])
                break
            else:
                continue
    stats[i].append(area[0]/area[1])

# %%
# add a column to stats with a list containing the land type (rural, suburban, urban) of the two zones

# %%
# add a column to stats with the average yearly precipitation of the two zones
for i in range(len(stats)):
    # convert zones to gdfs and extract the precipitation
    zone1 = ox.graph_from_polygon(stats[i][0].geometry, network_type='drive', retain_all=True, simplify=False, truncate_by_edge=True)
    zone1_precip = ox.project_gdf(ox.graph_to_gdfs(zone1, nodes=False, edges=False, fill_edge_geometry=True)[1]).precip[0]
    zone2 = ox.graph_from_polygon(stats[i][1].geometry, network_type='drive', retain_all=True, simplify=False, truncate_by_edge=True)
    zone2_precip = ox.project_gdf(ox.graph_to_gdfs(zone2, nodes=False, edges=False, fill_edge_geometry=True)[1]).precip[0]
    # add a list of the precipitation of the two zones to stats
    stats[i].append([zone1_precip, zone2_precip])

# %%
# add a row on top of stats with the column names
# ['zone1', 'zone2', '[d1', 'd2', ..., 'd1000]', 'avg_dist', 'ratio', 'land_type']
stats = [['zone1', 'zone2', '[d1, ..., d1000]', 'avg_dist', 'ratio', '[land_type_1, land_type_2]']] + stats
