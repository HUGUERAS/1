# 🤖 Especificações Técnicas: Chatbot AI (Bem Real)

## 📋 Visão Geral
Assistente técnico inteligente para análise de dados topográficos e suporte aos workflows de GIS/CAD da plataforma Bem Real.

---

## 🎨 Design System

### Paleta de Cores
```css
/* Botão Flutuante (FAB) */
--bronze-fosco: #CD7F32;        /* Estado normal */
--azul-marinho: #001F3F;        /* Estado aberto */

/* Janela de Chat */
--bg-principal: rgba(0, 31, 63, 0.9);    /* Azul Marinho 90% opacidade */
--borda: #B0B0B0;                         /* Titânio Metálico */
--blur: blur(10px);                       /* Glassmorphism */

/* Mensagens */
--msg-usuario: linear-gradient(135deg, #CD7F32 0%, #B87333 100%); /* Bronze Gradient */
--msg-bot: rgba(176, 176, 176, 0.15);     /* Cinza Translúcido */
```

### Tipografia
```css
/* Interface Principal */
font-family: 'Inter', 'Roboto', sans-serif;
font-size: 14px;
line-height: 1.5;

/* Timestamp */
font-family: 'JetBrains Mono', 'Consolas', monospace;
font-size: 11px;
opacity: 0.7;
```

---

## 🔧 Componentes

### 1. Botão Flutuante (FAB)
**Especificações:**
- Dimensões: 56px × 56px
- Formato: Círculo perfeito
- Posição: `bottom: 24px; right: 24px;`
- Background: Bronze Fosco (#CD7F32)
- Shadow: `0 4px 12px rgba(0, 0, 0, 0.3)`
- Animação: Pulso sutil a cada 2 segundos

**Estados:**
```css
/* Normal */
background: #CD7F32;
animation: fabPulse 2s infinite;

/* Hover */
transform: scale(1.1);
box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);

/* Aberto */
background: #001F3F;
animation: none;
```

### 2. Janela de Chat
**Especificações:**
- Dimensões: 380px × 560px
- Posição: `bottom: 96px; right: 24px;`
- Background: `rgba(0, 31, 63, 0.9)`
- Borda: `1px solid #B0B0B0`
- Blur: `backdrop-filter: blur(10px)`
- Border Radius: 12px
- Shadow: `0 8px 32px rgba(0, 0, 0, 0.5)`

**Estrutura:**
```
┌──────────────────────────────────────┐
│ 🤖 Assistente Técnico   [🗑️] [✖️]   │ ← Header
├──────────────────────────────────────┤
│                                      │
│  🤖 Olá! Como posso ajudar?         │
│                            12:34     │
│                                      │
│     Qual é a área do lote?  🧑       │
│  12:35                               │
│                                      │
│  🤖 A área é 12.345,67 m²...        │
│                            12:35     │
│                                      │
│                                      │ ← Messages
│                                      │
│                                      │
├──────────────────────────────────────┤
│ [Digite sua pergunta técnica... ] 📤│ ← Input
└──────────────────────────────────────┘
```

### 3. Header (Cabeçalho)
**Elementos:**
- Logo AI Bot (24px)
- Título: "Assistente Técnico"
- Botão Limpar (🗑️ clear-chat)
- Botão Fechar (✖️ close-x)

**Estilo:**
```css
padding: 16px 20px;
border-bottom: 1px solid rgba(176, 176, 176, 0.3);
background: rgba(0, 31, 63, 0.95);
```

### 4. Mensagens
**Tipos:**

**a) Mensagem do Usuário:**
```css
background: linear-gradient(135deg, #CD7F32 0%, #B87333 100%);
color: #FFFFFF;
border-bottom-right-radius: 4px; /* Tail effect */
align-self: flex-end;
max-width: 75%;
```

**b) Mensagem do Bot:**
```css
background: rgba(176, 176, 176, 0.15);
border: 1px solid rgba(176, 176, 176, 0.3);
color: #FFFFFF;
border-bottom-left-radius: 4px; /* Tail effect */
align-self: flex-start;
max-width: 75%;
```

