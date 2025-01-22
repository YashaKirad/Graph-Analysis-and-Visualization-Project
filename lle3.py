import pandas as pd
import networkx as nx
from scipy.sparse import csr_matrix
from itertools import islice
import plotly.graph_objects as go


edges_file_path = 'ogbn-arxiv.txt'
labels_file_path = 'ogbn-arxiv_label.csv'


# 1. Incrementally read the edge list 
def read_edges_in_chunks(file_path, chunk_size=10000):
    max_node_id = -1
    with open(file_path) as f:
        while True:
           
            chunk = list(islice(f, chunk_size))
            if not chunk:
                break
      
            chunk_data = [tuple(map(int, line.split())) for line in chunk]
            
            max_node_id = max(max_node_id, max(max(pair) for pair in chunk_data))
            yield chunk_data, max_node_id


# 2. Create a sparse matrix to store the graph
def build_sparse_graph(edge_chunks):
    row_ind, col_ind = [], []
    num_nodes = 0
    for chunk, max_node_id in edge_chunks:
        
        for source, target in chunk:
            row_ind.append(source)
            col_ind.append(target)
       
        num_nodes = max(num_nodes, max_node_id + 1)
  
    data = [1] * len(row_ind)
    sparse_graph = csr_matrix((data, (row_ind, col_ind)), shape=(num_nodes, num_nodes))
    return sparse_graph


edge_chunks = read_edges_in_chunks(edges_file_path)
sparse_graph = build_sparse_graph(edge_chunks)

# 3. Incrementally read the node labels
def read_labels_in_chunks(file_path, chunk_size=10000):
    label_dict = {}
  
    for chunk in pd.read_csv(file_path, chunksize=chunk_size, header=None, names=['id', 'label']):
        
        label_dict.update(dict(zip(chunk['id'], chunk['label'])))
    return label_dict


label_dict = read_labels_in_chunks(labels_file_path)


# 4. Convert the sparse matrix to a NetworkX graph object and visualize it using Plotly in 3D
def visualize_graph_3d(sparse_graph, label_dict, sample_size=1000):
    
    G = nx.from_scipy_sparse_array(sparse_graph)
    
    if G.number_of_nodes() == 0:
        raise ValueError("The graph has no nodes!")

    
    subgraph_nodes = list(G.nodes())[:sample_size]
    subgraph = G.subgraph(subgraph_nodes)

  
    pos = nx.spring_layout(subgraph, dim=3, k=0.5, iterations=50)  

    edge_x = []
    edge_y = []
    edge_z = []
    for edge in subgraph.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_z = []
    node_text = []
    for node in subgraph.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

        node_text.append(label_dict.get(node, ''))

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=5,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'3D Subgraph Visualization',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        scene=dict(
                            xaxis=dict(showbackground=False),
                            yaxis=dict(showbackground=False),
                            zaxis=dict(showbackground=False)
                        ),
                        annotations=[dict(
                            text="Graph generated using Plotly 3D",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                    )
                   )
    
    fig.show()



visualize_graph_3d(sparse_graph, label_dict, sample_size=2000)
