import random
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_for_mindmap(data):
    """
    Format data as a mind map visualization.
    
    Args:
        data (dict): Structured data with sections
        
    Returns:
        dict: Mind map data structure
    """
    mind_map = {
        "name": "Idea Analysis",
        "children": []
    }
    
    # Add each section as a child node
    for section_name, section_content in data.items():
        # Get emoji for the section
        if isinstance(section_content, dict) and "emoji" in section_content:
            emoji = section_content["emoji"]
            node_content = section_content.get("content", "")
        else:
            emoji = get_emoji_for_section(section_name)
            node_content = section_content
        
        # Create child nodes based on content type
        child_nodes = create_child_nodes(node_content)
        
        # Create section node
        section_node = {
            "name": f"{emoji} {section_name}",
            "children": child_nodes
        }
        
        mind_map["children"].append(section_node)
    
    return mind_map

def format_for_cards(data):
    """
    Format data as cards for display.
    
    Args:
        data (dict): Structured data with sections
        
    Returns:
        dict: Card layout data structure
    """
    cards = []
    
    # Get colors for the cards
    colors = generate_colors(len(data))
    
    for i, (section_name, section_content) in enumerate(data.items()):
        # Get emoji for the section
        if isinstance(section_content, dict) and "emoji" in section_content:
            emoji = section_content["emoji"]
            content = section_content.get("content", "")
        else:
            emoji = get_emoji_for_section(section_name)
            content = section_content
        
        # Format content based on type
        if isinstance(content, list):
            formatted_content = "\n".join([f"• {item}" for item in content])
        elif isinstance(content, dict):
            formatted_content = "\n".join([f"**{key}**: {value}" for key, value in content.items()])
        else:
            formatted_content = str(content)
        
        # Create card
        card = {
            "id": i + 1,
            "title": section_name,
            "emoji": emoji,
            "content": formatted_content,
            "color": colors[i]
        }
        
        cards.append(card)
    
    return {"cards": cards}

def format_for_timeline(data):
    """
    Format data as a timeline for display.
    
    Args:
        data (dict): Structured data with sections
        
    Returns:
        dict: Timeline data structure
    """
    # Find sections that might be sequential
    timeline_sections = []
    for section_name, section_content in data.items():
        # Check if section name suggests a phase or sequence
        if any(keyword in section_name.lower() for keyword in 
               ["phase", "step", "stage", "task", "milestone", "timeline", "roadmap"]):
            timeline_sections.append((section_name, section_content))
    
    # If no timeline sections found, look for "Key Tasks" or similar
    if not timeline_sections:
        for key_section in ["Key Tasks", "Tasks", "Steps", "Implementation"]:
            if key_section in data:
                timeline_sections = [(key_section, data[key_section])]
                break
    
    # If still no timeline sections, use all sections
    if not timeline_sections:
        # Skip some sections that don't make sense in a timeline
        timeline_sections = [(name, content) for name, content in data.items()
                           if not any(keyword in name.lower() for keyword in 
                                     ["competitor", "risk", "threat", "existing"])]
    
    # Create timeline events
    events = []
    for i, (section_name, section_content) in enumerate(timeline_sections):
        # Extract content based on structure
        if isinstance(section_content, dict) and "content" in section_content:
            content = section_content["content"]
            emoji = section_content.get("emoji", "📅")
        else:
            content = section_content
            emoji = get_emoji_for_section(section_name)
        
        # Format content based on type
        if isinstance(content, list):
            # For lists, create an event for each item
            for j, item in enumerate(content):
                events.append({
                    "id": len(events) + 1,
                    "title": f"{emoji} {section_name} - Step {j+1}",
                    "content": item,
                    "date": f"Phase {i+1}.{j+1}"
                })
        else:
            # For non-lists, create a single event
            events.append({
                "id": len(events) + 1,
                "title": f"{emoji} {section_name}",
                "content": str(content),
                "date": f"Phase {i+1}"
            })
    
    return {"events": events}

