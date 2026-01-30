import { BrowserRouter, Routes, Route, useNavigate, Navigate, useSearchParams } from 'react-router-dom';
import GlobalMap from './GlobalMap';
import DashboardTopografo from './DashboardTopografo';
import AIChat from './components/AIChat';
import ImprovedProfileCard from './components/ImprovedProfileCard';
import { AIBotChat } from './components/AIBotChat';
import { ParticlesBackground } from './components/ParticlesBackground';
import { AnimatedLogo } from './components/AnimatedLogo';
import { DarkModeToggle } from './components/DarkModeToggle';
import { OnboardingTour } from './components/OnboardingTour';
import { RuralDashboard } from './pages/dashboards/RuralDashboard';
import { LoginPage } from './pages/LoginPage';
import './styles/design-tokens.css';

// Componente da Tela Inicial (Landing Page)
const LandingPage = () => {
    const navigate = useNavigate();

    const handleLogin = (profile: string) => {
        if (profile === 'topografo') {
            navigate('/dashboard');
        } else if (profile === 'agricultor') {
            navigate('/rural');
        } else {
            // Proprietário - por enquanto vai para o mapa com perfil proprietario
            navigate('/map?profile=proprietario');
        }
    };

    return (
      <div style={{
            height: '100vh', width: '100vw',
            background: 'linear-gradient(135deg, var(--navy-950) 0%, var(--navy-600) 100%)',
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            fontFamily: 'Segoe UI, sans-serif',
            position: 'relative',
            overflow: 'hidden'
        }}>
            <ParticlesBackground />
            <DarkModeToggle />
            <OnboardingTour run={true} />
            
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
            
            <style>{`
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            `}</style>
        </div>
    );
};

// Componente Wrapper para o Dashboard Topógrafo
const DashboardWrapper = () => {
    const navigate = useNavigate();
    return (
        <DashboardTopografo 
            onAbrirProjeto={(id) => navigate(`/map?projeto=${id}`)} 
            onVoltar={() => navigate('/')}
        />
    );
};

// Componente Wrapper para o Mapa
const MapWrapper = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    
    // Recupera perfil e projeto da URL ou assume defaults
    const profile = searchParams.get('profile') || 'topografo';
    const projetoId = searchParams.get('projeto') ? Number(searchParams.get('projeto')) : null;

    return (
        <>
            <GlobalMap 
                userProfile={profile} 
                projetoId={projetoId}
                onLogout={() => navigate('/')} 
            />
            <AIChat context={profile === 'topografo' ? 'general' : profile === 'proprietario' ? 'rural' : 'urban'} />
            <AIBotChat />
        </>
    );
};

const App = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/dashboard" element={<DashboardWrapper />} />
                <Route path="/rural" element={<RuralDashboard />} />
                <Route path="/map" element={<MapWrapper />} />
                {/* Fallback para rotas desconhecidas */}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </BrowserRouter>
    );
};

export default App;
