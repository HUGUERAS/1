import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { FormField } from '../components/ui/FormField';
import type { LoginResponse } from '../types/auth';

export function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE || '/api'}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) throw new Error('Falha no login');

            const data: LoginResponse = await response.json();
            localStorage.setItem('user', JSON.stringify(data.user));

            if (data.user.role !== 'TECH') {
                navigate('/app/rural');
            } else {
                navigate('/'); // Redirect tech users
            }
        } catch (err) {
            console.error(err);
            setError('Credenciais inválidas');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-bem-navy">
            <div className="w-full max-w-md bg-white rounded-xl shadow-2xl p-8">
                <h1 className="text-3xl font-bold text-center text-bem-gold mb-8 font-serif">Bem Real</h1>

                <form onSubmit={handleLogin} className="space-y-6">
                    <FormField
                        label="Email"
                        id="email"
                        type="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                        placeholder="admin@bemreal.com"
                    />
                    <FormField
                        label="Senha"
                        id="password"
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                    />

                    {error && <p className="text-red-500 text-sm text-center">{error}</p>}

                    <Button
                        type="submit"
                        className="w-full !bg-bem-gold !text-bem-navy hover:!brightness-110 font-bold text-lg"
                        loading={isLoading}
                    >
                        Entrar
                    </Button>
                </form>
            </div>
        </div>
    );
}