def create_child_nodes(content):
    """
    Create child nodes for mind map based on content type.
    
    Args:
        content: Content to transform into nodes
        
    Returns:
        list: List of child nodes
    """
    if isinstance(content, list):
        return [{"name": item} for item in content]
    elif isinstance(content, dict):
        return [{"name": f"{key}: {value}"} for key, value in content.items() if key != "emoji"]
    elif isinstance(content, str):
        # For text content, split into reasonable chunks if too long
        if len(content) > 100:
            chunks = split_text_into_chunks(content)
            return [{"name": chunk} for chunk in chunks]
        return [{"name": content}]
    else:
        return [{"name": "No content"}]

def get_emoji_for_section(section_name):
    """
    Get an appropriate emoji for a section based on its name.
    
    Args:
        section_name (str): The name of the section
        
    Returns:
        str: An emoji character
    """
    # Map common section names to emojis
    emoji_map = {
        "project title": "🔍",
        "title": "📝",
        "goal": "🎯",
        "goals": "🎯",
        "project goals": "🎯",
        "task": "📋",
        "tasks": "📋",
        "key tasks": "📋",
        "stakeholder": "🧑‍🤝‍🧑",
        "stakeholders": "🧑‍🤝‍🧑",
        "risk": "⚠️",
        "risks": "⚠️",
        "tool": "🛠️",
        "tools": "🛠️",
        "technologies": "🛠️",
        "tools & technologies": "🛠️",
        "innovation": "💡",
        "innovations": "💡",
        "value": "💡",
        "unique value": "💡",
        "business model": "💰",
        "market": "📊",
        "market opportunity": "📊",
        "competitor": "🧠",
        "competitors": "🧠",
        "top competitors": "🧠",
        "competitive edge": "🆚",
        "revenue": "📈",
        "revenue streams": "📈",
        "marketing": "📢",
        "go-to-market": "📢",
        "strategy": "📢",
        "feature": "🌱",
        "features": "🌱",
        "roadmap": "🌱",
        "future": "🌱"
    }
    
    # Try to find a matching emoji
    for key, emoji in emoji_map.items():
        if key.lower() in section_name.lower():
            return emoji
    
    # Generic emojis for random assignment
    generic_emojis = ["📌", "🔖", "📊", "📈", "📉", "📇", "📋", "📑", "📝", "📔", "📕", "📗", "📘", "📙"]
    return random.choice(generic_emojis)

def generate_colors(num_colors=10):
    """
    Generate a list of visually distinct colors.
    
    Args:
        num_colors (int): Number of colors to generate
        
    Returns:
        list: List of hex color codes
    """
    # Set of visually distinct colors
    base_colors = [
        "#4F46E5",  # Indigo
        "#10B981",  # Emerald
        "#F59E0B",  # Amber
        "#EC4899",  # Pink
        "#8B5CF6",  # Purple
        "#06B6D4",  # Cyan
        "#F97316",  # Orange
        "#14B8A6",  # Teal
        "#7C3AED",  # Violet
        "#EF4444",  # Red
        "#6366F1",  # Indigo
        "#2563EB",  # Blue
    ]
    
    # Return all base colors if we need fewer than or equal to what we have
    if num_colors <= len(base_colors):
        return base_colors[:num_colors]
    
    # Otherwise, generate additional colors
    results = base_colors.copy()
    
    while len(results) < num_colors:
        # Take a random color and modify it slightly
        base = random.choice(base_colors)
        # Convert hex to RGB
        r = int(base[1:3], 16)
        g = int(base[3:5], 16)
        b = int(base[5:7], 16)
        
        # Modify the color slightly
        r = max(0, min(255, r + random.randint(-20, 20)))
        g = max(0, min(255, g + random.randint(-20, 20)))
        b = max(0, min(255, b + random.randint(-20, 20)))
        
        # Convert back to hex
        new_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Add to results if it's not already there
        if new_color not in results:
            results.append(new_color)
    
    return results

def split_text_into_chunks(text, max_length=100):
    """
    Split long text into reasonably sized chunks.
    
    Args:
        text (str): Text to split
        max_length (int): Maximum length per chunk
        
    Returns:
        list: List of text chunks
    """
    # First try to split by newlines
    if "\n" in text:
        return [line.strip() for line in text.split("\n") if line.strip()]
    
    # If no newlines, try to split by sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # If sentences are still too long, break them down further
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks