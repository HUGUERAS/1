import { useState, useEffect } from 'react';
import { Moon, Sun } from 'lucide-react';
import './DarkModeToggle.css';

export const DarkModeToggle = () => {
  const [isDark, setIsDark] = useState(() => {
    // Check localStorage or system preference
    const saved = localStorage.getItem('theme');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    // Apply theme
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(prev => !prev);
  };

  return (
    <button
      onClick={toggleTheme}
      className="dark-mode-toggle"
      aria-label={isDark ? 'Mudar para modo claro' : 'Mudar para modo escuro'}
      title={isDark ? 'Modo Claro' : 'Modo Escuro'}
    >
      <div className="toggle-track">
        <div className="toggle-thumb" data-theme={isDark ? 'dark' : 'light'}>
          {isDark ? (
            <Moon size={16} className="toggle-icon" />
          ) : (
            <Sun size={16} className="toggle-icon" />
          )}
        </div>
      </div>
    </button>
  );
};
