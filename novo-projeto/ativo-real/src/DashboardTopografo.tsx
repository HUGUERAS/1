import { useState, useEffect } from 'react';
import InfinitePayModal from './components/InfinitePayModal';
import { DarkModeToggle } from './components/DarkModeToggle';
import TopoIcon from './components/ui/TopoIcon';
import ManagePanelIcon from './assets/icons/topography/24px/manage-panel.svg?react';
import PaymentReceiveIcon from './assets/icons/topography/24px/payment-receive.svg?react';
import DashProjectsIcon from './assets/icons/topography/24px/dash-projects.svg?react';
import DashFinanceIcon from './assets/icons/topography/24px/dash-finance.svg?react';
import NewProjectIcon from './assets/icons/topography/32px/new-project.svg?react';
// Ícone pronto para uso futuro: logout

// --- INTERFACES COMBINADAS ---
interface Vizinho {
  id: number;
  nome: string;
  telefone: string;
  status: 'pendente' | 'assinado' | 'recusado';
  linkConvite: string;
}

interface DadosFinanceiros {
  valorTotal: number;
  valorPago: number;
  status: 'pendente' | 'parcial' | 'quitado';
  dataVencimento: string;
}

interface Projeto {
  id: number;
  titulo: string;
  local: string;
  proprietario: string;
  dataCriacao: string;
  status: string;
  tipo: string;
  area: number;
  progresso: number;
  vizinhos: Vizinho[];
  financeiro: DadosFinanceiros;
}

interface DashboardProps {
  onAbrirProjeto: (id: number) => void;
  onVoltar?: () => void;
}

// --- DADOS INICIAIS ---
const MOCK_INICIAL: Projeto[] = [
  { 
    id: 1, titulo: "Desmembramento Família Souza", local: "Gleba Rio Claro - SP", proprietario: "José Souza", 
    dataCriacao: "2023-10-25", status: "em_andamento", tipo: "desmembramento", area: 45.8, progresso: 65, 
    vizinhos: [
      { id: 1, nome: "João Silva (Fazenda Norte)", telefone: "(19) 98765-4321", status: "assinado", linkConvite: "https://ativo.real/convite/abc123" }
    ],
    financeiro: { valorTotal: 5000, valorPago: 2500, status: 'parcial', dataVencimento: '2023-11-20' }
  },
  { 
    id: 2, titulo: "Retificação Sítio Boa Vista", local: "Zona Rural - MG", proprietario: "Maria Santos", 
    dataCriacao: "2023-10-28", status: "concluido", tipo: "retificacao", area: 120.5, progresso: 100, 
    vizinhos: [],
    financeiro: { valorTotal: 12000, valorPago: 12000, status: 'quitado', dataVencimento: '2023-10-30' }
  }
];

