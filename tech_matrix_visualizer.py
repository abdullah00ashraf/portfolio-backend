import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd
import os

# --- SYSTEM THEME & DIRECTORY SETUP ---
# Tactical Dark Mode Palette
BG_COLOR = '#050505'
GRID_COLOR = '#1a1a1a'
TEXT_COLOR = '#888888'
GREEN_ACCENT = '#00ff41'
AMBER_ACCENT = '#ffb000'
CRIMSON_ACCENT = '#cc0000'

plt.rcParams.update({
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': BG_COLOR,
    'axes.edgecolor': GRID_COLOR,
    'text.color': TEXT_COLOR,
    'axes.labelcolor': TEXT_COLOR,
    'xtick.color': TEXT_COLOR,
    'ytick.color': TEXT_COLOR,
    'font.family': 'monospace'
})

# Create output directory
OUTPUT_DIR = "portfolio_visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================
# VISUAL 01: CAPABILITY RADAR (WEIGHTS)
# ==========================================
def generate_radar_chart():
    categories = ['AI & ML Models', 'Edge Infrastructure', 'Cryptography Vaults', 'Low-Level Execution', 'Heuristic Ops', 'Data Parsing']
    N = len(categories)
    
    # Capability weights (out of 1.0)
    values = [0.98, 0.92, 0.95, 0.88, 0.90, 0.94]
    values += values[:1] # Close the loop
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Draw one axe per variable and add labels
    plt.xticks(angles[:-1], categories, color=GREEN_ACCENT, size=10)
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "MAX"], color=GRID_COLOR, size=8)
    plt.ylim(0, 1.1)
    
    # Plot and fill
    ax.plot(angles, values, linewidth=2, linestyle='solid', color=GREEN_ACCENT)
    ax.fill(angles, values, color=GREEN_ACCENT, alpha=0.1)
    ax.grid(color=GRID_COLOR)
    ax.spines['polar'].set_color(GRID_COLOR)
    
    plt.title('// SYSTEM CAPABILITY WEIGHTS', size=14, color=AMBER_ACCENT, y=1.1)
    plt.savefig(f"{OUTPUT_DIR}/capability_radar.svg", format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    print("[SUCCESS] Capability Radar generated.")

# ==========================================
# VISUAL 02: COMPONENT SYNERGY HEATMAP
# ==========================================
def generate_synergy_matrix():
    # Key technologies to map against each other
    techs = ['FastAPI', 'PyTorch', 'PINNs', 'PostgreSQL', 'AES-256', 'LLVM IR', 'Bi-LSTM', 'Llama 3']
    
    # Simulated synergy/interaction matrix (0.0 to 1.0)
    data = np.array([
        [1.0, 0.8, 0.6, 0.9, 0.7, 0.4, 0.8, 0.9],
        [0.8, 1.0, 0.9, 0.5, 0.3, 0.7, 0.9, 0.6],
        [0.6, 0.9, 1.0, 0.4, 0.2, 0.8, 0.7, 0.3],
        [0.9, 0.5, 0.4, 1.0, 0.9, 0.3, 0.5, 0.6],
        [0.7, 0.3, 0.2, 0.9, 1.0, 0.6, 0.4, 0.5],
        [0.4, 0.7, 0.8, 0.3, 0.6, 1.0, 0.5, 0.8],
        [0.8, 0.9, 0.7, 0.5, 0.4, 0.5, 1.0, 0.7],
        [0.9, 0.6, 0.3, 0.6, 0.5, 0.8, 0.7, 1.0]
    ])
    
    df = pd.DataFrame(data, columns=techs, index=techs)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    # Custom dark green/amber color map
    cmap = sns.dark_palette(GREEN_ACCENT, as_cmap=True)
    
    sns.heatmap(df, annot=True, fmt=".2f", cmap=cmap, cbar=False, 
                linewidths=1, linecolor=BG_COLOR, 
                annot_kws={"color": TEXT_COLOR, "size": 9})
    
    plt.title('// COMPONENT SYNERGY & DATA FLOW MATRIX', size=14, color=AMBER_ACCENT, pad=20)
    plt.xticks(rotation=45, ha='right', color=GREEN_ACCENT)
    plt.yticks(rotation=0, color=GREEN_ACCENT)
    
    plt.savefig(f"{OUTPUT_DIR}/synergy_heatmap.svg", format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    print("[SUCCESS] Synergy Heatmap generated.")

# ==========================================
# VISUAL 03: ARCHITECTURE TOPOLOGY NETWORK
# ==========================================
def generate_topology_network():
    G = nx.Graph()
    
    # Nodes: Domains
    G.add_node("SYSTEM_CORE", layer=0, color=AMBER_ACCENT, size=3000)
    
    # Nodes: Subsystems
    subsystems = ["EDGE_API", "COGNITIVE_ENGINE", "CRYPTO_VAULT", "EXECUTION_JIT"]
    for sub in subsystems:
        G.add_node(sub, layer=1, color=GREEN_ACCENT, size=1500)
        G.add_edge("SYSTEM_CORE", sub, weight=3)
        
    # Nodes: Tech Stack (Leaves)
    edge_tech = ["FastAPI", "Redis", "Vanilla_JS", "Leaflet"]
    cog_tech = ["PyTorch", "PINNs", "Llama_3", "Bi-LSTM", "HuggingFace"]
    crypto_tech = ["AES-256", "Post-Quantum", "mTLS_1.3", "PostgreSQL"]
    exec_tech = ["Python", "C", "LLVM_IR", "JIT"]
    
    def add_leaves(parent, leaves):
        for leaf in leaves:
            G.add_node(leaf, layer=2, color=TEXT_COLOR, size=600)
            G.add_edge(parent, leaf, weight=1)
            
    add_leaves("EDGE_API", edge_tech)
    add_leaves("COGNITIVE_ENGINE", cog_tech)
    add_leaves("CRYPTO_VAULT", crypto_tech)
    add_leaves("EXECUTION_JIT", exec_tech)
    
    # Layout mathematics
    pos = nx.spring_layout(G, k=0.85, seed=42)
    
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    sizes = [node[1]['size'] for node in G.nodes(data=True)]
    
    plt.figure(figsize=(12, 10))
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color=GRID_COLOR, width=1.5, alpha=0.8)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=BG_COLOR, node_size=sizes, 
                           edgecolors=colors, linewidths=2)
    
    # Draw labels
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color='#ffffff', font_family='monospace')
    
    plt.title('// ARCHITECTURAL TOPOLOGY GRAPH', size=14, color=AMBER_ACCENT, loc='left')
    plt.axis('off')
    
    plt.savefig(f"{OUTPUT_DIR}/topology_network.svg", format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    print("[SUCCESS] Topology Network generated.")

if __name__ == "__main__":
    print("Initializing Systems Architecture Rendering Engine...")
    generate_radar_chart()
    generate_synergy_matrix()
    generate_topology_network()
    print(f"\n[INFO] All visual telemetry saved to ./{OUTPUT_DIR}/")
    print("[INFO] Vectors ready for frontend DOM injection.")
