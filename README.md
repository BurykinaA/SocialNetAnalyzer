# SocialNetAnalyzer

![image](https://github.com/user-attachments/assets/146e741c-c5d7-43e2-8f23-22f79e00493e)

![image](https://github.com/user-attachments/assets/4d0eef45-d047-45c3-8195-6311a81930d2)



## Overview

The goal of this project is to perform descriptive analysis of your social ego-network (a network of your connections, excluding yourself). The project consists of the following steps:

1. **Data Collection**: Gather data from an online service (VK) and create a network of your friends (first-order connections only).
2. **Analysis and Visualization**: Analyse the collected data and prepare visualizations.

## Project Structure

The repository includes the following files:

- **`alina_analysis.ipynb`**: A Jupyter Notebook containing the main analysis and visualizations.
- **`data_collect.py`**: Python script for collecting and preprocessing data from the selected social network.
- **`network_visualization.html`**: Interactive visualization of the network, generated as an HTML file.
- **`README.md`**: This file, describing the project's purpose, structure, and usage.

## Requirements

- Python 3.9+
Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Analysis Summary

- **Network Type**: Indicate whether the graph is directed/undirected, weighted/unweighted, homogeneous/heterogeneous.
- **Attributes**:
  - Nodes: Attributes like city, gender, education status.
  - Edges: Relationship strength or interaction frequency.
- **Basic Metrics**:
  - Number of nodes and edges.
  - Diameter, radius, clustering coefficients (global, average local, histogram of locals).
  - Average shortest path length (with histogram).
  - Degree distribution analysis, including parameter fitting (e.g., regression, MLE).

## Structural Analysis

- Compare the ego-network with random graph models (ER, BA, WS) by verifying properties of real-world networks.
- Centralities:
  - Degree, closeness, betweenness, and optionally Katz and Bonacich centralities.
  - Interpretation of central nodes (roles in the network, not just names).
- Prestige measures: PageRank, HITS (for directed networks).
- Assortative Mixing: Examine node attributes like gender, city, or education for correlation.
- Node similarity: Analyse structural equivalence and roles in the network.

## Community Detection

- Perform clique and k-core analysis with visualization.
- Apply multiple community detection algorithms and evaluate using metrics like modularity or silhouette scores.


