# Graph Analysis and Visualization Project

This project focuses on analyzing and visualizing large graph datasets, with functionalities for incremental reading, sparse matrix representation, and interactive visualizations in both 2D and 3D.

---

## Objectives and Outputs

### 1. `ll.py`
- **Objective**:
  - Reads a large edge list incrementally and constructs a sparse matrix representation of the graph.
  - Associates node labels with the graph using data from a CSV file.
  - Visualizes the graph using `matplotlib`.
- **Output**:
  - Subgraph visualization (2D) with color-coded nodes and labels.
  - A graph object stored as a sparse matrix for efficient computations.


### 2. `lle3.py`
- **Objective**:
  - Extends the functionality of `lle.py` by creating a 3D interactive visualization of the graph using `Plotly`.
  - Utilizes a spring layout algorithm to position nodes in 3D space.
- **Output**:
  - Interactive 3D graph visualization with hoverable node information.
  - A novel way to analyze graph structures in 3D.

---

## Libraries Used

1. **`pandas`**:
   - Used for reading and handling CSV files containing node labels.
   - Enables incremental processing of large datasets.

2. **`networkx`**:
   - Provides tools for creating, analyzing, and manipulating graphs.
   - Converts sparse matrices into graph objects for visualization.

3. **`matplotlib`**:
   - Used in `ll.py` for static 2D graph visualization.
   - Allows customization of node and edge styles.

4. **`scipy`**:
   - Provides sparse matrix representations for efficient storage of large graphs.
   - Essential for handling graphs with millions of nodes and edges.

5. **`plotly`**:
   - Used in `lle.py` and `lle3.py` for interactive graph visualizations in 2D and 3D.
   - Enhances user interaction with hover information and zoom functionalities.

6. **`itertools`**:
   - Enables efficient incremental reading of edge data in chunks.

---

## Features

- **Incremental Data Reading**:
  - Handles large graph datasets by reading edges and labels in chunks.

- **Sparse Matrix Representation**:
  - Efficiently stores and processes graphs with millions of nodes and edges.

- **Graph Visualizations**:
  - `ll.py`: Static 2D visualization using `matplotlib`.
  - `lle3.py`: Interactive 3D visualization using `Plotly`.

- **Node Label Integration**:
  - Associates labels with graph nodes for better analysis and visualization.

- **Interactive Features**:
  - Hover tooltips for nodes.
  - Zoom and rotate capabilities in 3D visualizations.

---


