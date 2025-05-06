import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from streamlit_agraph import agraph, Node, Edge, Config

def render_mind_map(data):
    """
    Render a mind map visualization using streamlit-agraph
    
    Args:
        data (dict): Mind map data from API
    """
    st.subheader("Mind Map Visualization")
    
    if not data or not data.get("children"):
        st.info("No mind map data available. Try analyzing your idea again or select a different visualization.")
        return
    
    # Create graph
    nodes = []
    edges = []
    
    # Create a unique ID for each node
    node_ids = {}
    node_counter = 0
    
    # Colors for different levels
    colors = ["#4F46E5", "#10B981", "#F59E0B", "#EC4899", "#6366F1"]
    
    def process_node(node_data, parent_id=None, level=0):
        nonlocal node_counter
        
        # Create unique ID for this node
        node_id = f"node_{node_counter}"
        node_counter += 1
        
        # Extract emoji if present
        label = node_data.get("name", "")
        emoji_prefix = ""
        
        # Try to extract emoji
        if label and len(label) > 0:
            first_char = label[0]
            if ord(first_char) > 127:  # Simple check for emoji/special character
                emoji_prefix = first_char
                label = label[1:].strip()
        
        # Add node
        size = 25 if level == 0 else 20 if level == 1 else 15
        nodes.append(Node(
            id=node_id, 
            label=label,
            size=size,
            color=colors[min(level, len(colors)-1)],
            shape="circle" if level < 2 else "box"
        ))
        
        # Add edge if this isn't the root
        if parent_id:
            edges.append(Edge(source=parent_id, target=node_id))
        
        # Process children
        children = node_data.get("children", [])
        for child in children:
            process_node(child, node_id, level + 1)
            
        return node_id
    
    # Process the root node and all children
    root_id = process_node(data, level=0)
    
    # Create config for the graph
    config = Config(
        width=800,
        height=600,
        directed=False,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
    )
    
    # Render the graph
    st.caption("Drag nodes to rearrange • Scroll to zoom • Click nodes to explore relationships")
    agraph(nodes=nodes, edges=edges, config=config)