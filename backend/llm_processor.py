from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import logging
import re
import json
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMProcessor:
    """Class to handle LLM interactions and response processing."""
    
    def __init__(self):
        """Initialize the LLM processor."""
        self.api_key = os.getenv('GROQ_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'llama3-70b-8192')
        self.temperature = float(os.getenv('TEMPERATURE', 0.7))
        self.max_tokens = int(os.getenv('MAX_TOKENS', 4096))
        
        # Check if API key is available
        if not self.api_key:
            logger.warning("No GROQ_API_KEY found in environment variables. LLM functionality will not work.")
            
        # Initialize LLM
        self._init_llm()
        
        # Simple response cache
        self.cache = {}
        self.cache_enabled = os.getenv('ENABLE_CACHE', 'True').lower() in ('true', '1', 't')
        self.cache_timeout = 3600  # 1 hour
    
    def _init_llm(self):
        """Initialize the LLM with current settings."""
        try:
            self.llm = ChatGroq(
                api_key=self.api_key,
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            logger.info(f"LLM initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise
    
    def process_idea(self, idea, template):
        """
        Process an idea using the specified template.
        
        Args:
            idea (str): The idea to analyze
            template (str): The template to use
            
        Returns:
            tuple: (raw_analysis, structured_data)
        """
        # Check cache first
        cache_key = (idea, template)
        if self.cache_enabled and cache_key in self.cache:
            timestamp, raw_analysis, structured_data = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                logger.info("Using cached analysis")
                return raw_analysis, structured_data
        
        # Create the prompt
        prompt = PromptTemplate(
            template=template,
            input_variables=["idea"]
        )
        
        # Create the chain
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            # Run the chain
            logger.info("Requesting LLM analysis...")
            raw_analysis = chain.run(idea=idea)
            
            # Parse the response
            logger.info("Parsing LLM response...")
            raw_analysis, structured_data = self.parse_response(raw_analysis)
            
            # Update cache
            if self.cache_enabled:
                self.cache[cache_key] = (time.time(), raw_analysis, structured_data)
            
            return raw_analysis, structured_data
            
        except Exception as e:
            logger.error(f"Error in process_idea: {str(e)}")
            raise
    
    def parse_response(self, raw_content):
        """
        Parse the raw LLM response into structured data.
        
        Args:
            raw_content (str): The raw LLM response
            
        Returns:
            tuple: (cleaned_content, structured_data)
        """
        # Try parsing as JSON first
        try:
            return raw_content, json.loads(raw_content)
        except json.JSONDecodeError:
            pass
        
        # Handle content with emoji section markers
        structured_data = self._extract_sections(raw_content)
        
        return raw_content, structured_data
    
    def _extract_sections(self, content):
        """
        Extract sections from the content based on headers.
        
        Args:
            content (str): The content to parse
            
        Returns:
            dict: Extracted sections
        """
        # Handle emoji section headers
        emoji_pattern = r'([\u2600-\u27BF\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]).*?\*\*(.*?)\*\*'
        section_pattern = r'(\d+)\.\s+\*\*(.*?)\*\*'
        
        sections = {}
        current_section = None
        current_content = []
        
        # Process line by line
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check for emoji section headers
            emoji_match = re.search(emoji_pattern, line)
            if emoji_match:
                emoji, section_name = emoji_match.groups()
                if current_section and current_content:
                    sections[current_section] = self._process_section_content('\n'.join(current_content))
                    current_content = []
                
                current_section = section_name.strip()
                sections[current_section] = {"emoji": emoji}
                continue
                
            # Check for numbered section headers
            section_match = re.search(section_pattern, line)
            if section_match:
                if current_section and current_content:
                    if isinstance(sections[current_section], dict):
                        sections[current_section]["content"] = self._process_section_content('\n'.join(current_content))
                    else:
                        sections[current_section] = self._process_section_content('\n'.join(current_content))
                    current_content = []
                
                current_section = section_match.group(2).strip()
                sections[current_section] = {}
                continue
            
            # If not a header, add content to current section
            if current_section:
                current_content.append(line)
        
        # Don't forget the last section
        if current_section and current_content:
            if isinstance(sections[current_section], dict):
                sections[current_section]["content"] = self._process_section_content('\n'.join(current_content))
            else:
                sections[current_section] = self._process_section_content('\n'.join(current_content))
        
        return sections
    
    def _process_section_content(self, content):
        """
        Process the content of a section to extract structured data.
        
        Args:
            content (str): The content of a section
            
        Returns:
            str or list or dict: Processed content
        """
        # Check if content is a list
        if re.search(r'^\s*[-*•]\s', content, re.MULTILINE):
            items = []
            for line in content.split('\n'):
                line = line.strip()
                if re.match(r'^\s*[-*•]\s', line):
                    items.append(line.split(maxsplit=1)[1] if len(line.split(maxsplit=1)) > 1 else "")
            return items
        
        # Check if content has key-value pairs
        if ': ' in content and '\n' in content:
            pairs = {}
            for line in content.split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    pairs[key.strip()] = value.strip()
            if pairs:
                return pairs
        
        # Otherwise return as plain text
        return content.strip()