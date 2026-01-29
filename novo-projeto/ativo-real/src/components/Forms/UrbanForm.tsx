import { useState } from 'react'
import { activateUrbanAccount } from '../../services/onboardingService'
import { Button } from '../ui/Button'
import { FormField } from '../ui/FormField'
import { useToast } from '../ui/ToastProvider'

const onlyDigits = (value: string) => value.replace(/\D/g, '')

const formatCpf = (value: string) => {
    const digits = onlyDigits(value).slice(0, 11)
    const part1 = digits.slice(0, 3)
    const part2 = digits.slice(3, 6)
    const part3 = digits.slice(6, 9)
    const part4 = digits.slice(9, 11)
    let formatted = part1
    if (part2) formatted += `.${part2}`
    if (part3) formatted += `.${part3}`
    if (part4) formatted += `-${part4}`
    return formatted
}

export function UrbanForm() {
    const { showToast } = useToast()
    const [loading, setLoading] = useState(false)

    const [cpf, setCpf] = useState('')
    const [birthDate, setBirthDate] = useState('')
    const [newPassword, setNewPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')

    const handleUrbanSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        if (newPassword !== confirmPassword) {
            showToast('error', 'As senhas precisam ser iguais')
            setLoading(false)
            return
        }

        const cpfDigits = onlyDigits(cpf)
        if (cpfDigits.length !== 11) {
            showToast('error', 'CPF inválido: use 11 dígitos')
            setLoading(false)
            return
        }
        if (!birthDate) {
            showToast('error', 'Informe a data de nascimento')
            setLoading(false)
            return
        }

        try {
            await activateUrbanAccount({
                cpf: cpfDigits,
                birthDate,
                password: newPassword,
            })
            showToast('success', 'Conta urbana ativada com sucesso')
            setCpf('')
            setBirthDate('')
            setNewPassword('')
            setConfirmPassword('')
        } catch {
            showToast('error', 'Erro ao ativar conta urbana')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="form-stack mt-5">
            <h2 className="form-title">🏙️ Ativação Conta Urbana</h2>
            <form onSubmit={handleUrbanSubmit} className="form-stack">
                <FormField
                    id="cpf"
                    label="CPF"
                    type="text"
                    value={cpf}
                    onChange={(e) => setCpf(formatCpf(e.target.value))}
                    required
                />

                <FormField
                    id="birthDate"
                    label="Data de Nascimento"
                    type="date"
                    aria-label="Data de nascimento"
                    value={birthDate}
                    onChange={(e) => setBirthDate(e.target.value)}
                    required
                />

                <FormField
                    id="newPassword"
                    label="Nova Senha"
                    type="password"
                    aria-label="Nova senha"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                />

                <FormField
                    id="confirmPassword"
                    label="Confirmar Nova Senha"
                    type="password"
                    aria-label="Confirmar nova senha"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                />

                <Button
                    type="submit"
                    variant="info"
                    loading={loading}
                    className="mt-2"
                >
                    Criar Senha e Acessar
                </Button>
            </form>
        </div>
    )
}
