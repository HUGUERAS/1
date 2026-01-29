import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { User, RuralDashboardData } from '../../types/auth';

export function RuralDashboard() {
    const navigate = useNavigate();
    const [user, setUser] = useState<User | null>(null);
    const [data, setData] = useState<RuralDashboardData | null>(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (!storedUser) {
            navigate('/login');
            return;
        }
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);

        fetch(`${import.meta.env.VITE_API_BASE || '/api'}/rural/dashboard/${parsedUser.id}`)
            .then(res => {
                if (!res.ok) throw new Error('Failed load dashboard');
                return res.json();
            })
            .then((data: RuralDashboardData) => setData(data))
            .catch(err => console.error(err));
    }, [navigate]);

    if (!user) return null;

    const columns = {
        'Identificado': 'border-yellow-400',
        'Contatado': 'border-blue-400',
        'Assinado': 'border-green-400',
        'Litígio': 'border-red-400'
    };

    const getCardsByStatus = (status: string) =>
        data?.confrontantes?.filter(c => c.status === status) || [];

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            {/* Header */}
            <header className="bg-bem-navy text-white px-6 py-4 shadow-md flex justify-between items-center">
                <div className="flex items-center gap-2">
                    <span className="text-bem-gold font-bold text-xl font-serif">Bem Real</span>
                </div>
                <div className="font-medium text-bem-cream">Olá, {user.name}</div>
            </header>

            <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-8">
                {/* Top Section: Property Card */}
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <h2 className="text-2xl font-bold text-gray-800">{data ? data.nome_imovel : 'Carregando imóvel...'}</h2>
                    <p className="text-gray-500 mt-1">Status: <span className="text-blue-600 font-semibold">Regularização em Andamento</span></p>
                </div>

                {/* Kanban Board */}
                <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Gestão de Confrontantes</h3>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        {Object.entries(columns).map(([status, borderColor]) => (
                            <div key={status} className="bg-gray-100/50 p-4 rounded-lg min-h-[300px]">
                                <h4 className="font-semibold text-gray-700 mb-3">{status}</h4>
                                <div className="space-y-3">
                                    {getCardsByStatus(status).map(card => (
                                        <div key={card.id} className={`bg-white p-3 rounded shadow-sm border-l-4 ${borderColor}`}>
                                            <p className="font-medium text-gray-800">{card.nome}</p>
                                            <p className="text-sm text-gray-500 truncate">{card.contato}</p>
                                        </div>
                                    ))}
                                    {getCardsByStatus(status).length === 0 && (
                                        <p className="text-xs text-gray-400 italic">Nenhum item</p>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
}
