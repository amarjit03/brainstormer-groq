from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
import time
import logging
from llm_processor import LLMProcessor
from viz_utils import format_for_mindmap, format_for_cards, format_for_timeline
from templates import get_template, list_templates

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  

llm_processor = LLMProcessor()

# Create analysis endpoint
@app.route('/api/analyze', methods=['POST'])
def analyze_idea():
    """
    Analyze an idea using the LLM and return structured results with visualizations.
    """
    try:
        # Get request data
        data = request.json
        
        if not data or 'idea' not in data:
            return jsonify({"error": "Missing required 'idea' field"}), 400
        
        idea = data.get('idea')
        template_name = data.get('template', 'business_idea')
        formats = data.get('formats', ['mind_map'])
        
        # If formats is a string, convert to list
        if isinstance(formats, str):
            formats = [formats]
        
        # Get the template
        template = get_template(template_name)
        if not template:
            return jsonify({"error": f"Unknown template: {template_name}"}), 404
        
        # Track processing time
        start_time = time.time()
        
        # Process the idea
        logger.info(f"Analyzing idea using template: {template_name}")
        raw_analysis, structured_data = llm_processor.process_idea(idea, template)
        
        # Extract a title
        title = "Idea Analysis"
        for section_name in ["Project Title", "Title"]:
            if section_name in structured_data:
                content = structured_data[section_name]
                if isinstance(content, str):
                    title = content
                elif isinstance(content, dict) and "content" in content:
                    title = content["content"]
                elif isinstance(content, list) and len(content) > 0:
                    title = content[0]
        
        # Generate visualizations
        visualizations = {}
        
        if 'mind_map' in formats or 'all' in formats:
            visualizations['mindMap'] = format_for_mindmap(structured_data)
        
        if 'cards' in formats or 'all' in formats:
            visualizations['cards'] = format_for_cards(structured_data)
        
        if 'timeline' in formats or 'all' in formats:
            visualizations['timeline'] = format_for_timeline(structured_data)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(f"Analysis completed in {processing_time:.2f} seconds")
        
        # Create response
        response = {
            "title": title,
            "idea": idea,
            "rawAnalysis": raw_analysis,
            "structuredData": structured_data,
            "visualizations": visualizations,
            "processingTime": f"{processing_time:.2f} seconds"
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in analyze_idea: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to analyze idea", "message": str(e)}), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get the list of available templates."""
    try:
        templates = list_templates()
        return jsonify({"templates": templates})
    except Exception as e:
        logger.error(f"Error in get_templates: {str(e)}")
        return jsonify({"error": "Failed to get templates", "message": str(e)}), 500

@app.route('/api/visualize', methods=['POST'])
def visualize_content():
    """
    Generate visualization data from existing content.
    """
    try:
        data = request.json
        
        if not data or 'content' not in data:
            return jsonify({"error": "Missing required 'content' field"}), 400
        
        content = data.get('content')
        content_type = data.get('contentType', 'raw')
        visualization_type = data.get('type', 'mind_map')
        
        # Process the content
        if content_type == 'raw':
            # Parse the raw content
            _, structured_data = llm_processor.parse_response(content)
        else:
            # Use the provided structured data
            if isinstance(content, str):
                try:
                    structured_data = json.loads(content)
                except json.JSONDecodeError:
                    return jsonify({"error": "Invalid JSON in content field"}), 400
            else:
                structured_data = content
        
        # Generate the visualization
        visualization = None
        if visualization_type == 'mind_map':
            visualization = format_for_mindmap(structured_data)
        elif visualization_type == 'cards':
            visualization = format_for_cards(structured_data)
        elif visualization_type == 'timeline':
            visualization = format_for_timeline(structured_data)
        else:
            return jsonify({"error": f"Unknown visualization type: {visualization_type}"}), 400
        
        return jsonify({
            "type": visualization_type,
            "visualization": visualization
        })
    
    except Exception as e:
        logger.error(f"Error in visualize_content: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to visualize content", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Service is running"})

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get the current LLM settings."""
    return jsonify({
        "model": llm_processor.model_name,
        "temperature": llm_processor.temperature,
        "max_tokens": llm_processor.max_tokens
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)