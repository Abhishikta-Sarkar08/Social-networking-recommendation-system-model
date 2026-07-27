import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# Step 1: Read full adjacency matrix from Excel
# -----------------------------
excel_file = "DSAproject.xlsx"
df_full = pd.read_excel(excel_file, index_col=0).fillna(0).astype(int)

# -----------------------------
# Step 2: Limit initial existing users
# -----------------------------
initial_users = ['Ayush', 'Swastika', 'Abhishikta', 'Meghna', 'Akash']
df = df_full.loc[initial_users, initial_users]

# -----------------------------
# Step 3: Save filtered CSV
# -----------------------------
csv_file = "DSAproject_filtered.csv"
df.to_csv(csv_file, index=True)
print(f"Filtered adjacency matrix saved to {csv_file}")

# -----------------------------
# Step 4: Create graph from full adjacency matrix
# -----------------------------
G = nx.from_pandas_adjacency(df_full)

# -----------------------------
# Step 5: Add new user
# -----------------------------
new_node = input("\nEnter your name: ").strip()

if new_node in G.nodes:
    print(f"Node '{new_node}' already exists!")
else:
    G.add_node(new_node)
    if new_node not in df.index:
        df.loc[new_node] = 0
    if new_node not in df.columns:
        df[new_node] = 0

# Show initial users
existing_nodes = initial_users.copy()
print(f"\nSay Hello to your friend: {existing_nodes}")

# Ask for connections
edges = input(f"{new_node}, choose your friends to connect with from the above, separated by commas: ")
edges = [node.strip() for node in edges.split(",") if node.strip()]

# Track new connections
new_connections = []

# Validate and add edges
for node in edges:
    if node not in existing_nodes:
        print(f"Warning: user '{node}' is not in the initial users list. Skipping.")
        continue
    G.add_edge(new_node, node)
    df.at[new_node, node] = 1
    df.at[node, new_node] = 1
    new_connections.append(node)

    # Friend-of-friend recommendation
    friends_of_node = [
        f for f in G.neighbors(node)
        if f != new_node and f not in initial_users and not G.has_edge(new_node, f)
    ]
    if friends_of_node:
        print(f"{node} is connected to {', '.join(friends_of_node)}; do you want to connect to any of them? (yes/no)")
        rec = input().strip().lower()
        if rec == 'yes':
            rec_edges = input(f"Enter the names from {', '.join(friends_of_node)} to connect to, separated by commas: ")
            rec_edges = [f.strip() for f in rec_edges.split(",") if f.strip()]
            for rec_node in rec_edges:
                if rec_node in friends_of_node and not G.has_edge(new_node, rec_node):
                    G.add_edge(new_node, rec_node)
                    df.at[new_node, rec_node] = 1
                    df.at[rec_node, new_node] = 1
                    new_connections.append(rec_node)

# -----------------------------
# Step 6: Save updated adjacency matrix
# -----------------------------
df.to_csv(csv_file, index=True)
print(f"\nUpdated adjacency matrix saved to {csv_file}")

# -----------------------------
# Step 7: Draw full graph (Spiral Layout)
# -----------------------------
plt.figure(figsize=(8, 8))
pos = nx.spiral_layout(G)

node_colors = ["orange" if node == new_node else "lightblue" for node in G.nodes()]
edge_colors = ["red" if new_node in (u, v) else "black" for u, v in G.edges()]

nx.draw(G, pos,
        with_labels=True,
        node_size=1000,
        node_color=node_colors,
        edge_color=edge_colors,
        font_size=6,
        font_weight="bold")

plt.title("Graph Visualization (Spiral Layout)")
plt.show()

# -----------------------------
# Step 8: Draw subgraph of new node and its connections
# -----------------------------
if new_connections:
    sub_nodes = [new_node] + new_connections
    subgraph = G.subgraph(sub_nodes)

    plt.figure(figsize=(6, 6))
    sub_pos = nx.circular_layout(subgraph)

    nx.draw(subgraph, sub_pos,
            with_labels=True,
            node_size=1000,
            node_color=["orange" if node == new_node else "lightgreen" for node in subgraph.nodes()],
            edge_color="blue",
            font_size=8,
            font_weight="bold")

    plt.title(f"{new_node}'s Connections")
    plt.show()

    print(f"\n Hey {new_node}! You have been connected to: {', '.join(new_connections)}")
else:
    print(f"\n{new_node}, You have not been connected to anyone.")
