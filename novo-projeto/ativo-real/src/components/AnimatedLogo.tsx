import { useState, useEffect } from 'react';
import './AnimatedLogo.css';

interface AnimatedLogoProps {
  size?: number;
  autoPlay?: boolean;
  loop?: boolean;
}

export const AnimatedLogo = ({ size = 320, autoPlay = true, loop = false }: AnimatedLogoProps) => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationComplete, setAnimationComplete] = useState(false);

  useEffect(() => {
    if (autoPlay && !animationComplete) {
      const timer = setTimeout(() => {
        setIsAnimating(true);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [autoPlay, animationComplete]);

  useEffect(() => {
    if (isAnimating) {
      const timer = setTimeout(() => {
        setAnimationComplete(true);
        if (loop) {
          setTimeout(() => {
            setIsAnimating(false);
            setAnimationComplete(false);
          }, 2000);
        }
      }, 2400); // Duration of full animation
      return () => clearTimeout(timer);
    }
  }, [isAnimating, loop]);

  return (
    <div 
      className="animated-logo-container" 
      style={{ width: size, height: 'auto' }}
      data-animating={isAnimating}
    >
      <img 
        src="/logos/logo-oficial.png" 
        alt="Logo Bem Real"
        className={`logo-image ${isAnimating ? 'animating' : ''}`}
        style={{ 
          width: '100%',
          filter: 'drop-shadow(0 8px 32px rgba(205, 127, 50, 0.3))'
        }}
      />
      {isAnimating && (
        <>
          {/* Animated rings around logo */}
          <div className="logo-ring ring-1" />
          <div className="logo-ring ring-2" />
          <div className="logo-ring ring-3" />
          
          {/* Shimmer effect */}
          <div className="logo-shimmer" />
          
          {/* Particles burst */}
          {[...Array(12)].map((_, i) => (
            <div 
              key={i} 
              className="logo-particle"
              style={{
                '--angle': `${i * 30}deg`,
                animationDelay: `${i * 50}ms`
              } as React.CSSProperties}
            />
          ))}
        </>
      )}
    </div>
  );
};
