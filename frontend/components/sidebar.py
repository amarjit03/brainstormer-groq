import streamlit as st
from utils.app import get_templates

def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.title("Idea Analyzer")
        st.markdown("---")
        
        # Template selection
        st.subheader("Template")
        
        # Get templates from API or use defaults
        templates = get_templates()
        
        template_options = []
        template_labels = []
        
        for template_id, template_name in templates.items():
            template_options.append(template_id)
            template_labels.append(template_name)
        
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
                "raw": "📝 Raw Analysis"
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
                    st.session_state["rerun_trigger"] = not st.session_state.get("rerun_trigger", False)
        
        # Footer
        st.markdown("---")
        st.caption("Powered by Groq LLM")