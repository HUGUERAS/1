"""
OpenRouter AI Integration Module

Provides secure API endpoint for calling OpenRouter models.
API key is kept secure on the backend (never exposed to frontend).
"""

import os
import json
import logging
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime

class OpenRouterClient:
    """Client for OpenRouter API calls"""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL = "ai21/jamba-large-1.7"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenRouter client
        
        Args:
            api_key: OpenRouter API key (defaults to env var OPENROUTER_API_KEY)
        """
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not configured")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ativo-real.azure",
            "X-Title": "Ativo Real - Land Management Platform",
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = DEFAULT_MODEL,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """
        Send chat completion request to OpenRouter
        
        Args:
            messages: List of messages with role and content
            model: Model to use (default: jamba-1.5-large)
            max_tokens: Maximum tokens in response
            temperature: Creativity parameter (0.0-2.0)
            top_p: Diversity via nucleus sampling
            stream: Whether to stream response
        
        Returns:
            API response dict with choices and usage
        
        Raises:
            requests.exceptions.RequestException: If API call fails
            ValueError: If response is invalid
        """
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
        }
        
        try:
            logging.info(f"Calling OpenRouter API with model: {model}")
            
            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logging.error("OpenRouter API request timed out")
            raise ValueError("OpenRouter API timeout")
        except requests.exceptions.ConnectionError:
            logging.error("Failed to connect to OpenRouter API")
            raise ValueError("OpenRouter API connection failed")
        except requests.exceptions.HTTPError as e:
            status_code = response.status_code
            error_msg = response.text if response.text else str(e)
            
            if status_code == 401:
                logging.error("OpenRouter authentication failed")
                raise ValueError("Invalid OpenRouter API key")
            elif status_code == 429:
                logging.warning("OpenRouter rate limited")
                raise ValueError("OpenRouter rate limited - try again later")
            else:
                logging.error(f"OpenRouter API error {status_code}: {error_msg}")
                raise ValueError(f"OpenRouter API error: {error_msg}")
    
    def analyze_topography(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Analyze topography-related prompt using Jamba model
        
        Args:
            prompt: User prompt about topography
            context: Additional context for analysis
        
        Returns:
            Analysis result as string
        """
        
        system_message = """Você é um especialista em topografia, geoprocessamento e gestão de terras.
Fornece análises detalhadas sobre propriedades rurais, características do terreno, 
potencial produtivo e conformidade ambiental. Seus dados são precisos e baseados em 
padrões SIRGAS 2000 (sistema geodésico brasileiro)."""
        
        messages = [
            {
                "role": "system",
                "content": system_message
            }
        ]
        
        if context:
            messages.append({
                "role": "user",
                "content": f"Contexto: {context}"
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.chat_completion(messages, model="ai21/jamba-large-1.7")
        
        if response.get("choices") and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise ValueError("Invalid response from OpenRouter")
    
    def generate_report(self, data: Dict[str, Any]) -> str:
        """
        Generate formatted report based on topography data
        
        Args:
            data: Topography data dictionary
        
        Returns:
            Formatted report as string
        """
        
        prompt = f"""Gere um relatório técnico profissional baseado nos seguintes dados de topografia:

{json.dumps(data, indent=2, ensure_ascii=False)}

O relatório deve incluir:
1. Resumo executivo
2. Características do terreno
3. Análise de potencial agrícola
4. Conformidade ambiental
5. Recomendações

Use formato Markdown com seções bem organizadas."""
        
        return self.analyze_topography(prompt)
    
    def validate_geometry_description(self, description: str) -> Dict[str, Any]:
        """
        Use AI to validate if a geometry description is valid
        
        Args:
            description: Text description of geometry
        
        Returns:
            Validation result with confidence and recommendations
        """
        
        prompt = f"""Analise a seguinte descrição de geometria/área rural:

"{description}"

Responda em JSON com:
{{
  "is_valid": boolean,
  "confidence": 0-1,
  "issues": ["lista", "de", "problemas"],
  "recommendations": ["lista", "de", "recomendações"],
  "geometric_type": "polygon|multipolygon|point|line"
}}"""
        
        response_text = self.analyze_topography(prompt)
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "is_valid": False,
                "confidence": 0.5,
                "issues": ["Could not parse AI response"],
                "recommendations": ["Please provide clearer geometry description"],
                "geometric_type": "unknown"
            }


# Utility functions for Azure Functions integration

def get_openrouter_client() -> OpenRouterClient:
    """Get initialized OpenRouter client"""
    return OpenRouterClient()


def handle_openrouter_error(error: Exception) -> tuple:
    """
    Handle OpenRouter errors and return HTTP response
    
    Args:
        error: Exception from OpenRouter
    
    Returns:
        Tuple of (status_code, error_dict)
    """
    
    error_msg = str(error)
    
    if "Invalid OpenRouter API key" in error_msg:
        return 401, {"error": "API key not configured or invalid"}
    elif "rate limited" in error_msg.lower():
        return 429, {"error": "Rate limited - please try again later"}
    elif "timeout" in error_msg.lower():
        return 504, {"error": "API request timed out"}
    else:
        return 500, {"error": "OpenRouter service error"}
