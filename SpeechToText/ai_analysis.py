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
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1.1,
            "max_tokens": max_tokens
        }
        
        print(f"Making API request with data: {data}")  # Debug log
        
        response = requests.post(
            "https://api.together.ai/v1/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"API response status: {response.status_code}")  # Debug log
        print(f"API response text: {response.text}")  # Debug log
        
        if response.status_code != 200:
            raise Exception(f"API returned status code {response.status_code}: {response.text}")
            
        result = response.json()
        if not result.get('choices') or not result['choices'][0].get('text'):
            raise Exception(f"Invalid API response format: {result}")
            
        return result['choices'][0]['text'].strip()
            
    except Exception as e:
        print(f"API error: {str(e)}")  # Debug log
        raise Exception(f"Together.ai API error: {str(e)}")

def analyze_brainstorming(text: str) -> Dict[str, Any]:
    """
    Analyze transcribed text using Mixtral-8x7B.
    Returns insights in a conversational format.
    """
    try:
        prompt = f"""<s>[INST] Eres un asistente experto en análisis de texto. Por favor analiza este texto y proporciona:
1. Un resumen conciso
2. Ideas y conceptos principales discutidos
3. Puntos importantes que necesitan atención
4. Patrones o temas notables

Texto a analizar:
{text} [/INST]"""

        analysis = _get_completion(prompt)
        return {
            'success': True,
            'analysis': analysis
        }

    except Exception as e:
        print(f"Analysis error: {str(e)}")  # Debug log
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
        prompt = f"""<s>[INST] Eres un asistente experto en planificación. Revisa este texto y crea una lista priorizada de acciones. Enfócate en:
1. Acciones inmediatas (Alta prioridad)
2. Próximos pasos
3. Consideraciones futuras

Formatea tu respuesta como una lista clara y accionable.

Texto a analizar:
{text} [/INST]"""

        action_items = _get_completion(prompt)
        return {
            'success': True,
            'action_items': action_items
        }

    except Exception as e:
        print(f"Action items error: {str(e)}")  # Debug log
        return {
            'success': False,
            'error': str(e)
        }

def suggest_improvements(text: str) -> Dict[str, Any]:
    """
    Generate improvement suggestions using Mixtral-8x7B.
    Returns detailed suggestions for the discussed topics.
    """
    try:
        prompt = f"""<s>[INST] Eres un asistente experto en mejora continua. Revisa este texto y sugiere mejoras. Enfócate en:
1. Áreas de oportunidad
2. Posibles mejoras
3. Enfoques alternativos
4. Consideraciones adicionales

Formatea tu respuesta con sugerencias claras y accionables.

Texto a analizar:
{text} [/INST]"""

        suggestions = _get_completion(prompt)
        return {
            'success': True,
            'suggestions': suggestions
        }

    except Exception as e:
        print(f"Suggestions error: {str(e)}")  # Debug log
        return {
            'success': False,
            'error': str(e)
        }

def summarize_text(text: str) -> Dict[str, Any]:
    """
    Generate a concise summary using Mixtral-8x7B.
    Perfect for getting a quick overview of spoken content.
    """
    try:
        prompt = f"""<s>[INST] Eres un asistente experto en síntesis de información. Crea un resumen conciso del siguiente texto, enfocándote en:
1. Puntos principales discutidos
2. Conclusiones clave
3. Contexto importante
4. Detalles notables

Incluye todos los puntos críticos.

Texto a resumir:
{text} [/INST]"""

        summary = _get_completion(prompt)
        return {
            'success': True,
            'summary': summary
        }

    except Exception as e:
        print(f"Summary error: {str(e)}")  # Debug log
        return {
            'success': False,
            'error': str(e)
        }
