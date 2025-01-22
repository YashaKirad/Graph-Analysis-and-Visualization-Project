import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from itertools import islice

# File paths
edges_file_path = 'ogbn-arxiv.txt'
labels_file_path = 'ogbn-arxiv_label.csv'


# 1. Incrementally read the edge list (processing large files in chunks)
def read_edges_in_chunks(file_path, chunk_size=10000):
    max_node_id = -1
    with open(file_path) as f:
        while True:
            # Read a chunk of the file
            chunk = list(islice(f, chunk_size))
            if not chunk:
                break
            # Convert the chunk to a list of edge pairs (source, target)
            chunk_data = [tuple(map(int, line.split())) for line in chunk]
            # Update the maximum node ID found
            max_node_id = max(max_node_id, max(max(pair) for pair in chunk_data))
            yield chunk_data, max_node_id


# 2. Create a sparse matrix to store the graph
def build_sparse_graph(edge_chunks):
    row_ind, col_ind = [], []
    num_nodes = 0
    for chunk, max_node_id in edge_chunks:
        # Add each edge to the row and column index lists
        for source, target in chunk:
            row_ind.append(source)
            col_ind.append(target)
        # Update the number of nodes
        num_nodes = max(num_nodes, max_node_id + 1)
    # Create a sparse matrix with ones at the edges' positions
    data = [1] * len(row_ind)
    sparse_graph = csr_matrix((data, (row_ind, col_ind)), shape=(num_nodes, num_nodes))
    return sparse_graph


# Dynamically read edge list and node count
edge_chunks = read_edges_in_chunks(edges_file_path)
sparse_graph = build_sparse_graph(edge_chunks)


# 3. Incrementally read the node labels
def read_labels_in_chunks(file_path, chunk_size=10000):
    label_dict = {}
    # Read the CSV file in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size, header=None, names=['id', 'label']):
        # Add the chunk of labels to the dictionary
        label_dict.update(dict(zip(chunk['id'], chunk['label'])))
    return label_dict


label_dict = read_labels_in_chunks(labels_file_path)


# 4. Convert the sparse matrix to a NetworkX graph object and visualize it
def visualize_graph(sparse_graph, label_dict, sample_size=1000):
    # Create a graph from the sparse matrix
    G = nx.from_scipy_sparse_array(sparse_graph)
    # Take a subgraph of the first sample_size nodes
    subgraph = nx.subgraph(G, list(G.nodes())[:sample_size])

    plt.figure(figsize=(15, 15))
    # Generate positions for the nodes in the subgraph
    pos = nx.spring_layout(subgraph, k=0.5, iterations=50)  # Adjust k and iterations for a more compact layout

    # Draw the subgraph with specific visual properties
    nx.draw(subgraph, pos, with_labels=False, node_size=50, node_color='skyblue', node_shape='o', edge_color='gray',
            alpha=0.7)

    # Add node labels and adjust font size to reduce overlap
    subgraph_labels = {node: label_dict[node] for node in subgraph.nodes if node in label_dict}
    nx.draw_networkx_labels(subgraph, pos, labels=subgraph_labels, font_size=5)

    plt.title(f'Subgraph Visualization with {sample_size} Nodes')
    plt.show()


# Visualize the subgraph
visualize_graph(sparse_graph, label_dict, sample_size=2000)  # Increase sample_size to display more nodes
