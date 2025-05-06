import streamlit as st
from utils.api import get_templates

def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.title("💡 Idea Analyzer")
        st.markdown("---")
        
        # Template selection
        st.subheader("Analysis Template")
        
        # Get templates from API or use defaults
        templates = get_templates()
        
        template_options = list(templates.keys())
        template_labels = list(templates.values())
        
        # Find the index of the currently selected template
        selected_template_index = 0
        if st.session_state.template_type in template_options:
            selected_template_index = template_options.index(st.session_state.template_type)
        
        template_selection = st.selectbox(
            "Select analysis template",
            options=range(len(template_options)),
            format_func=lambda i: template_labels[i],
            index=selected_template_index,
            key="template_selection"
        )
        
        st.session_state.template_type = template_options[template_selection]
        
        # Template descriptions
        template_descriptions = {
            "business_idea": "Comprehensive analysis of business viability, market opportunity, and implementation strategy.",
            "swot": "Strengths, Weaknesses, Opportunities, and Threats analysis for your idea.",
            "product_features": "Detailed breakdown of product features, priorities, and development roadmap."
        }
        
        current_template = st.session_state.template_type
        if current_template in template_descriptions:
            st.caption(template_descriptions[current_template])
        
        # Visualization options (only show if analysis exists)
        if st.session_state.analysis is not None:
            st.markdown("---")
            st.subheader("Visualization")
            
            view_options = {
                "mind_map": "🔄 Mind Map",
                "cards": "🃏 Cards",
                "timeline": "📅 Timeline",
                "raw": "📝 Raw Analysis"
            }
            
            # Create a container for the buttons
            view_container = st.container()
            
            with view_container:
                for view_id, view_name in view_options.items():
                    button_type = "primary" if st.session_state.current_view == view_id else "secondary"
                    if st.button(
                        view_name,
                        key=f"view_{view_id}",
                        help=f"Switch to {view_name} view",
                        use_container_width=True,
                        type=button_type
                    ):
                        st.session_state.current_view = view_id
                        st.rerun()
            
            # View descriptions
            view_descriptions = {
                "mind_map": "Visual representation of idea concepts and their relationships.",
                "cards": "Key aspects of your idea organized into searchable cards.",
                "timeline": "Implementation roadmap and phased approach.",
                "raw": "Complete text analysis of your idea."
            }
            
            current_view = st.session_state.current_view
            if current_view in view_descriptions:
                st.caption(view_descriptions[current_view])
        
        # Footer
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.caption("© 2025 Idea Analyzer")
        with col2:
            st.caption("Powered by Groq LLM")