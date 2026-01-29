import React, { useState } from 'react';
import Dashboard from './pages/Dashboard';
import MapEditor from './components/MapEditor';

function App() {
  const [currentProject, setCurrentProject] = useState(null);

  return (
    <div className="min-h-screen bg-[var(--color-background)]">
      {currentProject ? (
        <MapEditor 
          projetoId={currentProject.id} 
          onBack={() => setCurrentProject(null)} 
        />
      ) : (
        <Dashboard 
          onSelectProjeto={(proj) => setCurrentProject(proj)} 
        />
      )}
    </div>
  );
}

export default App;
