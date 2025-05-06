import streamlit as st
import pandas as pd
import json

def render_timeline(data):
    """
    Render timeline visualization
    
    Args:
        data (dict): Timeline data from API
    """
    st.subheader("Implementation Timeline")
    
    events = data.get("events", [])
    
    # Handle empty data
    if not events:
        st.info("No timeline data available. Try analyzing your idea again or select a different visualization.")
        st.caption("The timeline provides a phased implementation roadmap for your idea.")
        return
    
    # Add description
    st.markdown("""
    This timeline provides a phased approach to implementing your idea, breaking down the process into manageable steps.
    Each phase contains key milestones and activities to help guide your development process.
    """)
    
    # Group events by phase
    phases = {}
    for event in events:
        phase = event.get("date", "").split('.')[0]  # Extract phase from date
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(event)
    
    # Create phase navigation
    st.write("Jump to phase:")
    
    # Create a row of phase buttons
    phase_cols = st.columns(min(5, len(phases)))
    
    # Default active phase from session state or set to first phase
    if 'active_phase' not in st.session_state or st.session_state.active_phase not in phases:
        if phases:
            st.session_state.active_phase = list(phases.keys())[0]
    
    # Phase navigation buttons
    for i, (phase, _) in enumerate(phases.items()):
        col_idx = i % len(phase_cols)
        with phase_cols[col_idx]:
            button_type = "primary" if st.session_state.active_phase == phase else "secondary"
            if st.button(phase, key=f"phase_{i}", type=button_type):
                st.session_state.active_phase = phase
                st.rerun()
    
    # Display timeline with active phase expanded
    for phase, phase_events in phases.items():
        is_active = phase == st.session_state.active_phase
        with st.expander(f"**{phase}** ({len(phase_events)} events)", expanded=is_active):
            for event in phase_events:
                with st.container():
                    # Create a timeline event card
                    st.markdown(f"<div class='timeline-event'>", unsafe_allow_html=True)
                    
                    # Two-column layout: date and content
                    col1, col2 = st.columns([1, 5])
                    
                    with col1:
                        st.markdown(f"<div class='timeline-date'>{event.get('date', '')}</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"### {event.get('title', '')}")
                        
                        # Process content with bullet points
                        content = event.get('content', '')
                        if "• " in content or "- " in content:
                            lines = content.split("\n")
                            for line in lines:
                                line = line.strip()
                                if line.startswith("• ") or line.startswith("- "):
                                    st.markdown(line)
                                elif line:
                                    st.write(line)
                        else:
                            st.write(content)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("---")
    
    # Add export options
    with st.expander("Export Options"):
        # Create a dataframe from events for CSV export
        events_df = pd.DataFrame([
            {
                "Phase": event.get("date", "").split('.')[0],
                "Date": event.get("date", ""),
                "Title": event.get("title", ""),
                "Content": event.get("content", "").replace("\n", " ")
            }
            for event in events
        ])
        
        # Download as CSV
        st.download_button(
            label="Download Timeline (CSV)",
            data=events_df.to_csv(index=False).encode('utf-8'),
            file_name="implementation_timeline.csv",
            mime="text/csv",
            key="download_timeline_csv"
        )
        
        # Download as JSON
        json_str = json.dumps({"events": events}, indent=2)
        st.download_button(
            label="Download Timeline (JSON)",
            data=json_str,
            file_name="implementation_timeline.json",
            mime="application/json",
            key="download_timeline_json"
        )
        
        # View raw data
        st.json({"events": events})