**c) Indicador de Digitação:**
```
🤖 ● ● ●  (animação bounce)
```

### 5. Input (Campo de Texto)
**Especificações:**
- Altura: 44px
- Placeholder: "Digite sua pergunta técnica..."
- Background: `rgba(0, 0, 0, 0.3)`
- Border: `1px solid rgba(176, 176, 176, 0.3)`
- Focus Border: `#CD7F32`

**Botão Enviar:**
```css
width: 44px;
height: 44px;
background: #CD7F32;
border-radius: 8px;
```
**Estados:**
- Disabled: `opacity: 0.5` quando input vazio
- Hover: `scale(1.05)` e `background: #B87333`

---

## 🎭 Interações

### 1. Abrir/Fechar Chat
```typescript
const [isOpen, setIsOpen] = useState(false);

<button onClick={() => setIsOpen(!isOpen)}>
  <AiBotIcon />
</button>
```

### 2. Enviar Mensagem
```typescript
const handleSendMessage = () => {
  if (!inputText.trim()) return;
  
  // Adiciona mensagem do usuário
  setMessages([...messages, { text: inputText, sender: 'user' }]);
  
  // Simula resposta do bot
  setTimeout(() => {
    setMessages([...messages, { text: botResponse, sender: 'bot' }]);
  }, 1500);
};
```

### 3. Limpar Histórico
```typescript
const handleClearChat = () => {
  if (confirm('Deseja limpar todo o histórico?')) {
    setMessages([initialMessage]);
  }
};
```

### 4. Enter para Enviar
```typescript
const handleKeyPress = (e: React.KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSendMessage();
  }
};
```

---

## 🧠 Lógica do Bot (Placeholder)

### Contextos Suportados
```typescript
const generateBotResponse = (userInput: string): string => {
  const input = userInput.toLowerCase();
  
  if (input.includes('área') || input.includes('perímetro')) {
    return 'Posso ajudar com cálculos de área...';
  }
  
  if (input.includes('coordenada')) {
    return 'Para editar coordenadas, use a ferramenta...';
  }
  
  if (input.includes('exportar')) {
    return 'Você pode exportar em PDF, KML ou GeoJSON...';
  }
  
  if (input.includes('sigef') || input.includes('sobreposição')) {
    return 'A verificação de sobreposições é automática...';
  }
  
  return 'Como posso ajudar com seus dados topográficos?';
};
```

### Integração Futura (AI Real)
```typescript
// Substituir por chamada à API de LLM
const response = await fetch('/api/ai/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userInput,
    context: {
      projectId: currentProject.id,
      currentTool: activeTool,
      recentActions: actionsHistory.slice(-5),
    },
  }),
});

const { reply } = await response.json();
```

---

## 📦 Ícones Criados

### 1. **ai-bot.svg** (32px) - Ícone Principal
```svg
<svg width="32" height="32" viewBox="0 0 32 32" fill="none">
  <rect x="6" y="10" width="20" height="14" rx="2" stroke="#CD7F32" stroke-width="2"/>
  <circle cx="11" cy="17" r="1.5" fill="#CD7F32"/>
  <circle cx="21" cy="17" r="1.5" fill="#CD7F32"/>
  <path d="M16 6V10" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M13 6H19" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M8 24V26C8 27.1046 8.89543 28 10 28H22C23.1046 28 24 27.1046 24 26V24" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

### 2. **clear-chat.svg** (24px) - Limpar Histórico
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M4 6H20M10 11V17M14 11V17M5 6L6 19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19L19 6M9 6V4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V6" stroke="#B0B0B0" stroke-width="2" stroke-linecap="round"/>
</svg>
```

### 3. **send-message.svg** (24px) - Enviar
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

