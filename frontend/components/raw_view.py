import streamlit as st
import re

def render_raw_analysis(raw_text):
    """
    Render the raw analysis text with parsing and formatting
    
    Args:
        raw_text (str): Raw analysis text
    """
    st.subheader("Raw Analysis")
    
    if not raw_text:
        st.info("No analysis data available.")
        return
    
    # Description
    st.markdown("""
    This is the complete text analysis of your idea. You can read the entire analysis,
    search for specific content, or download it for later reference.
    """)
    
    # Add search functionality
    search_term = st.text_input("Search analysis", key="raw_search")
    
    # Process and display the raw text
    if search_term:
        # Highlight the search term
        highlighted_text = highlight_search_term(raw_text, search_term)
        st.markdown(highlighted_text, unsafe_allow_html=True)
        
        # Show occurrences
        occurrences = len(re.findall(re.escape(search_term), raw_text, re.IGNORECASE))
        st.caption(f"Found {occurrences} occurrences of '{search_term}'")
    else:
        # Show the raw text in a markdown area
        st.markdown(raw_text)
    
    # Extract sections for structured navigation
    sections = parse_raw_analysis(raw_text)
    
    if sections:
        with st.expander("Jump to section", expanded=False):
            for i, section in enumerate(sections):
                if st.button(f"{section['emoji']} {section['title']}", key=f"section_{i}"):
                    # Create an anchor for the section
                    section_id = section['title'].lower().replace(' ', '-')
                    st.markdown(f"<div id='{section_id}'></div>", unsafe_allow_html=True)
                    
                    # Scroll to the section
                    st.markdown(f"""
                    <script>
                        document.getElementById('{section_id}').scrollIntoView();
                    </script>
                    """, unsafe_allow_html=True)
    
    # Download options
    st.download_button(
        label="Download Raw Analysis",
        data=raw_text,
        file_name="idea_analysis.md",
        mime="text/markdown",
        key="download_raw"
    )

def parse_raw_analysis(raw_text):
    """
    Parse raw analysis text into sections with emoji and content
    
    Args:
        raw_text (str): Raw analysis text
        
    Returns:
        list: List of section dictionaries
    """
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

def highlight_search_term(text, search_term):
    """
    Highlight occurrences of search term in text
    
    Args:
        text (str): Text to search in
        search_term (str): Term to highlight
        
    Returns:
        str: HTML with highlighted search terms
    """
    if not search_term:
        return text
    
    # Escape the search term for regex
    escaped_term = re.escape(search_term)
    
    # Replace occurrences with highlighted version
    highlighted = re.sub(
        f'({escaped_term})', 
        r'<span style="background-color: #FFFF00; font-weight: bold;">\1</span>', 
        text, 
        flags=re.IGNORECASE
    )
    
    return highlighted