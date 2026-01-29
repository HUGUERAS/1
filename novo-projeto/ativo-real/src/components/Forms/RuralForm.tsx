import { useState } from 'react'
import { registerRuralFarm } from '../../services/onboardingService'
import { Button } from '../ui/Button'
import { FormField } from '../ui/FormField'
import { useToast } from '../ui/ToastProvider'

const onlyDigits = (value: string) => value.replace(/\D/g, '')

export function RuralForm() {
    const { showToast } = useToast()
    const [loading, setLoading] = useState(false)

    const [farmName, setFarmName] = useState('')
    const [document, setDocument] = useState('')
    const [area, setArea] = useState('')
    const [email, setEmail] = useState('')

    const handleRuralSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        try {
            await registerRuralFarm({
                farmName,
                document,
                area,
                email,
            })
            showToast('success', 'Conta rural criada com sucesso')
            setFarmName('')
            setDocument('')
            setArea('')
            setEmail('')
        } catch {
            showToast('error', 'Erro ao criar conta rural')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="form-stack mt-5">
            <h2 className="form-title">🚜 Cadastro Rural (B2B)</h2>
            <form onSubmit={handleRuralSubmit} className="form-stack">
                <FormField
                    id="farmName"
                    label="Nome da Fazenda"
                    type="text"
                    value={farmName}
                    onChange={(e) => setFarmName(e.target.value)}
                    required
                />

                <FormField
                    id="document"
                    label="CPF ou CNPJ"
                    type="text"
                    value={document}
                    onChange={(e) => setDocument(onlyDigits(e.target.value))}
                    required
                />

                <FormField
                    id="area"
                    label="Área Aproximada (hectares)"
                    type="number"
                    value={area}
                    onChange={(e) => setArea(e.target.value)}
                    required
                />

                <FormField
                    id="email"
                    label="E-mail do Responsável"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <Button
                    type="submit"
                    variant="success"
                    loading={loading}
                    className="mt-2"
                >
                    Criar Conta Rural
                </Button>
            </form>
        </div>
    )
}
