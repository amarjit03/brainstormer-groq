# import streamlit as st
# import requests
# import json
# from components.sidebar import render_sidebar
# from components.mind_map import render_mind_map
# from components.cards_view import render_cards
# from components.timeline_view import render_timeline
# from utils.app import analyze_idea, visualize_content

# # Set page configuration
# st.set_page_config(
#     page_title="Idea Analyzer",
#     page_icon="💡",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize session state
# if 'analysis' not in st.session_state:
#     st.session_state.analysis = None
# if 'current_view' not in st.session_state:
#     st.session_state.current_view = "mind_map"
# if 'template_type' not in st.session_state:
#     st.session_state.template_type = "business_idea"

# def reset_analysis():
#     st.session_state.analysis = None

# # Render sidebar
# render_sidebar()

# # Main content
# if st.session_state.analysis is None:
#     # Input form
#     st.title("💡 Idea Analyzer")
#     st.markdown("Describe your business or project idea in detail, and our AI will analyze it for you.")
    
#     with st.form("idea_input_form"):
#         idea = st.text_area(
#             "Your idea",
#             height=200,
#             placeholder="Enter your idea here... (e.g., A social media platform that connects local farmers directly with consumers, allowing people to buy fresh produce straight from nearby farms)",
#         )
        
#         col1, col2 = st.columns([1, 3])
#         with col1:
#             analyze_button = st.form_submit_button("Analyze My Idea")
        
#     if analyze_button and idea:
#         with st.spinner("Analyzing your idea..."):
#             try:
#                 response = analyze_idea(
#                     idea, 
#                     st.session_state.template_type,
#                     ["mind_map", "cards", "timeline"]
#                 )
#                 st.session_state.analysis = response
#             except Exception as e:
#                 st.error(f"Error analyzing idea: {str(e)}")
# else:
#     # Display analysis results
#     analysis = st.session_state.analysis
    
#     # Header
#     st.title(analysis.get("title", "Analysis Results"))
#     st.caption(f"Processing time: {analysis.get('processingTime', '0')} seconds")
    
#     # Button to start over
#     if st.button("Analyze Another Idea", key="reset_button"):
#         reset_analysis()
#         st.experimental_rerun()
    
#     # Display current visualization
#     current_view = st.session_state.current_view
    
#     if current_view == "mind_map":
#         render_mind_map(analysis.get("visualizations", {}).get("mindMap", {}))
#     elif current_view == "cards":
#         render_cards(analysis.get("visualizations", {}).get("cards", {}))
#     elif current_view == "timeline":
#         render_timeline(analysis.get("visualizations", {}).get("timeline", {}))
#     elif current_view == "raw":
#         st.subheader("Raw Analysis")
#         st.text_area("", value=analysis.get("rawAnalysis", ""), height=500, key="raw_analysis")

# # Add custom CSS
# st.markdown("""
# <style>
#     .main .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#     }
#     h1 {
#         margin-bottom: 1rem;
#     }
#     .stButton button {
#         background-color: #4F46E5;
#         color: white;
#         border-radius: 0.5rem;
#     }
#     .stButton button:hover {
#         background-color: #3730A3;
#     }
# </style>
# """, unsafe_allow_html=True)

import streamlit as st
import requests
import json
import pandas as pd
import re

# Set page configuration
st.set_page_config(
    page_title="Idea Analyzer",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'current_view' not in st.session_state:
    st.session_state.current_view = "mind_map"
if 'template_type' not in st.session_state:
    st.session_state.template_type = "business_idea"
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = set()

# API endpoint
BASE_URL = "https://brainstormer-groq.onrender.com/api"

# API functions
def analyze_idea(idea, template_type, formats):
    """Send idea to backend for analysis"""
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={
                "idea": idea,
                "template": template_type,
                "formats": formats
            },
            timeout=120
        )
        
        if response.status_code != 200:
            error_msg = f"API error: {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg = error_data["error"]
            except:
                pass
            raise Exception(error_msg)
        
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Request error: {str(e)}")

def get_templates():
    """Get available templates"""
    return {
        "business_idea": "Business Idea Analysis",
        "swot": "SWOT Analysis",
        "product_features": "Product Feature Analysis"
    }

