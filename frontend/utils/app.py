import requests
import json
import streamlit as st

# API endpoint
BASE_URL = "http://localhost:5000/api"

def analyze_idea(idea, template_type, formats):
    """
    Send idea to backend for analysis
    
    Args:
        idea (str): The idea text
        template_type (str): Template type (business_idea, swot, etc.)
        formats (list): List of visualization formats to generate
        
    Returns:
        dict: Analysis results
    """
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={
                "idea": idea,
                "template": template_type,
                "formats": formats
            },
            timeout=120  # Longer timeout for analysis
        )
        
        if response.status_code != 200:
            error_msg = f"API error: {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg = error_data["error"]
            except:
                pass
            raise Exception(error_msg)
        
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Request error: {str(e)}")

def visualize_content(content, content_type, visualization_type):
    """
    Generate visualization for content
    
    Args:
        content (str): The content to visualize
        content_type (str): Type of content (raw or structured)
        visualization_type (str): Type of visualization to generate
        
    Returns:
        dict: Visualization data
    """
    try:
        response = requests.post(
            f"{BASE_URL}/visualize",
            json={
                "content": content,
                "contentType": content_type,
                "type": visualization_type
            }
        )
        
        if response.status_code != 200:
            error_msg = f"API error: {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg = error_data["error"]
            except:
                pass
            raise Exception(error_msg)
        
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Request error: {str(e)}")

def get_templates():
    """Get available templates"""
    try:
        response = requests.get(f"{BASE_URL}/templates")
        
        if response.status_code != 200:
            return {
                "business_idea": "Business Idea Analysis",
                "swot": "SWOT Analysis",
                "product_features": "Product Feature Analysis"
            }
        
        return response.json().get("templates", {})
    except:
        # Fallback templates if API fails
        return {
            "business_idea": "Business Idea Analysis",
            "swot": "SWOT Analysis",
            "product_features": "Product Feature Analysis"
        }