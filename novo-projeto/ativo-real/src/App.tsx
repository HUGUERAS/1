import { useState } from 'react';
import GlobalMap from './GlobalMap';
import DashboardTopografo from './DashboardTopografo';
import AIChat from './components/AIChat';
import ImprovedProfileCard from './components/ImprovedProfileCard';
import { AIBotChat } from './components/AIBotChat';
import { ParticlesBackground } from './components/ParticlesBackground';
import { AnimatedLogo } from './components/AnimatedLogo';
import { DarkModeToggle } from './components/DarkModeToggle';
import { OnboardingTour } from './components/OnboardingTour';
import './styles/design-tokens.css';

const App = () => {
  const [currentView, setCurrentView] = useState('landing'); // 'landing', 'dashboard' ou 'map'
  const [userProfile, setUserProfile] = useState<string | null>(null); // 'topografo', 'proprietario', 'agricultor'
  const [projetoAtual, setProjetoAtual] = useState<number | null>(null);

  // Função que o usuário chama ao escolher um card
  const handleLogin = (profile: string) => {
    setUserProfile(profile);
    if (profile === 'topografo') {
      setCurrentView('dashboard'); // Topógrafo vai para dashboard de projetos
    } else {
      setCurrentView('map'); // Outros perfis vão direto para o mapa
    }
  };

  // 1. SE FOR LANDING PAGE, MOSTRA A TELA INICIAL
  if (currentView === 'landing') {
    return (
      <div style={{
        height: '100vh', width: '100vw',
        background: 'linear-gradient(135deg, var(--navy-950) 0%, var(--navy-600) 100%)',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        fontFamily: 'Segoe UI, sans-serif',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Particles Background */}
        <ParticlesBackground />
        
        {/* Dark Mode Toggle */}
        <DarkModeToggle />
        
        {/* Onboarding Tour */}
        <OnboardingTour run={true} />
        
        {/* Hero Section com Logo Animada */}
        <div style={{ textAlign: 'center', marginBottom: '60px', color: 'white', position: 'relative', zIndex: 1 }}>
          <AnimatedLogo size={320} autoPlay={true} loop={false} />
          <p className="text-gradient-bronze" style={{ 
            opacity: 0.9, 
            fontSize: 'var(--text-xl)', 
            marginTop: 'var(--space-6)', 
            fontWeight: 'var(--font-light)', 
            letterSpacing: 'var(--tracking-wide)',
            animation: 'fadeInUp 0.8s ease-out 1.2s backwards'
          }}>
            A tecnologia que conecta seu patrimônio à regularidade.
          </p>
        </div>

        {/* Seleção de Perfil */}
        <div style={{ 
          display: 'flex', 
          gap: 'var(--space-6)', 
          flexWrap: 'wrap', 
          justifyContent: 'center',
          position: 'relative',
          zIndex: 1,
          animation: 'fadeInUp 0.8s ease-out 1.4s backwards'
        }}>
          <ImprovedProfileCard 
            icon="ruler" 
            title="Topógrafo" 
            desc="Ferramentas técnicas de desenho e medição."
            onClick={() => handleLogin('topografo')}
            gradient="var(--gradient-bronze)"
          />
          <ImprovedProfileCard 
            icon="house" 
            title="Proprietário" 
            desc="Acompanhe a regularização do seu imóvel."
            onClick={() => handleLogin('proprietario')}
            gradient="var(--gradient-navy-subtle)"
          />
          <ImprovedProfileCard 
            icon="tractor" 
            title="Agricultor" 
            desc="Gestão de CAR e áreas produtivas."
            onClick={() => handleLogin('agricultor')}
            gradient="var(--gradient-gold)"
          />
        </div>
        
        {/* Fade-in animations */}
        <style>{`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(30px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}</style>
      </div>
    );
  }

  // 2. SE FOR DASHBOARD DO TOPÓGRAFO, MOSTRA A LISTA DE PROJETOS
  if (currentView === 'dashboard' && userProfile === 'topografo') {
    return <DashboardTopografo 
      onAbrirProjeto={(id) => { setProjetoAtual(id); setCurrentView('map'); }} 
      onVoltar={() => { setCurrentView('landing'); setUserProfile(null); }}
    />;
  }

  // 3. SE FOR MAPA, MOSTRA O GLOBALMAP
  return (
    <>
      <GlobalMap 
        userProfile={userProfile!} 
        projetoId={projetoAtual}
        onLogout={() => { 
          if (userProfile === 'topografo') {
            setCurrentView('dashboard'); // Topógrafo volta para dashboard
            setProjetoAtual(null);
          } else {
            setCurrentView('landing'); // Outros voltam para login
            setUserProfile(null); 
          }
        }} 
      />
      <AIChat context={userProfile === 'topografo' ? 'general' : userProfile === 'proprietario' ? 'rural' : 'urban'} />
      <AIBotChat />
    </>
  );
};

export default App;
