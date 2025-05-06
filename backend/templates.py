# Prompt templates for the LLM analysis

# Business idea analysis template
BUSINESS_IDEA_TEMPLATE = """
You are a business and product research analyst with expertise in market research, product development, and entrepreneurship.

Analyze the following idea thoroughly and provide a comprehensive analysis in the specified format:

IDEA: {idea}

Your analysis should be structured exactly as follows (include all emojis and section titles as shown):

🔍 1. **Project Title**
[Create a short, catchy name for this idea]

🎯 2. **Project Goals**
[Describe what the project aims to achieve in 2-3 sentences]

📋 3. **Key Tasks**
[List 5-7 actionable steps needed to build this project]

🧑‍🤝‍🧑 4. **Stakeholders**
[Identify 3-5 key stakeholders who would benefit from or be involved in this project]

⚠️ 5. **Risks**
[List 3-5 potential blockers or risks, both technical and market-based]

🛠️ 6. **Tools & Technologies**
[Recommend a technology stack that would be suitable for this project]

💡 7. **Innovations / Unique Value Props**
[Describe 2-3 elements that make this project different or better than alternatives]

💰 8. **Business Model**
[Suggest the most appropriate business model for this idea]

📊 9. **Market Opportunity**
[Analyze the potential market size, target users, and growth potential]

🧠 10. **Top Competitors**
[List 3-5 existing products or services that would compete with this idea]

🆚 11. **Competitive Edge**
[Explain why users would choose this product over competitors]

📈 12. **Revenue Streams**
[Suggest 2-4 ways this project could generate revenue]

📢 13. **Go-to-Market Strategy**
[Recommend an initial launch strategy, including target audiences and channels]

🌱 14. **Future Features / Roadmap**
[Suggest 3-5 features or developments that could be added after the initial launch]

Provide detailed, specific analysis for each section. Your analysis should be evidence-based and practical.
List items should be formatted with bullet points or dashes.
For sections like Key Tasks, Stakeholders, Risks, etc., use a bulleted list format.
"""

# SWOT analysis template
SWOT_ANALYSIS_TEMPLATE = """
You are a strategic business consultant with expertise in SWOT analysis.

Analyze the following idea or business and provide a detailed SWOT analysis in the specified format:

SUBJECT: {idea}

Your analysis should be structured exactly as follows:

💪 **Strengths**
[List and explain 4-6 internal strengths of the idea/business]

🔍 **Weaknesses**
[List and explain 4-6 internal weaknesses or limitations of the idea/business]

🚀 **Opportunities**
[List and explain 4-6 external opportunities that could benefit the idea/business]

⚠️ **Threats**
[List and explain 4-6 external threats or challenges that could harm the idea/business]

For each item in each section, include:
- A clear, concise title for the point
- A 1-2 sentence explanation
- If applicable, a brief suggestion on how to leverage (for strengths and opportunities) or address (for weaknesses and threats) this factor

Ensure your analysis is specific to the idea/business, evidence-based, and actionable.
Format each point as a bullet or numbered item for clarity.
"""

# Product feature analysis template
PRODUCT_FEATURE_TEMPLATE = """
You are a product manager with expertise in feature prioritization and development.

Analyze the following product idea and suggest key features in the specified format:

PRODUCT IDEA: {idea}

Your analysis should be structured exactly as follows:

🎯 **Core Value Proposition**
[Explain the main value this product provides to users in 2-3 sentences]

🧠 **Target User Personas**
[Describe 2-3 primary user personas who would use this product]

🔑 **Must-Have Features**
[List and explain 5-7 essential features that define the minimum viable product]

💎 **Nice-to-Have Features**
[List and explain 3-5 features that would enhance the product but aren't essential for launch]

🚫 **Anti-Features**
[List 2-4 features that might seem tempting but should be avoided, with reasoning]

⚙️ **Technical Considerations**
[Explain 3-4 key technical aspects to consider during development]

🔄 **Development Phases**
[Outline 3-4 logical phases for implementing these features]

📈 **Success Metrics**
[Suggest 4-6 metrics to measure the success of these features]

For each feature, include:
- A descriptive name
- A brief explanation of functionality
- The primary user need it addresses
- A rough complexity estimate (Low/Medium/High)

Format each feature as a bullet point with clear separation between elements.
"""

# Dictionary of all templates
_TEMPLATES = {
    "business_idea": BUSINESS_IDEA_TEMPLATE,
    "swot": SWOT_ANALYSIS_TEMPLATE,
    "product_features": PRODUCT_FEATURE_TEMPLATE
}

def get_template(template_name):
    """
    Get a template by name.
    
    Args:
        template_name (str): Name of the template
        
    Returns:
        str: The template text or None if not found
    """
    return _TEMPLATES.get(template_name)

def list_templates():
    """
    Get a list of available templates with descriptions.
    
    Returns:
        dict: Dictionary of template names and descriptions
    """
    return {
        "business_idea": "14-point business idea analysis",
        "swot": "SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)",
        "product_features": "Product feature analysis and prioritization"
    }

def add_template(name, template):
    """
    Add a new template or update an existing one.
    
    Args:
        name (str): Template name
        template (str): Template text
        
    Returns:
        bool: True if added, False if updated
    """
    is_new = name not in _TEMPLATES
    _TEMPLATES[name] = template
    return is_new