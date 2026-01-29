export interface User {
    id: string;
    name: string;
    role: string;
}

export interface LoginResponse {
    user: User;
}

export interface Confrontante {
    id: string;
    nome: string;
    status: 'Identificado' | 'Contatado' | 'Assinado' | 'Litígio';
    contato: string;
}

export interface RuralDashboardData {
    id: string;
    nome_imovel: string;
    metadados: any;
    confrontantes: Confrontante[];
}
