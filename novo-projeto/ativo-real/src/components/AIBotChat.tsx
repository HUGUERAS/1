import React, { useState, useRef, useEffect } from 'react';
import './AIBotChat.css';
import TopoIcon from './ui/TopoIcon';
import AiBotIcon from '../assets/icons/topography/32px/ai-bot.svg?react';
import ClearChatIcon from '../assets/icons/topography/24px/clear-chat.svg?react';
import CloseXIcon from '../assets/icons/topography/24px/close-x.svg?react';
import SendMessageIcon from '../assets/icons/topography/24px/send-message.svg?react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export const AIBotChat: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Olá! Sou o assistente técnico da Bem Real. Como posso ajudar com análise de dados topográficos?',
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Simulate bot response (replace with actual API call)
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: generateBotResponse(inputText),
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleClearChat = () => {
    if (confirm('Deseja limpar todo o histórico de conversa?')) {
      setMessages([
        {
          id: '1',
          text: 'Histórico limpo. Como posso ajudar?',
          sender: 'bot',
          timestamp: new Date(),
        },
      ]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  };

  // Placeholder bot logic (replace with actual AI integration)
  const generateBotResponse = (userInput: string): string => {
    const input = userInput.toLowerCase();
    
    if (input.includes('área') || input.includes('perímetro')) {
      return 'Posso ajudar com cálculos de área e perímetro. Certifique-se de que o polígono está fechado e sincronizado no dashboard.';
    }
    
    if (input.includes('coordenada') || input.includes('vértice')) {
      return 'Para editar coordenadas, use a ferramenta "Editar Vértices" no mapa. Coordenadas devem estar em SIRGAS 2000 (EPSG:31983).';
    }
    
    if (input.includes('exportar') || input.includes('relatório')) {
      return 'Você pode exportar o projeto em PDF (laudo oficial), KML (Google Earth) ou GeoJSON usando os botões no relatório técnico.';
    }
    
    if (input.includes('sigef') || input.includes('incra') || input.includes('sobreposição')) {
      return 'A verificação de sobreposições com SIGEF/INCRA/CAR é feita automaticamente. Verifique o status na seção "Análise de Sobreposições" do relatório.';
    }
    
    return 'Entendido. Precisa de ajuda com coordenadas, cálculos de área, exportação de dados ou verificação de sobreposições? Estou aqui para auxiliar!';
  };

  return (
    <>
      {/* Floating Button */}
      <button
        className={`ai-bot-fab ${isOpen ? 'ai-bot-fab--open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Abrir assistente AI"
      >
        <TopoIcon Icon={AiBotIcon} size={32} color="#FFFFFF" />
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="ai-bot-window">
          {/* Header */}
          <div className="ai-bot-header">
            <div className="ai-bot-header-title">
              <TopoIcon Icon={AiBotIcon} size={24} color="#CD7F32" />
              <span>Assistente Técnico</span>
            </div>
            <div className="ai-bot-header-actions">
              <button
                className="ai-bot-header-btn"
                onClick={handleClearChat}
                aria-label="Limpar conversa"
              >
                <TopoIcon Icon={ClearChatIcon} size={20} />
              </button>
              <button
                className="ai-bot-header-btn"
                onClick={() => setIsOpen(false)}
                aria-label="Fechar chat"
              >
                <TopoIcon Icon={CloseXIcon} size={20} />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="ai-bot-messages">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`ai-bot-message ${msg.sender === 'user' ? 'ai-bot-message--user' : 'ai-bot-message--bot'}`}
              >
                <div className="ai-bot-message-content">
                  <p>{msg.text}</p>
                  <span className="ai-bot-message-time">{formatTime(msg.timestamp)}</span>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="ai-bot-message ai-bot-message--bot">
                <div className="ai-bot-message-content">
                  <div className="ai-bot-typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="ai-bot-input-container">
            <input
              ref={inputRef}
              type="text"
              className="ai-bot-input"
              placeholder="Digite sua pergunta técnica..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button
              className="ai-bot-send-btn"
              onClick={handleSendMessage}
              disabled={!inputText.trim()}
              aria-label="Enviar mensagem"
            >
              <TopoIcon Icon={SendMessageIcon} size={20} color="#FFFFFF" />
            </button>
          </div>
        </div>
      )}
    </>
  );
};
