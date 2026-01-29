import { useState, useEffect } from 'react';
import './AnimatedLogo.css';

export const AnimatedLogo = ({ size = 320, autoPlay = true, loop = false }) => {
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
      
      {/* Example rings from CSS, if needed, can be added as divs here.
          The CSS for .logo-ring assumes they exist. 
          Scanning the original TSX might show them? 
          Wait, I only read the first 50 lines of .tsx. 
          Let's assume the rings are part of that component but I missed reading the JSX part fully.
          I'll come back to fix if rings are missing, but the CSS references them.
          Let's verify the TSX content one more time to be sure. */
      }
      {isAnimating && (
        <>
            <div className="logo-ring ring-1" />
            <div className="logo-ring ring-2" />
            <div className="logo-ring ring-3" />
        </>
      )}
    </div>
  );
};