def parse_raw_analysis(raw_text):
    """Parse raw analysis text into sections with emoji and content"""
    sections = []
    
    # Match emoji, section title, and content using regex
    pattern = r'([\u2600-\u27BF\U0001F300-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF])\s*\d*\.\s*\*\*(.*?)\*\*([\s\S]*?)(?=[\u2600-\u27BF\U0001F300-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]\s*\d*\.\s*\*\*|$)'
    
    matches = re.finditer(pattern, raw_text)
    
    for match in matches:
        emoji = match.group(1)
        title = match.group(2).strip()
        content = match.group(3).strip()
        
        sections.append({
            "emoji": emoji,
            "title": title,
            "content": content
        })
    
    return sections

# Sidebar
with st.sidebar:
    st.title("Idea Analyzer")
    st.markdown("---")
    
    # Template selection
    st.subheader("Template")
    templates = get_templates()
    
    template_options = list(templates.keys())
    template_labels = list(templates.values())
    
    selected_template_index = template_options.index(st.session_state.template_type) if st.session_state.template_type in template_options else 0
    
    template_selection = st.selectbox(
        "Select analysis template",
        options=range(len(template_options)),
        format_func=lambda i: template_labels[i],
        index=selected_template_index,
        key="template_selection"
    )
    
    st.session_state.template_type = template_options[template_selection]
    
    # Visualization options (only show if analysis exists)
    if st.session_state.analysis is not None:
        st.markdown("---")
        st.subheader("Visualization")
        
        view_options = {
            "mind_map": "🔄 Mind Map",
            "cards": "🃏 Cards",
            "timeline": "📅 Timeline",
            "raw": "📝 Raw Analysis",
            "detailed": "🔍 Detailed Analysis"
        }
        
        for view_id, view_name in view_options.items():
            if st.button(
                view_name,
                key=f"view_{view_id}",
                help=f"Switch to {view_name} view",
                use_container_width=True,
                type="secondary" if st.session_state.current_view != view_id else "primary"
            ):
                st.session_state.current_view = view_id
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    st.caption("Powered by Groq LLM")

# Render functions for different visualizations
def render_mind_map(data):
    st.subheader("Mind Map Visualization")
    
    if not data or not data.get("children"):
        st.info("No mind map data available. Try analyzing your idea again or select a different visualization.")
        return
    
    st.json(data)  # For now just display JSON data
    st.info("Mind map visualization would be displayed here with proper graphics library.")

def render_cards(data):
    st.subheader("Cards Visualization")
    
    cards = data.get("cards", [])
    
    if not cards:
        st.info("No card data available. Try analyzing your idea again or select a different visualization.")
        return
    
    # Search and filter
    search_term = st.text_input("Search cards", key="card_search_input")
    
    filter_options = ["All", "Business", "Technical", "Planning"]
    selected_filter = st.selectbox("Category", filter_options, key="card_filter_input")
    
    # Filter cards
    filtered_cards = cards
    
    # Apply category filter
    if selected_filter != "All":
        category_keywords = {
            "Business": ["business", "model", "revenue", "market", "competitor", "edge"],
            "Technical": ["tools", "technologies", "risks"],
            "Planning": ["tasks", "roadmap", "strategy", "features"]
        }
        
        keywords = category_keywords.get(selected_filter, [])
        if keywords:
            filtered_cards = [
                card for card in cards
                if any(keyword in card.get("title", "").lower() or 
                       keyword in card.get("content", "").lower() 
                       for keyword in keywords)
            ]
    
    # Apply search filter
    if search_term:
        search_term = search_term.lower()
        filtered_cards = [
            card for card in filtered_cards
            if search_term in card.get("title", "").lower() or 
               search_term in card.get("content", "").lower()
        ]
    
    # Show count
    st.caption(f"Showing {len(filtered_cards)} of {len(cards)} cards")
    
    # No results
    if not filtered_cards:
        st.warning(f"No cards match your search for '{search_term}'")
        return
    
    # Display cards in a grid (3 columns)
    cols = st.columns(3)
    
    for i, card in enumerate(filtered_cards):
        col_idx = i % 3
        
        with cols[col_idx]:
            with st.expander(f"{card.get('emoji', '')} {card.get('title', 'Card')}", expanded=False):
                content = card.get("content", "")
                st.write(content)

