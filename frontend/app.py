import streamlit as st
import os
import json

# Import components
from components.sidebar import render_sidebar
from components.mind_map import render_mind_map
from components.cards_view import render_cards
from components.timeline_view import render_timeline
from components.raw_view import render_raw_analysis

# Import utilities
from utils.api import analyze_idea, get_templates

# Set page configuration
st.set_page_config(
    page_title="Idea Analyzer",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open(os.path.join("styles", "custom.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'current_view' not in st.session_state:
    st.session_state.current_view = "mind_map"
if 'template_type' not in st.session_state:
    st.session_state.template_type = "business_idea"
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = set()

def reset_analysis():
    """Reset the analysis state"""
    st.session_state.analysis = None
    st.session_state.expanded_sections = set()

def main():
    # Load CSS
    try:
        load_css()
    except:
        st.warning("Could not load custom CSS styles.")
    
    # Render sidebar
    render_sidebar()
    
    # Main content
    if st.session_state.analysis is None:
        # Input form
        st.title("💡 Idea Analyzer")
        st.markdown("Describe your business or project idea in detail, and our AI will analyze it for you.")
        
        with st.form("idea_input_form"):
            idea = st.text_area(
                "Your idea",
                height=200,
                placeholder="Enter your idea here... (e.g., A social media platform that connects local farmers directly with consumers, allowing people to buy fresh produce straight from nearby farms)",
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                analyze_button = st.form_submit_button("Analyze My Idea", use_container_width=True)
            
        if analyze_button and idea:
            with st.spinner("Analyzing your idea... This may take up to 60 seconds."):
                try:
                    response = analyze_idea(
                        idea, 
                        st.session_state.template_type,
                        ["mind_map", "cards", "timeline"]
                    )
                    st.session_state.analysis = response
                    st.rerun()
                except Exception as e:
                    st.error(f"Error analyzing idea: {str(e)}")
    else:
        # Display analysis results
        analysis = st.session_state.analysis
        
        # Header
        st.title(analysis.get("title", "Analysis Results"))
        st.markdown(f"<div class='analysis-meta'>Processing time: {analysis.get('processingTime', '0')} seconds</div>", 
                   unsafe_allow_html=True)
        
        # Button to start over
        if st.button("Analyze Another Idea", key="reset_button", type="primary"):
            reset_analysis()
            st.rerun()
        
        # Display current visualization
        current_view = st.session_state.current_view
        
        if current_view == "mind_map":
            render_mind_map(analysis.get("visualizations", {}).get("mindMap", {}))
        elif current_view == "cards":
            render_cards(analysis.get("visualizations", {}).get("cards", {}))
        elif current_view == "timeline":
            render_timeline(analysis.get("visualizations", {}).get("timeline", {}))
        elif current_view == "raw":
            render_raw_analysis(analysis.get("rawAnalysis", ""))

if __name__ == "__main__":
    main()