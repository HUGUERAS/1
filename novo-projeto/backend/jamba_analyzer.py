"""
🧠 Jamba AI 2.1 Integration - Project Structure Analyzer
Modelo híbrido SSM-Transformer da AI21 Labs com 256K tokens de contexto
Especializado em análise e estruturação de projetos complexos

Autor: GitHub Copilot + Jamba AI 2.1
Data: 31/01/2026
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Type stubs for ai21 when not installed
class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

class AI21Client:
    def __init__(self, api_key: str):
        pass

try:
    from ai21 import AI21Client as _AI21Client
    from ai21.models.chat import ChatMessage as _ChatMessage
    AI21Client = _AI21Client
    ChatMessage = _ChatMessage
except ImportError:
    logging.debug("ai21 package not installed, using stubs")

# =====================================================
# CONFIGURAÇÃO
# =====================================================

AI21_API_KEY = os.getenv("AI21_API_KEY", "")
JAMBA_MODEL = "ai21/jamba-large-1.7"  # OpenRouter format

# =====================================================
# CLIENTE JAMBA
# =====================================================

class JambaStructureAnalyzer:
    """
    Analisador de estrutura de projeto usando Jamba AI 2.1
    
    Capacidades:
    - Análise de arquitetura completa (até 256K tokens)
    - Refatoração e sugestões de estrutura
    - Detecção de padrões e anti-patterns
    - Geração de documentação automática
    - Code review contextual
    """
    
    def __init__(self):
        if not AI21_API_KEY:
            raise ValueError("AI21_API_KEY é obrigatória. Configure a variável de ambiente.")
        self.client = AI21Client(api_key=AI21_API_KEY)
        
        self.model = JAMBA_MODEL
        self.max_tokens = 4096
        self.temperature = 0.3  # Baixa para respostas mais determinísticas
    
    def analyze_project_structure(
        self,
        project_files: List[Dict[str, str]],
        analysis_type: str = "architecture"
    ) -> Dict:
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
        
        Returns:
            Dict com análise completa e recomendações
        """
        
        # Construir contexto do projeto
        project_context = self._build_project_context(project_files)
        
        # Prompt específico por tipo
        system_prompt = self._get_system_prompt(analysis_type)
        
        try:
            messages = [
                ChatMessage(
                    role="system",
                    content=system_prompt
                ),
                ChatMessage(
                    role="user",
                    content=f"""Analise este projeto:

{project_context}

Forneça uma análise detalhada focada em: {analysis_type}"""
                )
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                "success": True,
                "analysis": response.choices[0].message.content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "analysis_type": analysis_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Jamba analysis error: {e}")
            return {
                "success": False,
                "error": str(e),
                "analysis": "Erro ao analisar projeto com Jamba."
            }
    
    def suggest_refactoring(
        self,
        component_code: str,
        component_type: str = "component"
    ) -> Dict:
        """
        Sugere refatoração para um componente específico
        
        Args:
            component_code: Código do componente
            component_type: Tipo (component, service, model, etc)
        
        Returns:
            Dict com sugestões de refatoração
        """
        
        prompt = f"""Como especialista em Clean Code e arquitetura, analise este {component_type}:

```
{component_code}
```

Forneça:
1. **Análise de Qualidade**: Problemas identificados
2. **Refatoração**: Código refatorado seguindo best practices
3. **Explicação**: O que foi melhorado e por quê
4. **Testes**: Sugestão de testes unitários
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    ChatMessage(role="user", content=prompt)
                ],
                max_tokens=self.max_tokens,
                temperature=0.3
            )
            
            return {
                "success": True,
                "refactoring": response.choices[0].message.content,
                "original_lines": len(component_code.splitlines()),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_architecture_diagram(
        self,
        project_structure: Dict
    ) -> Dict:
        """
        Gera diagrama de arquitetura em formato Mermaid
        
        Args:
            project_structure: Estrutura do projeto
        
        Returns:
            Dict com código Mermaid do diagrama
        """
        
        prompt = f"""Com base nesta estrutura de projeto, gere um diagrama Mermaid completo:

{json.dumps(project_structure, indent=2)}

O diagrama deve incluir:
- Arquitetura de alto nível (C4 Model - Context)
- Componentes principais
- Fluxo de dados
- Integrações externas

Retorne APENAS o código Mermaid válido, sem explicações."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    ChatMessage(role="user", content=prompt)
                ],
                max_tokens=2048,
                temperature=0.2
            )
            
            mermaid_code = response.choices[0].message.content
            
            # Extrair apenas código Mermaid
            if "```mermaid" in mermaid_code:
                mermaid_code = mermaid_code.split("```mermaid")[1].split("```")[0].strip()
            
            return {
                "success": True,
                "diagram": mermaid_code,
                "format": "mermaid",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def code_review(
        self,
        diff: str,
        context: Optional[str] = None
    ) -> Dict:
        """
        Code review automatizado de mudanças
        
        Args:
            diff: Git diff das mudanças
            context: Contexto adicional do PR
        
        Returns:
            Dict com review detalhado
        """
        
        prompt = f"""Como reviewer experiente, analise estas mudanças:

```diff
{diff}
```

{f'Contexto: {context}' if context else ''}

Forneça:
1. **Aprovação**: ✅ Aprovar | ⚠️ Aprovar com ressalvas | ❌ Rejeitar
2. **Problemas Críticos**: Issues que impedem merge
3. **Sugestões**: Melhorias opcionais
4. **Segurança**: Vulnerabilidades detectadas
5. **Testes**: Cobertura necessária
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    ChatMessage(role="user", content=prompt)
                ],
                max_tokens=3072,
                temperature=0.3
            )
            
            return {
                "success": True,
                "review": response.choices[0].message.content,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # =====================================================
    # HELPERS PRIVADOS
    # =====================================================
    
    def _build_project_context(self, files: List[Dict]) -> str:
        """Constrói contexto formatado do projeto"""
        context_parts = []
        
        for file in files[:50]:  # Limitar a 50 arquivos principais
            path = file.get("path", "unknown")
            content = file.get("content", "")
            
            # Truncar arquivos muito grandes
            if len(content) > 5000:
                content = content[:5000] + "\n... (truncado)"
            
            context_parts.append(f"""
## {path}
```
{content}
```
""")
        
        return "\n".join(context_parts)
    
    def _get_system_prompt(self, analysis_type: str) -> str:
        """Retorna system prompt específico por tipo de análise"""
        
        prompts = {
            "architecture": """Você é um arquiteto de software sênior especializado em:
- Clean Architecture
- Microservices
- Domain-Driven Design
- Design Patterns
- SOLID principles

Analise a arquitetura do projeto e forneça insights profundos sobre estrutura, padrões e oportunidades de melhoria.""",
            
            "refactor": """Você é um especialista em refatoração e Clean Code.
Identifique code smells, duplicações, complexidade excessiva e sugira refatorações concretas.""",
            
            "security": """Você é um especialista em segurança de aplicações.
Identifique vulnerabilidades, exposições de dados sensíveis, falhas de autenticação/autorização.""",
            
            "performance": """Você é um especialista em otimização de performance.
Identifique gargalos, consultas N+1, algoritmos ineficientes, problemas de memória.""",
            
            "documentation": """Você é um technical writer especializado em documentação de código.
Gere documentação clara, concisa e completa seguindo melhores práticas."""
        }
        
        return prompts.get(analysis_type, prompts["architecture"])
    
    def _mock_analysis(self, files: List[Dict], analysis_type: str) -> Dict:
        """Análise mock quando Jamba não está disponível"""
        return {
            "success": True,
            "analysis": f"""## Análise Mock ({analysis_type})

⚠️ **AI21 API Key não configurada**

Para habilitar análise com Jamba AI 2.1:
1. Obtenha API key em: https://studio.ai21.com/
2. Configure: AI21_API_KEY no Azure Functions
3. Reinicie a aplicação

**Arquivos analisados**: {len(files)}
**Modelo**: Jamba 1.5 Large (256K context)
""",
            "model": "mock",
            "analysis_type": analysis_type,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _mock_refactoring(self, code: str, component_type: str) -> Dict:
        """Refatoração mock"""
        return {
            "success": True,
            "refactoring": f"""## Refatoração Mock

Configure AI21_API_KEY para análise real com Jamba.

**Tipo**: {component_type}
**Linhas**: {len(code.splitlines())}
""",
            "timestamp": datetime.utcnow().isoformat()
        }


# =====================================================
# DUAL-MODEL STRATEGY
# =====================================================

class HybridAIService:
    """
    Serviço híbrido usando Phi-Silica (chat) + Jamba (estruturação)
    
    - Phi-Silica 3.6: Chat contextual, perguntas rápidas
    - Jamba AI 2.1: Análise profunda, refatoração, arquitetura
    """
    
    def __init__(self):
        self.jamba = JambaStructureAnalyzer()
        # Phi-Silica já existe em ai_assistant.py
    
    def analyze_and_chat(self, query: str, project_files: List[Dict] = None) -> Dict:
        """
        Decide qual modelo usar baseado no query
        
        Jamba para:
        - "analise a arquitetura"
        - "refatore este código"
        - "revise este PR"
        - "gere documentação"
        
        Phi-Silica para:
        - "como cadastrar?"
        - "o que é CAR?"
        - Chat rápido
        """
        
        query_lower = query.lower()
        
        # Keywords que ativam Jamba
        jamba_keywords = [
            "arquitetura", "estrutura", "refator", "review", 
            "analis", "otimiz", "melhori", "diagram", "documentaç"
        ]
        
        use_jamba = any(keyword in query_lower for keyword in jamba_keywords)
        
        if use_jamba and project_files:
            return {
                "model": "jamba-ai-2.1",
                "response": self.jamba.analyze_project_structure(project_files)
            }
        else:
            return {
                "model": "phi-silica-3.6",
                "response": "Use ai_assistant.py para chat contextual"
            }


# =====================================================
# EXEMPLO DE USO
# =====================================================

if __name__ == "__main__":
    analyzer = JambaStructureAnalyzer()
    
    # Exemplo: Analisar arquitetura
    files = [
        {"path": "backend/models.py", "content": "# código..."},
        {"path": "frontend/App.tsx", "content": "// código..."}
    ]
    
    result = analyzer.analyze_project_structure(files, "architecture")
    print(json.dumps(result, indent=2))
