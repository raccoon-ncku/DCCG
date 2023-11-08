import csv
import networkx as nx
import pandas as pd
import networkx as nx

my_dict = {}
with open('mta_travel_time.csv') as f_input:
    for row in csv.reader(f_input):
        my_dict[row[0]] = {row[1]: row[2]}


df = pd.read_csv('mta_travel_time.csv', names=['origin', 'dest', 'dist'])
g = nx.from_pandas_edgelist(df,source='origin',target='dest',edge_attr='dist')
try:
    path = nx.dijkstra_path(g,
                        source='7-Court Square',
                        target='A-Fulton Street'
                        )
    print("The Shortest Path From Source To Destination:")
    print(path)
except Exception:
    print("No Path Exists Between Selected Stations")


print("Shortest Time It Will Take To Reach To Destination(in mili-second):")

path1=nx.dijkstra_path_length(g,'7-Court Square',
                        'A-Fulton Street','dist')

print(path1)
#shortest_time.dijkstra(my_dict, '1-157th Street', '1-137th Street City College')