import requests
import json
import streamlit as st
import time

# API endpoint
BASE_URL = "https://brainstormer-groq.onrender.com/api"

@st.cache_data(ttl=3600)
def get_templates():
    """
    Get available templates from the API
    
    Returns:
        dict: Dictionary of template types and names
    """
    try:
        response = requests.get(f"{BASE_URL}/templates", timeout=10)
        
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
    start_time = time.time()
    
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
        
        result = response.json()
        
        # Add processing time if not included
        if "processingTime" not in result:
            result["processingTime"] = round(time.time() - start_time, 2)
            
        return result
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
            },
            timeout=60
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

# For mocking sample data during development
def get_sample_analysis():
    """Get sample analysis data for development"""
    return {
        "title": "AI-Powered Health Monitoring App Analysis",
        "processingTime": 3.2,
        "rawAnalysis": "# AI-Powered Health Monitoring App Analysis\n\n🚀 **Overview**\nAn AI-powered health monitoring app that uses smartphone sensors and wearable device integration to track vital signs, activity levels, and sleep patterns. The app provides personalized health insights, early warning signs of potential health issues, and connects users with healthcare providers when necessary.\n\n💼 **Business Model**\n- Freemium model with basic health tracking features available for free\n- Premium subscription for advanced AI insights and predictions\n- B2B partnerships with healthcare providers and insurance companies\n- Data monetization (anonymized and with explicit user consent)\n\n👥 **Target Market**\n- Health-conscious individuals (25-65 years)\n- Patients with chronic conditions requiring regular monitoring\n- Elderly population and their caregivers\n- Fitness enthusiasts looking for comprehensive health data\n- Healthcare providers seeking remote patient monitoring solutions\n\n🔍 **Competitive Analysis**\n- Existing health apps focus primarily on fitness or specific health metrics\n- Few competitors offer comprehensive AI-driven health insights\n- Major differentiation through medical-grade accuracy and healthcare integration\n- Tech giants entering healthcare space pose significant competition\n\n🏗️ **Technical Requirements**\n- Machine learning algorithms for health data analysis and prediction\n- Secure cloud infrastructure for sensitive health data\n- Mobile app development (iOS and Android)\n- API integration with various wearable devices\n- HIPAA compliance and robust data security measures\n\n⚠️ **Risks and Challenges**\n- Regulatory approval for medical claims and features\n- Data privacy concerns and security requirements\n- Accuracy of health predictions and liability issues\n- User adoption and engagement challenges\n- Integration complexity with healthcare systems\n\n📈 **Growth Strategy**\n- Initial launch with core features to early adopters\n- Gradual expansion of AI capabilities and health insights\n- Strategic partnerships with healthcare providers\n- Geographic expansion with localized health recommendations\n- Additional features based on user feedback and market demands",
        "visualizations": {
            "mindMap": {
                "name": "AI-Powered Health App",
                "children": [
                    {
                        "name": "💼 Business Model",
                        "children": [
                            {"name": "Freemium Model"},
                            {"name": "Premium Subscription"},
                            {"name": "B2B Partnerships"},
                            {"name": "Data Monetization"}
                        ]
                    },
                    {
                        "name": "👥 Target Market",
                        "children": [
                            {"name": "Health-conscious Individuals"},
                            {"name": "Chronic Condition Patients"},
                            {"name": "Elderly Population"},
                            {"name": "Fitness Enthusiasts"},
                            {"name": "Healthcare Providers"}
                        ]
                    },
                    {
                        "name": "🏗️ Technical Req.",
                        "children": [
                            {"name": "ML Algorithms"},
                            {"name": "Secure Cloud Infrastructure"},
                            {"name": "Mobile App Development"},
                            {"name": "Wearable Integration"},
                            {"name": "HIPAA Compliance"}
                        ]
                    },
                    {
                        "name": "⚠️ Risks",
                        "children": [
                            {"name": "Regulatory Approval"},
                            {"name": "Data Privacy"},
                            {"name": "Prediction Accuracy"},
                            {"name": "User Adoption"},
                            {"name": "Integration Complexity"}
                        ]
                    }
                ]
            },
            "cards": {
                "cards": [
                    {
                        "emoji": "💼",
                        "title": "Revenue Streams",
                        "content": "• Freemium model with basic features free\n• Premium subscription ($9.99/month)\n• Healthcare provider partnerships\n• Insurance company data sharing\n• Enterprise solutions for remote monitoring"
                    },
                    {
                        "emoji": "🏆",
                        "title": "Competitive Edge",
                        "content": "• Medical-grade accuracy vs. consumer fitness apps\n• AI-driven predictive health insights\n• Integration with healthcare systems\n• Multi-device compatibility\n• Focus on actionable recommendations"
                    },
                    {
                        "emoji": "🔧",
                        "title": "Required Technologies",
                        "content": "• Machine learning for health data analysis\n• Secure cloud storage (HIPAA compliant)\n• Mobile app development\n• API integration with wearables\n• Data visualization tools"
                    },
                    {
                        "emoji": "📊",
                        "title": "Market Opportunity",
                        "content": "The global digital health market is projected to reach $380 billion by 2025, with health monitoring apps representing a $47 billion segment. Aging populations and rising healthcare costs are driving demand for preventative and remote monitoring solutions."
                    },
                    {
                        "emoji": "⚠️",
                        "title": "Key Challenges",
                        "content": "• Regulatory approval in multiple markets\n• Ensuring data privacy and security\n• Achieving medical-grade accuracy\n• Healthcare system integration\n• User retention and engagement"
                    },
                    {
                        "emoji": "📱",
                        "title": "Core Features",
                        "content": "• Vital signs monitoring\n• Sleep analysis\n• Activity tracking\n• Personalized health insights\n• Early warning detection\n• Healthcare provider connection\n• Medication reminders"
                    }
                ]
            },
            "timeline": {
                "events": [
                    {
                        "date": "Phase 1",
                        "title": "MVP Development",
                        "content": "Develop the minimum viable product with core functionality:\n• Basic health tracking features\n• Simple dashboard and visualizations\n• Initial AI algorithms for basic insights\n• Integration with popular wearables\n• HIPAA-compliant data storage"
                    },
                    {
                        "date": "Phase 2",
                        "title": "Beta Testing & Refinement",
                        "content": "• Launch beta version to limited user group\n• Collect user feedback and health data\n• Refine AI algorithms based on real-world data\n• Implement improvements to UI/UX\n• Begin partnership discussions with healthcare providers"
                    },
                    {
                        "date": "Phase 3",
                        "title": "Public Launch & Expansion",
                        "content": "• Full public release of the app\n• Implementation of premium subscription model\n• Launch marketing campaigns targeting key user segments\n• Expand wearable device compatibility\n• Begin integration with healthcare systems"
                    },
                    {
                        "date": "Phase 4",
                        "title": "Advanced Features & Partnerships",
                        "content": "• Roll out advanced AI predictive features\n• Secure partnerships with major healthcare providers\n• Explore insurance company partnerships\n• Expand to international markets\n• Develop specialized modules for chronic conditions"
                    },
                    {
                        "date": "Phase 5",
                        "title": "Ecosystem Development",
                        "content": "• Launch API for third-party developers\n• Develop virtual health assistant features\n• Explore telemedicine integration\n• Create community features for user support\n• Develop enterprise solutions for healthcare organizations"
                    }
                ]
            }
        }
    }