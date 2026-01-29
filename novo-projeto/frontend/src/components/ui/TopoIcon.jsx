import React from 'react';
import './TopoIcon.css';

/**
 * Componente para ícones topográficos BEM REAL
 * Suporta coloração dinâmica e controle de tamanho
 * 
 * @param Icon - Componente SVG (Lucide ou similar)
 * @param size - Tamanho em pixels (default 24)
 * @param isActive - Estado ativo/inativo (bronze/cinza)
 * @param disabled - Estado desabilitado
 * @param color - Cor customizada (sobrescreve isActive)
 * @param className - Classes CSS adicionais
 */
export const TopoIcon = ({
  Icon,
  size = 24,
  isActive = true,
  disabled = false,
  color,
  className = '',
  ariaLabel,
}) => {
  // Cores do Design System BEM REAL
  const BRONZE_ACTIVE = '#CD7F32';   // Bronze Fosco - Ativo
  const GRAY_INACTIVE = '#A0A0A0';    // Cinza - Inativo
  const DARK_DISABLED = '#4A4A4A';    // Cinza Escuro - Desabilitado

  const getIconColor = () => {
    if (color) return color;
    if (disabled) return DARK_DISABLED;
    return isActive ? BRONZE_ACTIVE : GRAY_INACTIVE;
  };

  const iconColor = getIconColor();

  if (!Icon) return null;

  return (
    <Icon
      width={size}
      height={size}
      style={{
        stroke: iconColor,
        fill: 'none',
        transition: 'stroke 0.2s ease-in-out',
        marginRight: '8px',
        verticalAlign: 'middle',
        opacity: disabled ? 0.5 : 1,
        cursor: disabled ? 'not-allowed' : 'inherit',
      }}
      className={`topo-icon ${className} ${disabled ? 'disabled' : ''}`}
      aria-label={ariaLabel}
      aria-disabled={disabled}
      role="img"
    />
  );
};

// export default TopoIcon;
