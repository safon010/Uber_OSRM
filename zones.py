# %%
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import networkx as nx
import warnings

zones = gpd.read_file('/home/safon010/Uber_OSRM/cincinnati_censustracts.json')
# %%
graph = []
for i in range(len(zones)):
    print(i+1, "/" , str(len(zones)))
    graph.append(ox.graph_from_polygon(zones.geometry[i], network_type='drive', retain_all=False, simplify=False, truncate_by_edge=True))
G = nx.compose_all(graph)

# %%
# stats will be a list of lists with the following structure:
# [[zone_11, zone_12, d_11, ..., d_11000]
#   ...
#  [zone_n1, zone_n2, d_n1,..., d_n1000]]
num_paths = 500
num_zone_combos = 500
stats = []
for i in range(num_zone_combos):
    # choose two random indeces out oof len(zones) zones
    # and append corresponding zones to stats
    # and assign zone1 and zone2 to the corresponding graph
    ind1, ind2 = random.sample(range(len(zones)), 2)
    zone1 = graph[ind1]
    zone2 = graph[ind2]
    stats.append([zones.loc[ind1], zones.loc[ind2]])
    j = 0
    while j < num_paths:
        node1 = random.choice(list(zone1.nodes))
        node2 = random.choice(list(zone2.nodes))
        try:
            shortest_path = nx.shortest_path_length(G, node1, node2, weight='length', method='dijkstra')
            stats[i].append([shortest_path])
            j += 1
            if j % 1 == 0:
                print("zone combo: ", i+1, "/", num_zone_combos, ",    path: ", j, "/", num_paths)
        except nx.exception.NetworkXNoPath:
            continue
# %%
# save stats to cin_stats.csv
import csv
with open('cin_stats.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(stats)
# %%
#practice
# choose two random zones out of graph
zone1 = graph[0]
zone2 = graph[1]

i=0
while i<100:
    node1 = random.choice(list(zone1.nodes))
    node2 = random.choice(list(zone2.nodes))
    try:
        shortest_path = nx.shortest_path_length(G, node1, node2, weight='length', method='dijkstra')
        print(i, shortest_path)
        i+=1
    except nx.exception.NetworkXNoPath:
        continue
# %%
