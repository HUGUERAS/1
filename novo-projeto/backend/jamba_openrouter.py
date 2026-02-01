"""
🧠 Jamba AI 2.1 Integration via OpenRouter
Acesso unificado a múltiplos modelos de IA incluindo Jamba 1.7 Large

Autor: GitHub Copilot + OpenRouter SDK
Data: 31/01/2026
"""

import os
import json
from typing import Dict, List, Optional, AsyncIterator
from datetime import datetime
import logging
from enum import Enum

# Suporta tanto AI21 direto quanto OpenRouter
try:
    from openrouter import OpenRouter
    OPENROUTER_AVAILABLE = True
except ImportError:
    OPENROUTER_AVAILABLE = False
    logging.warning("OpenRouter SDK não instalado. Use: pip install openrouter-sdk")

try:
    from ai21 import AI21Client
    from ai21.models.chat import ChatMessage
    AI21_AVAILABLE = True
except ImportError:
    AI21_AVAILABLE = False
    logging.warning("AI21 SDK não instalado. Use: pip install ai21")

# =====================================================
# CONFIGURAÇÃO
# =====================================================

class AIProvider(str, Enum):
    OPENROUTER = "openrouter"  # Recomendado - acesso unificado
    AI21_DIRECT = "ai21"       # Direto na AI21

# Configuração via env vars
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
AI21_API_KEY = os.getenv("AI21_API_KEY", "")

# Selecionar provider automaticamente
if OPENROUTER_API_KEY and OPENROUTER_AVAILABLE:
    DEFAULT_PROVIDER = AIProvider.OPENROUTER
elif AI21_API_KEY and AI21_AVAILABLE:
    DEFAULT_PROVIDER = AIProvider.AI21_DIRECT
else:
    raise ValueError("⚠️ Nenhuma API key configurada. Configure OPENROUTER_API_KEY ou AI21_API_KEY.")

# Modelos disponíveis
JAMBA_MODELS = {
    "large": "ai21/jamba-large-1.7",      # 256K context, melhor qualidade
    "mini": "ai21/jamba-mini-1.5",        # 256K context, mais rápido
    "instruct": "ai21/jamba-1.5-instruct" # Fine-tuned para instruções
}

# =====================================================
# CLIENTE UNIFICADO
# =====================================================

