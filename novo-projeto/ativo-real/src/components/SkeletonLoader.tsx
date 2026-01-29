import './SkeletonLoader.css';

interface SkeletonLoaderProps {
  type?: 'text' | 'card' | 'map' | 'dashboard' | 'avatar' | 'button';
  count?: number;
  height?: number;
  width?: number | string;
  className?: string;
}

export const SkeletonLoader = ({ 
  type = 'text', 
  count = 1, 
  height,
  width = '100%',
  className = '' 
}: SkeletonLoaderProps) => {
  
  const renderSkeleton = () => {
    switch (type) {
      case 'card':
        return (
          <div className="skeleton-card">
            <div className="skeleton-image" />
            <div className="skeleton-content">
              <div className="skeleton-line" style={{ width: '60%' }} />
              <div className="skeleton-line" style={{ width: '80%' }} />
              <div className="skeleton-line" style={{ width: '40%' }} />
            </div>
          </div>
        );
      
      case 'map':
        return (
          <div className="skeleton-map">
            <div className="skeleton-map-controls">
              <div className="skeleton-circle" />
              <div className="skeleton-circle" />
              <div className="skeleton-circle" />
            </div>
            <div className="skeleton-map-layers">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="skeleton-line" style={{ width: '80%' }} />
              ))}
            </div>
          </div>
        );
      
      case 'dashboard':
        return (
          <div className="skeleton-dashboard">
            <div className="skeleton-stats">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="skeleton-stat-card">
                  <div className="skeleton-circle" />
                  <div className="skeleton-line" style={{ width: '70%' }} />
                </div>
              ))}
            </div>
            <div className="skeleton-chart">
              <div className="skeleton-bars">
                {[...Array(6)].map((_, i) => (
                  <div 
                    key={i} 
                    className="skeleton-bar"
                    style={{ height: `${Math.random() * 60 + 40}%` }}
                  />
                ))}
              </div>
            </div>
          </div>
        );
      
      case 'avatar':
        return <div className="skeleton-circle" style={{ width: width, height: height || width }} />;
      
      case 'button':
        return <div className="skeleton-button" style={{ width, height }} />;
      
      default: // text
        return (
          <div 
            className="skeleton-line" 
            style={{ 
              width, 
              height: height || 16 
            }} 
          />
        );
    }
  };

  return (
    <div className={`skeleton-container ${className}`}>
      {[...Array(count)].map((_, i) => (
        <div key={i} className="skeleton-wrapper">
          {renderSkeleton()}
        </div>
      ))}
    </div>
  );
};
