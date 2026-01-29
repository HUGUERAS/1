import { useState } from 'react';
import './ImprovedProfileCard.css';

interface ProfileCardProps {
  icon: string;
  title: string;
  desc: string;
  onClick: () => void;
  gradient?: string;
}

export default function ImprovedProfileCard({ icon, title, desc, onClick, gradient }: ProfileCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  // Ícones SVG de alta qualidade
  const iconSVG: Record<string, JSX.Element> = {
    '📐': (
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
        <path d="M8 56L56 8L52 4L4 52L8 56Z" fill="url(#grad1)" />
        <path d="M12 52L52 12M16 48L48 16M20 44L44 20" stroke="currentColor" strokeWidth="2" />
        <defs>
          <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#667eea" />
            <stop offset="100%" stopColor="#764ba2" />
          </linearGradient>
        </defs>
      </svg>
    ),
    '🏠': (
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
        <path d="M32 8L8 28V56H24V40H40V56H56V28L32 8Z" fill="url(#grad2)" />
        <path d="M32 8L8 28M32 8L56 28" stroke="currentColor" strokeWidth="2" />
        <defs>
          <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#f093fb" />
            <stop offset="100%" stopColor="#f5576c" />
          </linearGradient>
        </defs>
      </svg>
    ),
    '🚜': (
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
        <circle cx="16" cy="48" r="8" fill="url(#grad3)" />
        <circle cx="48" cy="48" r="12" fill="url(#grad3)" />
        <path d="M8 36H32V24H40L48 32V36H56V44H52M12 44H24M40 44H36" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <rect x="32" y="28" width="8" height="8" rx="1" fill="currentColor" opacity="0.3" />
        <defs>
          <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#4facfe" />
            <stop offset="100%" stopColor="#00f2fe" />
          </linearGradient>
        </defs>
      </svg>
    )
  };

  return (
    <div
      className={`improved-card ${isHovered ? 'hovered' : ''}`}
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{ background: gradient || 'white' }}
    >
      {/* Glow effect */}
      <div className="card-glow"></div>
      
      {/* Icon with animation */}
      <div className="card-icon">
        {iconSVG[icon] || <span style={{ fontSize: '48px' }}>{icon}</span>}
      </div>

      {/* Content */}
      <h3 className="card-title">{title}</h3>
      <p className="card-desc">{desc}</p>

      {/* Arrow indicator */}
      <div className="card-arrow">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </div>
    </div>
  );
}
