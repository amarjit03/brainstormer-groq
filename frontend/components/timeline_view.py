import streamlit as st
import pandas as pd

def render_timeline(data):
    """
    Render timeline visualization
    
    Args:
        data (dict): Timeline data from API
    """
    st.subheader("Implementation Timeline")
    
    events = data.get("events", [])
    
    if not events:
        st.info("No timeline data available. Try analyzing your idea again or select a different visualization.")
        return
    
    # Group events by phase
    phases = {}
    for event in events:
        phase = event.get("date", "").split('.')[0]
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(event)
    
    # Create phase navigation
    st.write("Jump to phase:")
    
    phase_cols = st.columns(min(5, len(phases)))
    for i, (phase, _) in enumerate(phases.items()):
        col_idx = i % len(phase_cols)
        with phase_cols[col_idx]:
            if st.button(phase, key=f"phase_{i}"):
                st.session_state.active_phase = phase
    
    # Render timeline
    for phase, phase_events in phases.items():
        with st.expander(f"**{phase}** ({len(phase_events)} events)", expanded=True):
            for event in phase_events:
                with st.container():
                    col1, col2 = st.columns([1, 5])
                    
                    with col1:
                        st.markdown(f"**{event.get('date', '')}**")
                    
                    with col2:
                        st.markdown(f"### {event.get('title', '')}")
                        st.write(event.get('content', ''))
                
                st.markdown("---")