def render_timeline(data):
    st.subheader("Implementation Timeline")
    
    events = data.get("events", [])
    
    if not events:
        st.info("No timeline data available. Try analyzing your idea again or select a different visualization.")
        return
    
    for event in events:
        with st.expander(f"**{event.get('date', '')}**: {event.get('title', '')}", expanded=False):
            st.write(event.get('content', ''))

def render_raw_analysis(raw_text):
    st.subheader("Raw Analysis")
    
    if not raw_text:
        st.info("No analysis data available.")
        return
    
    st.text_area("", value=raw_text, height=500, key="raw_analysis")
    
    # Download button for raw analysis
    st.download_button(
        label="Download Raw Analysis",
        data=raw_text,
        file_name="idea_analysis.txt",
        mime="text/plain",
        key="download_raw"
    )

def render_detailed_analysis(raw_text):
    st.subheader("Detailed Analysis")
    
    if not raw_text:
        st.info("No analysis data available.")
        return
    
    # Parse the raw text into sections
    sections = parse_raw_analysis(raw_text)
    
    if not sections:
        st.warning("Could not parse the analysis into sections. Showing raw text instead.")
        st.text_area("", value=raw_text, height=500)
        return
    
    # Add controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Search analysis", key="detailed_search")
    
    with col2:
        if st.button("Expand All", key="expand_all"):
            st.session_state.expanded_sections = set(range(len(sections)))
    
    with col3:
        if st.button("Collapse All", key="collapse_all"):
            st.session_state.expanded_sections = set()
    
    # Display sections in a visually appealing way
    for i, section in enumerate(sections):
        # Check if section matches search term
        if search_term and search_term.lower() not in section["title"].lower() and search_term.lower() not in section["content"].lower():
            continue
            
        # Create a colored container for each section
        with st.container():
            # Header with emoji and title
            header_col1, header_col2 = st.columns([0.1, 0.9])
            
            with header_col1:
                st.markdown(f"<h2 style='margin: 0; font-size: 2.5rem;'>{section['emoji']}</h2>", unsafe_allow_html=True)
            
            with header_col2:
                st.markdown(f"<h3 style='margin: 0;'>{section['title']}</h3>", unsafe_allow_html=True)
            
            # Determine if this section should be expanded
            is_expanded = i in st.session_state.expanded_sections
            
            # Show content in an expander
            with st.expander("Show content", expanded=is_expanded):
                # Format the content with proper markdown
                content = section["content"]
                
                # Check if content has bullet points
                if "• " in content or "- " in content:
                    lines = content.split('\n')
                    formatted_lines = []
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith("• ") or line.startswith("- "):
                            formatted_lines.append(line)
                        elif line:
                            formatted_lines.append(line)
                    
                    formatted_content = '\n'.join(formatted_lines)
                    st.markdown(formatted_content)
                else:
                    st.markdown(content)
                
                # Add to expanded sections if user expands manually
                if not is_expanded:
                    st.session_state.expanded_sections.add(i)
            
            # Remove from expanded sections if user collapses manually
            if is_expanded and i in st.session_state.expanded_sections:
                st.session_state.expanded_sections.remove(i)
            
            # Add a divider between sections
            st.markdown("---")
    
    # Add download and share options
    st.markdown("### Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download as Text",
            data=raw_text,
            file_name="detailed_analysis.txt",
            mime="text/plain",
            key="download_detailed"
        )
    
    with col2:
        st.download_button(
            label="Download as Markdown",
            data=raw_text,
            file_name="detailed_analysis.md",
            mime="text/markdown",
            key="download_md"
        )

def reset_analysis():
    st.session_state.analysis = None
    st.session_state.expanded_sections = set()

# Main content area
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
        
        analyze_button = st.form_submit_button("Analyze My Idea")
    
    if analyze_button and idea:
        with st.spinner("Analyzing your idea..."):
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
    st.caption(f"Processing time: {analysis.get('processingTime', '0')} seconds")
    
    # Button to start over
    if st.button("Analyze Another Idea", key="reset_button"):
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
    elif current_view == "detailed":
        render_detailed_analysis(analysis.get("rawAnalysis", ""))

# Add custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        margin-bottom: 1rem;
    }
    /* Custom styling for the detailed analysis view */
    .stExpander {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    .stExpander:hover {
        border-color: #b0b0b0;
    }
</style>
""", unsafe_allow_html=True)