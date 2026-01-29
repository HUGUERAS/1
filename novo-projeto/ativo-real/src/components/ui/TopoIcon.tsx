import React from 'react';

/**
 * Componente para ícones topográficos BEM REAL
 * Suporta coloração dinâmica e controle de tamanho
 * 
 * @param Icon - Componente SVG importado via vite-plugin-svgr
 * @param size - Tamanho em pixels (16, 24, 32)
 * @param isActive - Estado ativo/inativo (bronze/cinza)
 * @param color - Cor customizada (sobrescreve isActive)
 * @param className - Classes CSS adicionais
 */

interface TopoIconProps {
  Icon: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  size?: 16 | 20 | 24 | 32;
  isActive?: boolean;
  disabled?: boolean;
  color?: string;
  className?: string;
  ariaLabel?: string;
}

const TopoIcon: React.FC<TopoIconProps> = ({
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

export default TopoIcon;
