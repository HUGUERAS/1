"""
AI Assistant Endpoint
Integração com modelo Phi-Silica fine-tuned
"""

import os
import logging
import json
from typing import List, Dict
import requests
from datetime import datetime

# ========================================
# Configuração do Modelo
# ========================================
MODEL_ENDPOINT = os.environ.get("PHI_SILICA_ENDPOINT", "")
MODEL_API_KEY = os.environ.get("PHI_SILICA_API_KEY", "")

# Sistema de prompts
SYSTEM_PROMPTS = {
    "general": """Você é um assistente especializado em gestão de ativos rurais e urbanos.
Você ajuda usuários com:
- Cadastro de propriedades rurais e urbanas
- Informações sobre documentação necessária (CAR, CCIR)
- Questões sobre áreas, geolocalização e mapas
- Suporte técnico da plataforma Ativo Real

Seja conciso, objetivo e educado.""",
    
    "rural": """Especialista em propriedades rurais. Conhecimento sobre:
- CAR (Cadastro Ambiental Rural)
- CCIR (Certificado de Cadastro de Imóvel Rural)
- Áreas produtivas e de preservação
- Georreferenciamento""",
    
    "urban": """Especialista em propriedades urbanas. Conhecimento sobre:
- Cadastro de lotes e terrenos
- Ativação de contas
- Gestão de usuários"""
}

class AIAssistant:
    """Cliente para o modelo Phi-Silica fine-tuned"""
    
    def __init__(self):
        self.endpoint = MODEL_ENDPOINT
        self.api_key = MODEL_API_KEY
        self.max_tokens = 512
        self.temperature = 0.7
    
    def generate_response(
        self,
        user_message: str,
        context_type: str = "general",
        conversation_history: List[Dict] = None
    ) -> Dict:
        """
        Gera resposta do modelo
        
        Args:
            user_message: Pergunta do usuário
            context_type: Tipo de contexto (general, rural, urban)
            conversation_history: Histórico de mensagens anteriores
        
        Returns:
            Dict com resposta e metadados
        """
        
        # Construir mensagens
        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS.get(context_type, SYSTEM_PROMPTS["general"])}
        ]
        
        # Adicionar histórico
        if conversation_history:
            messages.extend(conversation_history[-5:])  # Últimas 5 mensagens
        
        # Adicionar mensagem atual
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Chamar modelo (Azure OpenAI ou GitHub Models)
            if self.endpoint:
                response = self._call_hosted_model(messages)
            else:
                # Fallback: resposta mock
                response = self._mock_response(user_message, context_type)
            
            return {
                "success": True,
                "response": response["content"],
                "tokens_used": response.get("tokens", 0),
                "model": response.get("model", "phi-silica-3.6-finetuned"),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"AI generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "Desculpe, não consegui processar sua pergunta no momento."
            }
    
    def _call_hosted_model(self, messages: List[Dict]) -> Dict:
        """Chama modelo hospedado (Azure/GitHub)"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        response = requests.post(
            f"{self.endpoint}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "content": data["choices"][0]["message"]["content"],
            "tokens": data["usage"]["total_tokens"],
            "model": data["model"]
        }
    
    def _mock_response(self, message: str, context: str) -> Dict:
        """Resposta mock para testes sem modelo"""
        message_lower = message.lower()
        
        # Respostas baseadas em keywords
        if any(word in message_lower for word in ["cadastrar", "cadastro", "registrar"]):
            if context == "rural":
                response = """Para cadastrar uma propriedade rural:

1. Acesse o menu "Cadastro Rural"
2. Preencha os dados:
   - Nome da fazenda
   - Documento (CAR/CCIR)
   - Área em hectares
   - Coordenadas (opcional)
3. Informe dados do administrador
4. Clique em "Cadastrar"

Você receberá um ID único da propriedade."""
            else:
                response = """Para cadastrar um imóvel urbano:

1. Acesse "Cadastro Urbano"
2. Informe CPF e data de nascimento
3. Defina uma senha
4. Confirme o cadastro

Você receberá um link de ativação por email."""
        
        elif any(word in message_lower for word in ["car", "ccir", "documento"]):
            response = """Documentos rurais:

**CAR** (Cadastro Ambiental Rural):
- Obrigatório para propriedades rurais
- Registro ambiental no SICAR
- Contém informações de preservação

**CCIR** (Certificado de Cadastro de Imóvel Rural):
- Emitido pelo INCRA
- Necessário para transações
- Validade de 1 ano"""
        
        elif any(word in message_lower for word in ["mapa", "localização", "coordenadas"]):
            response = """Sobre mapas e localização:

- Você pode visualizar propriedades no mapa interativo
- Clique em "Visualizar Mapa" no menu
- Use filtros por tipo (rural/urbano)
- Propriedades aparecem como marcadores ou polígonos
- Clique em um marcador para ver detalhes"""
        
        elif any(word in message_lower for word in ["ajuda", "help", "suporte"]):
            response = """Como posso ajudar?

Posso responder sobre:
• Cadastro de propriedades rurais e urbanas
• Documentação necessária (CAR, CCIR)
• Uso do mapa interativo
• Ativação de contas
• Problemas técnicos

Faça sua pergunta!"""
        
        else:
            response = f"""Recebi sua mensagem: "{message}"

Posso ajudar com informações sobre cadastro de propriedades, documentação rural (CAR/CCIR) e uso da plataforma.

O que você gostaria de saber especificamente?"""
        
        return {
            "content": response,
            "tokens": len(response.split()),
            "model": "mock-assistant"
        }

# Singleton instance
_assistant_instance = None

def get_ai_assistant() -> AIAssistant:
    """Retorna instância singleton do assistente"""
    global _assistant_instance
    if _assistant_instance is None:
        _assistant_instance = AIAssistant()
    return _assistant_instance