class JambaClient:
    """
    Cliente unificado para Jamba AI via OpenRouter ou AI21 direto
    """
    
    def __init__(
        self, 
        provider: AIProvider = DEFAULT_PROVIDER,
        model: str = "large"
    ):
        self.provider = provider
        self.model_name = JAMBA_MODELS.get(model, JAMBA_MODELS["large"])
        self.client = None
        
        # Inicializar cliente baseado no provider
        if provider == AIProvider.OPENROUTER and OPENROUTER_AVAILABLE:
            self.client = OpenRouter(api_key=OPENROUTER_API_KEY)
        elif provider == AIProvider.AI21_DIRECT and AI21_AVAILABLE:
            self.client = AI21Client(api_key=AI21_API_KEY)
        
        self.max_tokens = 4096
        self.temperature = 0.3
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> Dict | AsyncIterator:
        """
        Envia mensagens para o modelo
        
        Args:
            messages: Lista de mensagens [{"role": "user", "content": "..."}]
            stream: Se True, retorna generator para streaming
        
        Returns:
            Dict com resposta ou AsyncIterator se stream=True
        """
        
        try:
            if self.provider == AIProvider.OPENROUTER:
                return await self._openrouter_completion(messages, stream)
            elif self.provider == AIProvider.AI21_DIRECT:
                return await self._ai21_completion(messages)
        except Exception as e:
            logging.error(f"Erro no chat completion: {e}")
            return {
                "success": False,
                "error": str(e),
                "content": "Erro ao processar requisição."
            }
    
    async def _openrouter_completion(
        self,
        messages: List[Dict],
        stream: bool = False
    ) -> Dict | AsyncIterator:
        """Completion via OpenRouter"""
        
        if stream:
            # Retornar generator para streaming
            return self._openrouter_stream(messages)
        
        # Non-streaming
        response = await self.client.chat.send(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return {
            "success": True,
            "content": response.choices[0].message.content,
            "model": self.model_name,
            "provider": "openrouter",
            "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _openrouter_stream(self, messages: List[Dict]) -> AsyncIterator[str]:
        """Stream de tokens do OpenRouter"""
        
        stream = await self.client.chat.send(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True
        )
        
        async for chunk in stream:
            content = chunk.choices[0]?.delta?.content
            if content:
                yield content
    
    async def _ai21_completion(self, messages: List[Dict]) -> Dict:
        """Completion via AI21 direto"""
        
        # Converter para formato AI21
        ai21_messages = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in messages
        ]
        
        response = self.client.chat.completions.create(
            model="jamba-1.5-large",
            messages=ai21_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return {
            "success": True,
            "content": response.choices[0].message.content,
            "model": "jamba-1.5-large",
            "provider": "ai21",
            "tokens_used": response.usage.total_tokens,
            "timestamp": datetime.utcnow().isoformat()
        }
    



# =====================================================
# ANALISADOR DE ESTRUTURA (REFATORADO)
# =====================================================

class JambaStructureAnalyzer:
    """
    Analisador de estrutura de projeto usando Jamba AI
    Agora com suporte a OpenRouter e streaming
    """
    
    def __init__(self, provider: AIProvider = DEFAULT_PROVIDER, model: str = "large"):
        self.client = JambaClient(provider=provider, model=model)
    
    async def analyze_project_structure(
        self,
        project_files: List[Dict[str, str]],
        analysis_type: str = "architecture",
        stream: bool = False
    ) -> Dict | AsyncIterator:
        """
        Analisa estrutura completa do projeto
        
        Args:
            project_files: Lista de arquivos [{path: str, content: str}]
            analysis_type: Tipo de análise
                - "architecture": Visão geral da arquitetura
                - "refactor": Sugestões de refatoração
                - "security": Análise de segurança
                - "performance": Otimizações de performance
                - "documentation": Geração de docs
            stream: Se True, retorna tokens em tempo real
        
        Returns:
            Dict com análise ou AsyncIterator se stream=True
        """
        
        # Construir contexto do projeto
        project_context = self._build_project_context(project_files)
        
        # Prompt específico
        system_prompt = self._get_system_prompt(analysis_type)
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""Analise este projeto em detalhes:

{project_context}

Foco da análise: {analysis_type}

Forneça:
1. Visão geral
2. Pontos fortes
3. Pontos fracos
4. Recomendações específicas
5. Priorização de ações
"""
            }
        ]
        
        return await self.client.chat_completion(messages, stream=stream)
    
    async def suggest_refactoring(
        self,
        component_code: str,
        component_type: str = "component",
        stream: bool = False
    ) -> Dict | AsyncIterator:
        """Sugere refatoração para um componente"""
        
        messages = [
            {
                "role": "system",
                "content": "Você é um especialista em Clean Code e refatoração."
            },
            {
                "role": "user",
                "content": f"""Refatore este {component_type}:

```
{component_code}
```

Forneça:
1. Análise do código atual
2. Código refatorado
3. Explicação das mudanças
4. Testes sugeridos
"""
            }
        ]
        
        return await self.client.chat_completion(messages, stream=stream)
    
    async def code_review(
        self,
        diff: str,
        context: Optional[str] = None,
        stream: bool = False
    ) -> Dict | AsyncIterator:
        """Code review de mudanças"""
        
        messages = [
            {
                "role": "system",
                "content": "Você é um code reviewer experiente."
            },
            {
                "role": "user",
                "content": f"""Revise estas mudanças:

```diff
{diff}
```

{f'Contexto: {context}' if context else ''}

Forneça:
1. Aprovação (✅/⚠️/❌)
2. Problemas críticos
3. Sugestões
4. Segurança
5. Cobertura de testes necessária
"""
            }
        ]
        
        return await self.client.chat_completion(messages, stream=stream)
    
    async def generate_architecture_diagram(
        self,
        project_structure: Dict
    ) -> Dict:
        """Gera diagrama Mermaid da arquitetura"""
        
        messages = [
            {
                "role": "user",
                "content": f"""Gere um diagrama Mermaid desta arquitetura:

{json.dumps(project_structure, indent=2)}

Retorne APENAS código Mermaid válido."""
            }
        ]
        
        result = await self.client.chat_completion(messages, stream=False)
        
        if result.get("success"):
            mermaid_code = result["content"]
            
            # Extrair código Mermaid
            if "```mermaid" in mermaid_code:
                mermaid_code = mermaid_code.split("```mermaid")[1].split("```")[0].strip()
            
            return {
                "success": True,
                "diagram": mermaid_code,
                "format": "mermaid"
            }
        
        return result
    
    # =====================================================
    # HELPERS
    # =====================================================
    
    def _build_project_context(self, files: List[Dict]) -> str:
        """Constrói contexto formatado do projeto"""
        context_parts = []
        
        for file in files[:50]:  # Limitar a 50 arquivos
            path = file.get("path", "unknown")
            content = file.get("content", "")
            
            # Truncar arquivos grandes
            if len(content) > 5000:
                content = content[:5000] + "\n... (truncado)"
            
            context_parts.append(f"## {path}\n```\n{content}\n```\n")
        
        return "\n".join(context_parts)
    
    def _get_system_prompt(self, analysis_type: str) -> str:
        """System prompt específico por tipo"""
        
        prompts = {
            "architecture": """Você é um arquiteto de software sênior especializado em:
- Clean Architecture
- Microservices
- Domain-Driven Design
- Design Patterns
- SOLID principles

Analise a arquitetura e forneça insights profundos.""",
            
            "refactor": """Você é um especialista em refatoração e Clean Code.
Identifique code smells, duplicações, complexidade excessiva.""",
            
            "security": """Você é um especialista em segurança de aplicações.
Identifique vulnerabilidades, exposições de dados, falhas de auth.""",
            
            "performance": """Você é um especialista em otimização.
Identifique gargalos, N+1 queries, algoritmos ineficientes.""",
            
            "documentation": """Você é um technical writer.
Gere documentação clara e completa."""
        }
        
        return prompts.get(analysis_type, prompts["architecture"])


# =====================================================
# EXEMPLO DE USO
# =====================================================

async def example_usage():
    """Exemplo de uso do cliente Jamba"""
    
    analyzer = JambaStructureAnalyzer(
        provider=AIProvider.OPENROUTER,
        model="large"
    )
    
    # Exemplo 1: Análise sem streaming
    print("=" * 60)
    print("📊 ANÁLISE DE ARQUITETURA (Non-streaming)")
    print("=" * 60)
    
    files = [
        {
            "path": "backend/models.py",
            "content": "class User:\n    def __init__(self, name):\n        self.name = name"
        }
    ]
    
    result = await analyzer.analyze_project_structure(files, "architecture", stream=False)
    
    if result.get("success"):
        print(f"\n✅ Análise concluída!")
        print(f"Provider: {result.get('provider')}")
        print(f"Model: {result.get('model')}")
        print(f"Tokens: {result.get('tokens_used')}")
        print(f"\n{result['content']}")
    
    # Exemplo 2: Análise com streaming
    print("\n" + "=" * 60)
    print("🌊 ANÁLISE COM STREAMING")
    print("=" * 60 + "\n")
    
    stream = await analyzer.analyze_project_structure(files, "refactor", stream=True)
    
    async for chunk in stream:
        print(chunk, end="", flush=True)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
