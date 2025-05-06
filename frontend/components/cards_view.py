import streamlit as st
import json
import pandas as pd

def render_cards(data):
    """
    Render cards visualization
    
    Args:
        data (dict): Cards data from API
    """
    st.subheader("Cards Visualization")
    
    cards = data.get("cards", [])
    
    # Handle empty data
    if not cards:
        st.info("No card data available. Try analyzing your idea again or select a different visualization.")
        st.caption("Cards display key aspects of your idea in an organized, searchable format.")
        return
    
    # Description
    st.markdown("""
    Cards break down your idea into key components that can be easily searched and filtered.
    Use the search and filter options below to focus on specific aspects of your analysis.
    """)
    
    # Search and filter layout
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
            "Business": ["business", "model", "revenue", "market", "competitor", "edge", "monetization", "pricing", "cost"],
            "Technical": ["tools", "technologies", "risks", "technical", "development", "platform", "architecture", "security"],
            "Planning": ["tasks", "roadmap", "strategy", "features", "timeline", "phase", "implementation", "launch"]
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
        if st.button("Clear filters", key="clear_filters_button"):
            st.session_state.card_search = ""
            st.session_state.card_filter = "All"
            st.rerun()
        return
    
    # Display cards in a grid (3 columns)
    cols = st.columns(3)
    
    for i, card in enumerate(filtered_cards):
        col_idx = i % 3
        
        with cols[col_idx]:
            # Create a card container
            with st.container():
                # Card header
                st.markdown(
                    f"<div class='card-header'>{card.get('emoji', '')} <span class='card-title'>{card.get('title', 'Card')}</span></div>", 
                    unsafe_allow_html=True
                )
                
                # Card content
                with st.expander("Show content", expanded=False):
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
    
    # Add export options
    with st.expander("Export Options"):
        # Create a dataframe from cards for CSV export
        cards_df = pd.DataFrame([
            {
                "Emoji": card.get("emoji", ""),
                "Title": card.get("title", ""),
                "Content": card.get("content", "").replace("\n", " ")
            }
            for card in cards
        ])
        
        # Download as CSV
        st.download_button(
            label="Download Cards (CSV)",
            data=cards_df.to_csv(index=False).encode('utf-8'),
            file_name="idea_cards.csv",
            mime="text/csv",
            key="download_cards_csv"
        )
        
        # Download as JSON
        json_str = json.dumps({"cards": cards}, indent=2)
        st.download_button(
            label="Download Cards (JSON)",
            data=json_str,
            file_name="idea_cards.json",
            mime="application/json",
            key="download_cards_json"
        )