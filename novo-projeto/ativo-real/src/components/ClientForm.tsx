import React, { useState } from 'react';

/**
 * ClientForm.tsx
 * Formulário completo do cliente para preenchimento de dados cadastrais
 */

interface ClientFormData {
  nome_cliente: string;
  cpf_cnpj_cliente: string;
  telefone_cliente: string;
  endereco: string;
}

interface ClientFormProps {
  initialData?: Partial<ClientFormData>;
  onSubmit: (data: ClientFormData) => void;
  loading?: boolean;
}

export const ClientForm: React.FC<ClientFormProps> = ({ initialData, onSubmit, loading }) => {
  const [formData, setFormData] = useState<ClientFormData>({
    nome_cliente: initialData?.nome_cliente || '',
    cpf_cnpj_cliente: initialData?.cpf_cnpj_cliente || '',
    telefone_cliente: initialData?.telefone_cliente || '',
    endereco: initialData?.endereco || '',
  });

  const [errors, setErrors] = useState<Partial<Record<keyof ClientFormData, string>>>({});

  const validateCPF = (cpf: string): boolean => {
    const cleanCPF = cpf.replace(/\D/g, '');
    return cleanCPF.length === 11 || cleanCPF.length === 14; // CPF ou CNPJ
  };

  const formatPhone = (phone: string): string => {
    const clean = phone.replace(/\D/g, '');
    if (clean.length <= 10) {
      return clean.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    }
    return clean.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  };

  const formatCPF = (value: string): string => {
    const clean = value.replace(/\D/g, '');
    if (clean.length <= 11) {
      return clean.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }
    return clean.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validação
    const newErrors: Partial<Record<keyof ClientFormData, string>> = {};

    if (!formData.nome_cliente.trim()) {
      newErrors.nome_cliente = 'Nome é obrigatório';
    }

    if (!validateCPF(formData.cpf_cnpj_cliente)) {
      newErrors.cpf_cnpj_cliente = 'CPF/CNPJ inválido';
    }

    if (!formData.telefone_cliente.trim()) {
      newErrors.telefone_cliente = 'Telefone é obrigatório';
    }

    if (!formData.endereco.trim()) {
      newErrors.endereco = 'Endereço é obrigatório';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">📋 Dados Cadastrais</h2>

      {/* Nome */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Nome Completo *
        </label>
        <input
          type="text"
          value={formData.nome_cliente}
          onChange={(e) => setFormData({ ...formData, nome_cliente: e.target.value })}
          className={`w-full px-3 py-2 border rounded-md ${errors.nome_cliente ? 'border-red-500' : 'border-gray-300'
            }`}
          placeholder="João da Silva"
        />
        {errors.nome_cliente && (
          <p className="text-red-500 text-sm mt-1">{errors.nome_cliente}</p>
        )}
      </div>

      {/* CPF/CNPJ */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          CPF/CNPJ *
        </label>
        <input
          type="text"
          value={formData.cpf_cnpj_cliente}
          onChange={(e) =>
            setFormData({ ...formData, cpf_cnpj_cliente: formatCPF(e.target.value) })
          }
          className={`w-full px-3 py-2 border rounded-md ${errors.cpf_cnpj_cliente ? 'border-red-500' : 'border-gray-300'
            }`}
          placeholder="000.000.000-00"
          maxLength={18}
        />
        {errors.cpf_cnpj_cliente && (
          <p className="text-red-500 text-sm mt-1">{errors.cpf_cnpj_cliente}</p>
        )}
      </div>

      {/* Telefone */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Telefone *
        </label>
        <input
          type="tel"
          value={formData.telefone_cliente}
          onChange={(e) =>
            setFormData({ ...formData, telefone_cliente: formatPhone(e.target.value) })
          }
          className={`w-full px-3 py-2 border rounded-md ${errors.telefone_cliente ? 'border-red-500' : 'border-gray-300'
            }`}
          placeholder="(61) 99999-9999"
          maxLength={15}
        />
        {errors.telefone_cliente && (
          <p className="text-red-500 text-sm mt-1">{errors.telefone_cliente}</p>
        )}
      </div>

      {/* Endereço */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Endereço Completo *
        </label>
        <textarea
          value={formData.endereco}
          onChange={(e) => setFormData({ ...formData, endereco: e.target.value })}
          className={`w-full px-3 py-2 border rounded-md ${errors.endereco ? 'border-red-500' : 'border-gray-300'
            }`}
          placeholder="Rua, número, bairro, cidade, estado, CEP"
          rows={3}
        />
        {errors.endereco && (
          <p className="text-red-500 text-sm mt-1">{errors.endereco}</p>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full py-2 px-4 rounded-md text-white font-medium ${loading
          ? 'bg-gray-400 cursor-not-allowed'
          : 'bg-blue-600 hover:bg-blue-700'
          }`}
      >
        {loading ? 'Salvando...' : 'Salvar Dados'}
      </button>
    </form>
  );
};