### 4. **close-x.svg** (24px) - Fechar
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M18 6L6 18M6 6L18 18" stroke="#B0B0B0" stroke-width="2" stroke-linecap="round"/>
</svg>
```

---

## 🚀 Implementação

### 1. Adicionar ao App Principal
```tsx
// src/App.tsx
import { AIBotChat } from './components/AIBotChat';

function App() {
  return (
    <div className="app">
      {/* Outros componentes */}
      <AIBotChat />
    </div>
  );
}
```

### 2. Estrutura de Arquivos
```
src/
├── components/
│   ├── AIBotChat.tsx       (Componente principal)
│   └── AIBotChat.css       (Estilos completos)
├── assets/
│   └── icons/topography/
│       ├── 24px/
│       │   ├── clear-chat.svg
│       │   ├── send-message.svg
│       │   └── close-x.svg
│       └── 32px/
│           └── ai-bot.svg
```

---

## 📱 Responsividade

### Mobile (< 768px)
```css
.ai-bot-window {
  width: calc(100vw - 48px);
  height: calc(100vh - 120px);
}
```

### Small Mobile (< 480px)
```css
.ai-bot-fab {
  width: 48px;
  height: 48px;
  bottom: 16px;
  right: 16px;
}

.ai-bot-window {
  width: calc(100vw - 32px);
  height: calc(100vh - 104px);
}
```

---

## ✅ Checklist de Funcionalidades

### Implementado
- [x] Botão flutuante (FAB) com animação pulse
- [x] Janela de chat com glassmorphism
- [x] Mensagens do usuário e bot com tail effect
- [x] Indicador de digitação (typing)
- [x] Scroll automático para última mensagem
- [x] Enter para enviar, Shift+Enter para nova linha
- [x] Botão enviar desabilitado quando input vazio
- [x] Limpar histórico com confirmação
- [x] Timestamp em todas as mensagens
- [x] Responsividade mobile/tablet/desktop
- [x] 4 ícones técnicos (ai-bot, clear-chat, send-message, close-x)

### Próximos Passos (Integração AI)
- [ ] Integrar com API de LLM (OpenAI/Azure OpenAI)
- [ ] Contexto do projeto (ID, coordenadas, área)
- [ ] Contexto da ferramenta ativa (desenho, edição, medição)
- [ ] Histórico de ações do usuário (últimas 5)
- [ ] Sugestões automáticas (quick replies)
- [ ] Exportar conversa como TXT/PDF
- [ ] Comandos por voz (Speech-to-Text)
- [ ] Múltiplos idiomas (PT-BR, EN, ES)

---

## 🎯 Casos de Uso

### 1. Análise de Dados
**Usuário:** "Qual a área total do lote V1-V2-V3?"  
**Bot:** "A área do polígono é 12.345,67 m² (1,23 ha). Perímetro: 456,78 m."

### 2. Suporte de Ferramenta
**Usuário:** "Como edito coordenadas?"  
**Bot:** "Use a ferramenta 'Editar Vértices' (🔧) no mapa. Clique no vértice desejado e insira as novas coordenadas X, Y, Z."

### 3. Validação de Dados
**Usuário:** "Tem conflito com SIGEF?"  
**Bot:** "Verificação concluída: ✅ LIVRE. Não há sobreposições detectadas no SIGEF/INCRA."

### 4. Exportação
**Usuário:** "Como gero o relatório PDF?"  
**Bot:** "Vá em 'Relatório Técnico' → Botão 'Laudo Oficial (PDF)' no footer. O documento incluirá coordenadas, azimutes e análise de sobreposições."

---

## 🎨 Animações CSS

### 1. FAB Pulse
```css
@keyframes fabPulse {
  0%, 100% { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); }
  50% { box-shadow: 0 4px 12px rgba(205, 127, 50, 0.6); }
}
```

### 2. Janela Slide-In
```css
@keyframes windowSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
```

### 3. Mensagem Slide-In
```css
@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 4. Typing Bounce
```css
@keyframes typingBounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-8px); }
}
```

---

**Status:** ✅ Pronto para produção (aguardando integração AI)  
**Última atualização:** 22 de Janeiro de 2026
