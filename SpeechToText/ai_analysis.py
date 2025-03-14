import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY not found in environment variables")

def _get_completion(prompt: str, max_tokens: int = 1000) -> str:
    """Helper function to get completion from Together.ai API"""
    try:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1.1,
            "stop": ["</s>", "[/INST]"]
        }
        
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"API returned status code {response.status_code}: {response.text}")
            
        result = response.json()
        if not result.get('choices') or not result['choices'][0].get('text'):
            raise Exception(f"Invalid API response format: {result}")
            
        return result['choices'][0]['text'].strip()
            
    except Exception as e:
        raise Exception(f"Together.ai API error: {str(e)}")

def analyze_brainstorming(text: str) -> Dict[str, Any]:
    """
    Analyze brainstorming session using Mixtral-8x7B.
    Returns insights in a conversational format.
    """
    try:
        prompt = f"""<s>[INST] You are an expert at analyzing document management systems and workflows.
        
Analyze the following feedback about our document management system and provide:
1. A concise summary of the main issues
2. Key patterns and recurring problems identified
3. Most critical issues that need immediate attention
4. Potential quick wins vs long-term improvements

Format your response in a clear, organized way that's easy to read.

Text to analyze:
{text} [/INST]"""

        analysis = _get_completion(prompt)
        return {
            'success': True,
            'analysis': analysis
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def generate_action_items(text: str) -> Dict[str, Any]:
    """
    Generate action items using Mixtral-8x7B.
    Returns a prioritized list of actions.
    """
    try:
        prompt = f"""<s>[INST] You are an expert at improving document management systems.
        
Review this feedback about our document system and create a prioritized action plan. Group actions into:
1. Quick Wins (This Week):
   - Focus on immediate user pain points
   - Simple UI/UX improvements
   - Quick bug fixes

2. Short-term Actions (This Month):
   - Performance improvements
   - Feature enhancements
   - Security updates

3. Long-term Projects (Beyond):
   - Major architectural changes
   - New feature development
   - Infrastructure upgrades

Format your response as a clear, actionable list with specific tasks and priorities.

Text to analyze:
{text} [/INST]"""

        action_items = _get_completion(prompt)
        return {
            'success': True,
            'action_items': action_items
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def suggest_improvements(text: str) -> Dict[str, Any]:
    """
    Generate improvement suggestions using Mixtral-8x7B.
    Returns detailed suggestions for enhancing the system.
    """
    try:
        prompt = f"""<s>[INST] You are an expert at improving document management and PDF handling systems.
        
Review this feedback and suggest improvements. Focus on:
1. User Experience
   - Interface improvements
   - Workflow optimization
   - Mobile responsiveness

2. Performance
   - Upload/download speeds
   - Processing efficiency
   - Resource usage

3. Features
   - Missing capabilities
   - Enhancement opportunities
   - Integration possibilities

4. Security & Compliance
   - Data protection
   - Access control
   - Audit trails

Format your response as specific, actionable suggestions with clear benefits.

Text to analyze:
{text} [/INST]"""

        suggestions = _get_completion(prompt)
        return {
            'success': True,
            'suggestions': suggestions
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def summarize_text(text: str) -> Dict[str, Any]:
    """
    Generate a concise summary using Mixtral-8x7B.
    Perfect for getting a quick overview of user feedback.
    """
    try:
        prompt = f"""<s>[INST] You are an expert at summarizing technical feedback about document management systems.
        
Summarize the following feedback, focusing on:
1. Core issues and pain points
2. Suggested improvements
3. User needs and preferences
4. Technical requirements

Keep the summary concise but include all critical points.

Text to summarize:
{text} [/INST]"""

        summary = _get_completion(prompt)
        return {
            'success': True,
            'summary': summary
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
