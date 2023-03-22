import csv
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import networkx as nx

# open cin_stats.csv
# %%
# load stats from cin_stats.csv as a list of lists
with open('cin_stats.csv', 'r') as f:
    reader = csv.reader(f)
    stats = list(reader)
# %%
# combine and replace all the distances into one list
for i in range(len(stats)):
    stats[i] = stats[i][:2] + [float(x) for x in stats[i][2:]]

# add a row on top of stats with the column names
# ['zone1', 'zone2', '[d1', 'd2', ..., 'd1000]', 'avg_dist', 'ratio', 'land_type']
stats = [['zone1', 'zone2', '[d1', ..., 'd1000]', 'avg_dist', 'ratio', '[land_type_1, land_type_2]']] + stats

# %%
# add a column to stats with the average distance between the two zones
for i in range(len(stats)):
    stats[i].append(sum(stats[i][2:])/len(stats[i][2:]))
# %%

# add a column to stats with the ratio of the area of the first zone to the area of the second zone
for i in range(len(stats)):
    # calculate the area of the first zone
    zone1 = ox.graph_from_polygon(stats[i][0].geometry, network_type='drive', retain_all=True, simplify=False, truncate_by_edge=True)
    zone1_area = ox.project_gdf(ox.graph_to_gdfs(zone1, nodes=False, edges=False, fill_edge_geometry=True)[1]).area[0]
    # calculate the area of the second zone
    zone2 = ox.graph_from_polygon(stats[i][1].geometry, network_type='drive', retain_all=True, simplify=False, truncate_by_edge=True)
    zone2_area = ox.project_gdf(ox.graph_to_gdfs(zone2, nodes=False, edges=False, fill_edge_geometry=True)[1]).area[0]
    # calculate the ratio of the first zone to the second zone
    stats[i].append(zone1_area/zone2_area)
# %%

# add a column to stats with a list containing the land type (rural, suburban, urban) of the two zones
for i in range(len(stats)):
    # convert zones to gdfs and extract the land type
    zone1 = ox.graph_from_polygon(stats[i][0].geometry, network_type='drive', retain_all=True, simplify=False, truncate_by_edge=True)
    zone1_land_type = ox.project_gdf(ox.graph_to_gdfs(zone1, nodes=False, edges=False, fill_edge_geometry=True)[1]).landuse[0]
    zone2 = ox.graph_from_polygon(stats[i][1].geometry, network_type='drive', retain_all=True, simplify=False, truncate_by_edge=True)
    zone2_land_type = ox.project_gdf(ox.graph_to_gdfs(zone2, nodes=False, edges=False, fill_edge_geometry=True)[1]).landuse[0]
    # add the land type to stats
    stats[i].append([zone1_land_type, zone2_land_type])
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