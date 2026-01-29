import { useState } from 'react'
import { loginTechnician } from '../../services/onboardingService'
import { Button } from '../ui/Button'
import { FormField } from '../ui/FormField'
import { useToast } from '../ui/ToastProvider'

export function TechLoginForm() {
    const { showToast } = useToast()
    const [loading, setLoading] = useState(false)

    const [techUser, setTechUser] = useState('')
    const [techPassword, setTechPassword] = useState('')

    const handleTechnicianSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        if (!techUser || !techPassword) {
            showToast('error', 'Informe usuário e senha do técnico')
            setLoading(false)
            return
        }

        try {
            await loginTechnician({ username: techUser, password: techPassword })
            showToast('success', 'Sessão do técnico iniciada')
            setTechUser('')
            setTechPassword('')
        } catch {
            showToast('error', 'Erro ao autenticar técnico')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="form-stack mt-5">
            <h2 className="form-title">🛠️ Acesso do Profissional</h2>
            <p className="helper-text">Autentique-se para acessar o workspace técnico.</p>
            <form onSubmit={handleTechnicianSubmit} className="form-stack">
                <FormField
                    id="techUser"
                    label="Usuário"
                    type="text"
                    value={techUser}
                    onChange={(e) => setTechUser(e.target.value)}
                    required
                />

                <FormField
                    id="techPassword"
                    label="Senha"
                    type="password"
                    value={techPassword}
                    onChange={(e) => setTechPassword(e.target.value)}
                    required
                />

                <div className="flex flex-col gap-3">
                    <Button
                        type="submit"
                        variant="primary"
                        loading={loading}
                        className="mt-1"
                    >
                        Entrar no Workspace
                    </Button>
                    {/* 
                    <a
                        className="text-sm font-semibold text-blue-900 underline-offset-2 hover:underline"
                        href="https://workspace.exemplo.com"
                        target="_blank"
                        rel="noreferrer"
                    >
                        Ir para o workspace
                    </a>
                    */}
                </div>
            </form>
        </div>
    )
}
