import { BrowserRouter, Routes, Route, Navigate, useParams, useNavigate, useSearchParams } from 'react-router-dom';
import GlobalMap from './GlobalMapValidacao';
import DashboardTopografo from './DashboardTopografo';
import { ClientPortal } from './components/ClientPortal';
import { AIBotChat } from './components/AIBotChat';
import { ParticlesBackground } from './components/ParticlesBackground';
import { AnimatedLogo } from './components/AnimatedLogo';
import { DarkModeToggle } from './components/DarkModeToggle';
import { LoginPage } from './pages/LoginPage';
import ImprovedProfileCard from './components/ImprovedProfileCard';
import './styles/design-tokens.css';

const LandingPage = () => {
    const navigate = useNavigate();
    return (
      <div style={{ height: '100vh', background: 'linear-gradient(135deg, var(--navy-950), var(--navy-600))', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <ParticlesBackground />
            <DarkModeToggle />
            <div style={{ textAlign: 'center', marginBottom: '60px', color: 'white', zIndex: 1 }}>
                <AnimatedLogo size={320} autoPlay loop={false} />
                <p style={{ fontSize: '1.5rem', marginTop: '24px' }}>A tecnologia que conecta seu patrimônio à regularidade.</p>
            </div>
            <div style={{ display: 'flex', gap: '24px', zIndex: 1 }}>
                <ImprovedProfileCard icon="ruler" title="Topógrafo" desc="Ferramentas técnicas." onClick={() => navigate('/dashboard')} />
                <ImprovedProfileCard icon="house" title="Cliente" desc="Acompanhe seu imóvel." onClick={() => alert('Você receberá um link por email')} />
            </div>
        </div>
    );
};

const ClientPortalWrapper = () => {
    const { token } = useParams<{ token: string }>();
    if (!token) return <div style={{ padding: '20px', textAlign: 'center' }}><h2>❌ Token inválido</h2></div>;
    return <ClientPortal token={token} />;
};

const DashboardWrapper = () => {
    const navigate = useNavigate();
    return <DashboardTopografo onAbrirProjeto={(id) => navigate(`/map?projeto=${id}`)} onVoltar={() => navigate('/')} />;
};

const MapWrapper = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const projetoId = searchParams.get('projeto') ? Number(searchParams.get('projeto')) : null;
    return (
        <>
            <GlobalMap userProfile="topografo" projetoId={projetoId} onLogout={() => navigate('/')} />
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
                <Route path="/map" element={<MapWrapper />} />
                <Route path="/client/:token" element={<ClientPortalWrapper />} />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </BrowserRouter>
    );
};

export default App;
