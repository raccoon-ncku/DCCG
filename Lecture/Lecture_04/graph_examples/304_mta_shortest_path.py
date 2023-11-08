import os
import networkx as nx
import pandas as pd
import networkx as nx

fp = os.path.join(
    os.path.dirname(__file__),
    'mta_travel_time.csv'
)

df = pd.read_csv(fp, names=['origin', 'dest', 'dist'])
g = nx.from_pandas_edgelist(df,source='origin',target='dest',edge_attr='dist')

path = nx.dijkstra_path(g,
                    source='7-Court Square',
                    target='A-Fulton Street'
                    )
print("The Shortest Path From Source To Destination:")
print(path)

print("Shortest Time It Will Take To Reach To Destination(in mili-second):")

time=nx.dijkstra_path_length(g,'7-Court Square',
                        'A-Fulton Street','dist')

print(time)