// --- COMPONENTE KPI ---
const KpiCard = ({ valor, label, cor, isMoney = false }: { valor: string | number, label: string, cor: string, isMoney?: boolean }) => (
  <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)', borderBottom: `4px solid ${cor}` }}>
    <div style={{ fontSize: '24px', fontWeight: 'bold', color: cor }}>
      {isMoney ? `R$ ${Number(valor).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : valor}
    </div>
    <div style={{ color: '#7f8c8d', fontSize: '13px', marginTop: '5px' }}>{label}</div>
  </div>
);

export default function DashboardTopografo({ onAbrirProjeto, onVoltar }: DashboardProps) {
  const [projetos, setProjetos] = useState<Projeto[]>([]);
  const [modoVisualizacao, setModoVisualizacao] = useState<'projetos' | 'financeiro'>('projetos');
  
  // Modais
  const [modalNovoAberto, setModalNovoAberto] = useState(false);
  const [projetoEmGestao, setProjetoEmGestao] = useState<Projeto | null>(null);
  const [paymentModalOpen, setPaymentModalOpen] = useState(false);
  const [selectedProjectForPayment, setSelectedProjectForPayment] = useState<Projeto | null>(null);
  
  // Formulários
  const [novoProjData, setNovoProjData] = useState({ titulo: '', local: '', proprietario: '', area: '', valor: '' });
  const [novoVizinhoData, setNovoVizinhoData] = useState({ nome: '', telefone: '' });

  // 1. CARREGAR
  useEffect(() => {
    const salvos = localStorage.getItem('db_projetos_v2');
    if (salvos) setProjetos(JSON.parse(salvos));
    else {
      setProjetos(MOCK_INICIAL);
      localStorage.setItem('db_projetos_v2', JSON.stringify(MOCK_INICIAL));
    }
  }, []);

  // 2. SALVAR
  const salvarAlteracoes = (novaLista: Projeto[]) => {
    setProjetos(novaLista);
    localStorage.setItem('db_projetos_v2', JSON.stringify(novaLista));
  };

  // Cálculos Financeiros
  const financeiro = {
    totalContratado: projetos.reduce((acc, p) => acc + p.financeiro.valorTotal, 0),
    totalRecebido: projetos.reduce((acc, p) => acc + p.financeiro.valorPago, 0),
    totalPendente: projetos.reduce((acc, p) => acc + (p.financeiro.valorTotal - p.financeiro.valorPago), 0),
    inadimplentes: projetos.filter(p => p.financeiro.status === 'pendente' && new Date(p.financeiro.dataVencimento) < new Date()).length
  };

  // --- LÓGICA DE PROJETOS ---
  const criarProjeto = () => {
    if (!novoProjData.titulo) return alert("Nome obrigatório");
    const novo: Projeto = {
      id: Date.now(),
      titulo: novoProjData.titulo,
      local: novoProjData.local,
      proprietario: novoProjData.proprietario,
      area: Number(novoProjData.area) || 0,
      dataCriacao: new Date().toLocaleDateString('pt-BR'),
      status: 'em_andamento',
      tipo: 'desmembramento',
      progresso: 0,
      vizinhos: [],
      financeiro: {
        valorTotal: Number(novoProjData.valor) || 0,
        valorPago: 0,
        status: 'pendente',
        dataVencimento: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
      }
    };
    salvarAlteracoes([novo, ...projetos]);
    setModalNovoAberto(false);
    setNovoProjData({ titulo: '', local: '', proprietario: '', area: '', valor: '' });
  };

  const excluirProjeto = (id: number) => {
    if (confirm("ATENÇÃO: Apagar este projeto removerá também o mapa desenhado. Continuar?")) {
      const novaLista = projetos.filter(p => p.id !== id);
      salvarAlteracoes(novaLista);
      localStorage.removeItem(`rascunho_projeto_${id}`);
      if (projetoEmGestao?.id === id) setProjetoEmGestao(null);
    }
  };


  // --- LÓGICA DE VIZINHOS ---
  const adicionarVizinho = () => {
    if (!projetoEmGestao || !novoVizinhoData.nome) return;
    
    const novoVizinho: Vizinho = {
      id: Date.now(),
      nome: novoVizinhoData.nome,
      telefone: novoVizinhoData.telefone,
      status: 'pendente',
      linkConvite: `https://ativo.real/assinatura/${projetoEmGestao.id}/${Date.now()}`
    };

    const novaLista = projetos.map(p => {
      if (p.id === projetoEmGestao.id) {
        return { ...p, vizinhos: [...p.vizinhos, novoVizinho] };
      }
      return p;
    });

    salvarAlteracoes(novaLista);
    const projetoAtualizado = novaLista.find(p => p.id === projetoEmGestao.id) || null;
    setProjetoEmGestao(projetoAtualizado);
    setNovoVizinhoData({ nome: '', telefone: '' });
  };

  const removerVizinho = (idVizinho: number) => {
    if (!projetoEmGestao) return;
    const novaLista = projetos.map(p => {
      if (p.id === projetoEmGestao.id) {
        return { ...p, vizinhos: p.vizinhos.filter(v => v.id !== idVizinho) };
      }
      return p;
    });
    salvarAlteracoes(novaLista);
    const projetoAtualizado = novaLista.find(p => p.id === projetoEmGestao.id) || null;
    setProjetoEmGestao(projetoAtualizado);
  };

  const copiarLink = (link: string) => {
    navigator.clipboard.writeText(link);
    alert("🔗 Link copiado! Cole no WhatsApp do vizinho.");
  };

  // --- LÓGICA FINANCEIRA ---
  const receberPagamento = (id: number) => {
    const valor = prompt("Quanto o cliente pagou?");
    if (!valor) return;
    
    const novosProjetos = projetos.map(p => {
      if (p.id === id) {
        const novoPago = p.financeiro.valorPago + Number(valor);
        const novoStatus = novoPago >= p.financeiro.valorTotal ? 'quitado' : 'parcial';
        return { ...p, financeiro: { ...p.financeiro, valorPago: novoPago, status: novoStatus as any } };
      }
      return p;
    });
    salvarAlteracoes(novosProjetos);
  };

  // --- RENDERIZAÇÃO ---
  return (
    <div style={{ 
      padding: 'var(--space-10)', 
      background: 'var(--color-background)', 
      minHeight: '100vh', 
      fontFamily: 'Segoe UI',
      transition: 'background var(--transition-base)'
    }}>
      
      {/* Dark Mode Toggle */}
      <DarkModeToggle />
      
      {/* HEADER + ABAS */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: 'var(--space-6)',
        animation: 'fadeInUp 0.6s ease-out'
      }}>
        <div>
          <h1 style={{ 
            color: 'var(--color-text-primary)', 
            margin: 0,
            fontSize: 'var(--text-4xl)',
            fontWeight: 'var(--font-bold)'
          }}>Gestão Ativo Real</h1>
          <p style={{ 
            color: 'var(--color-text-secondary)', 
            margin: 0,
            fontSize: 'var(--text-lg)',
            marginTop: 'var(--space-2)'
          }}>Painel do Topógrafo</p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button 
            onClick={() => setModoVisualizacao('projetos')} 
            style={{ 
              ...btnStyle(modoVisualizacao === 'projetos' ? 'var(--color-primary)' : 'var(--glass-background)'), 
              color: modoVisualizacao === 'projetos' ? 'white' : 'var(--color-text-primary)', 
              border: 'var(--glass-border)',
              backdropFilter: 'var(--glass-blur)',
              transition: 'all var(--transition-fast)',
              boxShadow: modoVisualizacao === 'projetos' ? 'var(--shadow-bronze)' : 'var(--shadow-md)'
            }}
            onMouseEnter={(e) => {
              if (modoVisualizacao !== 'projetos') {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = modoVisualizacao === 'projetos' ? 'var(--shadow-bronze)' : 'var(--shadow-md)';
            }}
          >
            <TopoIcon Icon={DashProjectsIcon} size={20} color={modoVisualizacao === 'projetos' ? 'white' : 'var(--color-text-primary)'} ariaLabel="Projetos" />
            Projetos
          </button>
          <button 
            onClick={() => setModoVisualizacao('financeiro')} 
            style={{ 
              ...btnStyle(modoVisualizacao === 'financeiro' ? 'var(--color-primary)' : 'var(--glass-background)'), 
              color: modoVisualizacao === 'financeiro' ? 'white' : 'var(--color-text-primary)', 
              border: 'var(--glass-border)',
              backdropFilter: 'var(--glass-blur)',
              transition: 'all var(--transition-fast)',
              boxShadow: modoVisualizacao === 'financeiro' ? 'var(--shadow-bronze)' : 'var(--shadow-md)'
            }}
            onMouseEnter={(e) => {
              if (modoVisualizacao !== 'financeiro') {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = modoVisualizacao === 'financeiro' ? 'var(--shadow-bronze)' : 'var(--shadow-md)';
            }}
          >
            <TopoIcon Icon={DashFinanceIcon} size={20} color={modoVisualizacao === 'financeiro' ? 'white' : 'var(--color-text-primary)'} ariaLabel="Financeiro" />
            Financeiro
          </button>
          {onVoltar && (
            <button 
              onClick={onVoltar} 
              style={{
                ...btnStyle('#e74c3c'),
                transition: 'all var(--transition-fast)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              }}
            >Sair</button>
          )}
        </div>
      </div>

      {/* VISÃO 1: PROJETOS */}
      {modoVisualizacao === 'projetos' && (
        <>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'flex-end', 
            marginBottom: 'var(--space-6)',
            animation: 'fadeInUp 0.6s ease-out 0.1s backwards'
          }}>
            <button 
              onClick={() => setModalNovoAberto(true)} 
              style={{
                ...btnStyle('#27ae60'),
                background: 'var(--gradient-bronze)',
                border: 'none',
                boxShadow: 'var(--shadow-bronze)',
                transition: 'all var(--transition-fast)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px) scale(1.05)';
                e.currentTarget.style.boxShadow = 'var(--shadow-bronze-lg)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)';
                e.currentTarget.style.boxShadow = 'var(--shadow-bronze)';
              }}
            >
              <TopoIcon Icon={NewProjectIcon} size={32} color="white" ariaLabel="Novo Projeto" />
              Novo Projeto
            </button>
          </div>

          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', 
            gap: 'var(--space-6)',
            animation: 'fadeInUp 0.8s ease-out 0.2s backwards'
          }}>
            {projetos.map((p, index) => (
              <div 
                key={p.id} 
                style={{ 
                  background: 'var(--glass-background)', 
                  backdropFilter: 'var(--glass-blur)',
                  border: 'var(--glass-border)',
                  padding: 'var(--space-6)', 
                  borderRadius: 'var(--radius-xl)', 
                  boxShadow: 'var(--shadow-lg)', 
                  borderLeft: `4px solid var(--color-primary)`,
                  transition: 'all var(--transition-base)',
                  animation: `fadeInUp 0.6s ease-out ${0.3 + index * 0.1}s backwards`,
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-8px)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-2xl), var(--shadow-bronze)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
                }}
              >
                <h3 style={{ 
                  margin: '0 0 var(--space-2) 0', 
                  color: 'var(--color-text-primary)',
                  fontSize: 'var(--text-xl)',
                  fontWeight: 'var(--font-bold)'
                }}>{p.titulo}</h3>
                <p style={{ 
                  color: 'var(--color-text-secondary)', 
                  fontSize: 'var(--text-sm)',
                  lineHeight: 'var(--leading-relaxed)'
                }}>📍 {p.local} <br/> 👤 {p.proprietario}</p>
                
                {/* Barra de Progresso */}
                <div style={{ margin: '15px 0' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '3px' }}>
                    <span>Execução</span>
                    <strong>{p.progresso}%</strong>
                  </div>
                  <div style={{ width: '100%', height: '6px', background: '#eee', borderRadius: '3px' }}>
                    <div style={{ width: `${p.progresso}%`, height: '100%', background: '#27ae60', borderRadius: '3px' }}></div>
                  </div>
                </div>

                {/* Resumo de Envolvidos */}
                <div style={{ marginTop: '15px', padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#555', marginBottom: '5px' }}>ENVOLVIDOS ({p.vizinhos.length})</div>
                  {p.vizinhos.length === 0 && <span style={{ fontSize: '11px', color: '#999' }}>Nenhum vizinho adicionado.</span>}
                  {p.vizinhos.slice(0, 2).map(v => (
                    <div key={v.id} style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '5px', marginTop: '2px' }}>
                      <span style={{ color: v.status === 'pendente' ? 'red' : v.status === 'assinado' ? 'green' : '#f39c12' }}>●</span> {v.nome}
                    </div>
                  ))}
                  {p.vizinhos.length > 2 && <div style={{ fontSize: '11px', color: '#999' }}>+{p.vizinhos.length - 2} outros...</div>}
                </div>

                <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                  <button onClick={() => onAbrirProjeto(p.id)} style={{ ...btnStyle('#002B49'), flex: 1, padding: '10px' }}>🗺️ Mapa</button>
                  <button onClick={() => setProjetoEmGestao(p)} style={{ ...btnStyle('#e67e22'), padding: '10px' }}>
                    <TopoIcon Icon={ManagePanelIcon} size={24} color="white" ariaLabel="Gestão" />
                    Gestão
                  </button>
                  <button onClick={() => excluirProjeto(p.id)} style={{ ...btnStyle('#fee'), color: 'red', border: '1px solid red', padding: '10px' }}>🗑️</button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}


      {/* VISÃO 2: FINANCEIRO */}
      {modoVisualizacao === 'financeiro' && (
        <>
          {/* KPIs Financeiros */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '30px' }}>
            <KpiCard valor={financeiro.totalContratado} label="Total Contratado" cor="#002B49" isMoney />
            <KpiCard valor={financeiro.totalRecebido} label="Recebido (Caixa)" cor="#27ae60" isMoney />
            <KpiCard valor={financeiro.totalPendente} label="A Receber" cor="#f39c12" isMoney />
            <KpiCard valor={financeiro.inadimplentes} label="Clientes Inadimplentes" cor="#e74c3c" />
          </div>

          <h3 style={{ color: '#555' }}>Contas a Receber</h3>
          <div style={{ background: 'white', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 2px 5px rgba(0,0,0,0.05)' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ background: '#f8f9fa' }}>
                <tr>
                  <th style={thStyle}>Cliente / Projeto</th>
                  <th style={thStyle}>Vencimento</th>
                  <th style={thStyle}>Valor Total</th>
                  <th style={thStyle}>Pago</th>
                  <th style={thStyle}>Restante</th>
                  <th style={thStyle}>Status</th>
                  <th style={thStyle}>Ação</th>
                </tr>
              </thead>
              <tbody>
                {projetos.map(p => {
                  const restante = p.financeiro.valorTotal - p.financeiro.valorPago;
                  return (
                    <tr key={p.id} style={{ borderBottom: '1px solid #eee' }}>
                      <td style={tdStyle}><strong>{p.proprietario}</strong><br /><small>{p.titulo}</small></td>
                      <td style={tdStyle}>{new Date(p.financeiro.dataVencimento).toLocaleDateString()}</td>
                      <td style={tdStyle}>R$ {p.financeiro.valorTotal.toLocaleString()}</td>
                      <td style={{ ...tdStyle, color: '#27ae60' }}>R$ {p.financeiro.valorPago.toLocaleString()}</td>
                      <td style={{ ...tdStyle, color: '#e74c3c', fontWeight: 'bold' }}>R$ {restante.toLocaleString()}</td>
                      <td style={tdStyle}>
                        <span style={{
                          padding: '4px 8px', borderRadius: '4px', fontSize: '12px',
                          background: p.financeiro.status === 'quitado' ? '#d4edda' : p.financeiro.status === 'pendente' ? '#f8d7da' : '#fff3cd',
                          color: p.financeiro.status === 'quitado' ? '#155724' : p.financeiro.status === 'pendente' ? '#721c24' : '#856404'
                        }}>
                          {p.financeiro.status.toUpperCase()}
                        </span>
                      </td>
                      <td style={tdStyle}>
                        {restante > 0 && (
                          <>
                            <button onClick={() => receberPagamento(p.id)} style={{ ...btnStyle('#27ae60'), padding: '5px 10px', fontSize: '12px', marginRight: '5px' }}>
                              <TopoIcon Icon={PaymentReceiveIcon} size={20} color="white" ariaLabel="Receber Pagamento" />
                              Receber
                            </button>
                            <button 
                              onClick={() => {
                                setSelectedProjectForPayment(p);
                                setPaymentModalOpen(true);
                              }} 
                              style={{ ...btnStyle('#3b82f6'), padding: '5px 10px', fontSize: '12px' }}
                            >
                              💳 Online
                            </button>
                          </>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* MODAL 1: NOVO PROJETO */}
      {modalNovoAberto && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ background: 'white', padding: '30px', borderRadius: '12px', width: '400px' }}>
            <h2 style={{ marginTop: 0 }}>Novo Serviço</h2>
            <input placeholder="Nome do Projeto *" value={novoProjData.titulo} onChange={e => setNovoProjData({ ...novoProjData, titulo: e.target.value })} style={inputStyle} />
            <input placeholder="Proprietário" value={novoProjData.proprietario} onChange={e => setNovoProjData({ ...novoProjData, proprietario: e.target.value })} style={inputStyle} />
            <input placeholder="Local" value={novoProjData.local} onChange={e => setNovoProjData({ ...novoProjData, local: e.target.value })} style={inputStyle} />
            <div style={{ display: 'flex', gap: '10px' }}>
              <input type="number" placeholder="Área (ha)" value={novoProjData.area} onChange={e => setNovoProjData({ ...novoProjData, area: e.target.value })} style={inputStyle} />
              <input type="number" placeholder="Valor (R$)" value={novoProjData.valor} onChange={e => setNovoProjData({ ...novoProjData, valor: e.target.value })} style={inputStyle} />
            </div>
            <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
              <button onClick={() => setModalNovoAberto(false)} style={{ ...btnStyle('#eee'), color: '#333', flex: 1 }}>Cancelar</button>
              <button onClick={criarProjeto} style={{ ...btnStyle('#27ae60'), flex: 1 }}>Salvar</button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL 2: GERENCIAR VIZINHOS */}
      {projetoEmGestao && (
        <div style={styles.backdrop}>
          <div style={{ ...styles.modal, maxWidth: '600px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h2 style={{ marginTop: 0, fontSize: '20px' }}>Gerenciar: {projetoEmGestao.titulo}</h2>
              <button onClick={() => setProjetoEmGestao(null)} style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' }}>✖</button>
            </div>

            {/* Formulário de Adicionar */}
            <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', padding: '15px', background: '#f0f2f5', borderRadius: '8px', alignItems: 'flex-end' }}>
              <div style={{ flex: 2 }}>
                <label style={{ fontSize: '12px', fontWeight: 'bold' }}>Nome do Vizinho</label>
                <input placeholder="Ex: João da Cerca Norte" value={novoVizinhoData.nome} onChange={e => setNovoVizinhoData({ ...novoVizinhoData, nome: e.target.value })} style={{ ...styles.input, marginBottom: 0 }} />
              </div>
              <div style={{ flex: 1 }}>
                <label style={{ fontSize: '12px', fontWeight: 'bold' }}>Telefone</label>
                <input placeholder="(00) 00000-0000" value={novoVizinhoData.telefone} onChange={e => setNovoVizinhoData({ ...novoVizinhoData, telefone: e.target.value })} style={{ ...styles.input, marginBottom: 0 }} />
              </div>
              <button onClick={adicionarVizinho} style={{ ...styles.btn, background: '#27ae60', height: '42px' }}>Adicionar</button>
            </div>

            {/* Lista de Vizinhos */}
            <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
              {projetoEmGestao.vizinhos.length === 0 && <p style={{ textAlign: 'center', color: '#999' }}>Nenhum vizinho cadastrado.</p>}

              {projetoEmGestao.vizinhos.map(v => (
                <div key={v.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', borderBottom: '1px solid #eee' }}>
                  <div>
                    <strong>{v.nome}</strong> <span style={{ fontSize: '12px', color: '#777' }}>({v.telefone})</span>
                    <div style={{ fontSize: '12px', color: v.status === 'pendente' ? 'red' : v.status === 'assinado' ? 'green' : '#f39c12' }}>
                      Status: {v.status.toUpperCase()}
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '5px' }}>
                    <button onClick={() => copiarLink(v.linkConvite)} style={{ ...styles.btn, padding: '5px 10px', fontSize: '12px', background: '#3498db' }}>🔗 Link</button>
                    <button onClick={() => removerVizinho(v.id)} style={{ ...styles.btn, padding: '5px 10px', fontSize: '12px', background: '#fee', color: 'red', border: '1px solid red' }}>🗑️</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Modal de Pagamento InfinitePay */}
      {selectedProjectForPayment && (
        <InfinitePayModal
          isOpen={paymentModalOpen}
          onClose={() => {
            setPaymentModalOpen(false);
            setSelectedProjectForPayment(null);
          }}
          projectId={selectedProjectForPayment.id}
          projectTitle={selectedProjectForPayment.titulo}
          amount={selectedProjectForPayment.financeiro.valorTotal - selectedProjectForPayment.financeiro.valorPago}
          onSuccess={(paymentId) => {
            console.log('Pagamento aprovado:', paymentId);
            // Atualizar status do pagamento
            const novaLista = projetos.map(p => {
              if (p.id === selectedProjectForPayment.id) {
                return {
                  ...p,
                  financeiro: {
                    ...p.financeiro,
                    valorPago: p.financeiro.valorTotal,
                    status: 'quitado' as const
                  }
                };
              }
              return p;
            });
            salvarAlteracoes(novaLista);
            setPaymentModalOpen(false);
            setSelectedProjectForPayment(null);
            alert('✅ Pagamento confirmado!');
          }}
        />
      )}
    </div>
  );
}

// Estilos
const btnStyle = (bg: string) => ({ backgroundColor: bg, color: bg === '#eee' || bg === 'white' ? '#333' : 'white', border: 'none', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' });
const inputStyle = { width: '100%', padding: '10px', marginBottom: '10px', border: '1px solid #ddd', borderRadius: '6px', boxSizing: 'border-box' as const };
const thStyle = { padding: '15px', textAlign: 'left' as const, fontSize: '13px', color: '#666' };
const tdStyle = { padding: '15px', borderTop: '1px solid #eee', fontSize: '14px' };

const styles = {
  btn: { color: 'white', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' as const },
  card: { background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)', borderLeft: '5px solid #002B49' },
  input: { width: '100%', padding: '10px', marginBottom: '10px', border: '1px solid #ddd', borderRadius: '6px', boxSizing: 'border-box' as const },
  backdrop: { position: 'fixed' as const, top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 },
  modal: { background: 'white', padding: '30px', borderRadius: '12px', width: '90%', maxWidth: '500px' }
};



