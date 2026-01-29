import React, { useState, useEffect, useRef } from 'react';
import './AIChat.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface AIChatProps {
  context?: 'general' | 'rural' | 'urban';
}

export default function AIChat({ context = 'general' }: AIChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          context,
          conversationId
        })
      });

      const data = await response.json();

      if (data.success) {
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.message,
          timestamp: data.metadata.timestamp
        };

        setMessages(prev => [...prev, assistantMessage]);
        
        if (!conversationId) {
          setConversationId(data.conversationId);
        }
      } else {
        throw new Error(data.error || 'Failed to get response');
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Desculpe, ocorreu um erro. Por favor, tente novamente.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <>
      {/* Botão flutuante */}
      <button
        className="ai-chat-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Abrir chat"
      >
        💬
      </button>

      {/* Janela de chat */}
      {isOpen && (
        <div className="ai-chat-window">
          <div className="ai-chat-header">
            <h3>🤖 Assistente AI</h3>
            <div className="ai-chat-actions">
              <button onClick={clearChat} title="Limpar conversa">🔄</button>
              <button onClick={() => setIsOpen(false)} title="Fechar">✕</button>
            </div>
          </div>

          <div className="ai-chat-messages">
            {messages.length === 0 && (
              <div className="ai-chat-welcome">
                <p>👋 Olá! Sou seu assistente virtual.</p>
                <p>Como posso ajudar com o Ativo Real?</p>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`ai-chat-message ai-chat-message-${msg.role}`}>
                <div className="ai-chat-message-content">
                  <div className="ai-chat-message-avatar">
                    {msg.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="ai-chat-message-text">
                    {msg.content}
                  </div>
                </div>
                <div className="ai-chat-message-time">
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="ai-chat-message ai-chat-message-assistant">
                <div className="ai-chat-message-content">
                  <div className="ai-chat-message-avatar">🤖</div>
                  <div className="ai-chat-typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <form className="ai-chat-input" onSubmit={sendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Digite sua mensagem..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !input.trim()}>
              Enviar
            </button>
          </form>
        </div>
      )}
    </>
  );
}
