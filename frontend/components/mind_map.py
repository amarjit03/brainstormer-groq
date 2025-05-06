import streamlit as st
import json
import random
from streamlit_agraph import agraph, Node, Edge, Config

def render_mind_map(data):
    """
    Render a mind map visualization using streamlit-agraph
    
    Args:
        data (dict): Mind map data from API
    """
    st.subheader("Mind Map Visualization")
    
    # Handle empty data
    if not data or not data.get("children"):
        st.info("No mind map data available. Try analyzing your idea again or select a different visualization.")
        st.caption("Mind maps show the relationships between different aspects of your idea, helping you visualize the overall concept.")
        return
    
    # Add description
    st.markdown("""
    This mind map visualizes the key components of your idea and how they relate to each other.
    - **Drag nodes** to rearrange the layout
    - **Hover over nodes** to see details
    - **Zoom and pan** to explore complex relationships
    """)
    
    # Create graph
    nodes = []
    edges = []
    
    # Create a unique ID for each node
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
        
        # Add node
        size = 30 if level == 0 else 24 if level == 1 else 20
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
        collapsible=False,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": False}
    )
    
    # Render the graph
    st.caption("Drag nodes to rearrange • Scroll to zoom • Click nodes to explore relationships")
    
    # Try to render the graph, with fallback to JSON display
    try:
        agraph(nodes=nodes, edges=edges, config=config)
    except Exception as e:
        st.error(f"Could not render mind map visualization: {str(e)}")
        st.json(data)
    
    # Add export options
    with st.expander("Export Options"):
        # Download as JSON
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="Download Mind Map (JSON)",
            data=json_str,
            file_name="mind_map.json",
            mime="application/json"
        )
        
        # View raw data
        st.json(data)