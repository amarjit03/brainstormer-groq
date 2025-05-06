import streamlit as st
import pandas as pd

def render_cards(data):
    """
    Render cards visualization
    
    Args:
        data (dict): Cards data from API
    """
    st.subheader("Cards Visualization")
    
    cards = data.get("cards", [])
    
    if not cards:
        st.info("No card data available. Try analyzing your idea again or select a different visualization.")
        return
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Search cards", key="card_search")
    
    with col2:
        filter_options = ["All", "Business", "Technical", "Planning"]
        selected_filter = st.selectbox("Category", filter_options, key="card_filter")
    
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
        if st.button("Clear filters"):
            st.session_state.card_search = ""
            st.session_state.card_filter = "All"
            st.experimental_rerun()
        return
    
    # Display cards in a grid (3 columns)
    cols = st.columns(3)
    
    for i, card in enumerate(filtered_cards):
        col_idx = i % 3
        
        with cols[col_idx]:
            with st.expander(f"{card.get('emoji', '')} {card.get('title', 'Card')}", expanded=False):
                content = card.get("content", "")
                
                # Handle bullet points
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