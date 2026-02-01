import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Button } from '../components/ui/Button';
import { AnimatedLogo } from '../components/AnimatedLogo';
import { TopoIcon } from '../components/ui/TopoIcon';
import { Plus, Map, FolderOpen, Loader2 } from 'lucide-react';

export default function Dashboard({ onSelectProjeto }) {
  const [projetos, setProjetos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProjetos();
  }, []);

  async function loadProjetos() {
    try {
      setLoading(true);
      const data = await api.getProjetos();
      // Azure Functions might return { projects: [...] } or just [...]
      // Adjust based on your backend return. Assuming direct array or { projects: [] } for now.
      setProjetos(Array.isArray(data) ? data : data.projects || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateProjeto() {
    const nome = prompt("Nome do novo projeto:");
    if (!nome) return;

    try {
      setLoading(true);
      const novo = await api.createProjeto({ 
          nome, 
          descricao: `Criado em ${new Date().toLocaleDateString()}` 
      });
      loadProjetos();
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[var(--color-background)] text-[var(--color-text-primary)]">
      {/* Header / Hero */}
      <header className="pt-12 pb-8 px-6 flex flex-col items-center justify-center border-b border-[var(--color-border)] bg-[var(--color-surface)]">
        <AnimatedLogo size={120} autoPlay loop={false} />
        <h1 className="mt-6 text-3xl font-bold bg-gradient-to-r from-[var(--bronze-600)] to-[var(--gold)] bg-clip-text text-transparent">
          Bem Real Topografia
        </h1>
        <p className="mt-2 text-[var(--titanium-500)]">
          Gestão Inteligente de Ativos Imobiliários
        </p>
      </header>

      {/* Content */}
      <main className="max-w-4xl mx-auto p-6">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <TopoIcon Icon={FolderOpen} size={24} />
            Seus Projetos
          </h2>
          <Button onClick={handleCreateProjeto} variant="primary">
            <Plus className="w-4 h-4 mr-2" />
            Novo Projeto
          </Button>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-[var(--bronze-600)]" />
          </div>
        ) : error ? (
           <div className="p-4 rounded-md bg-red-50 text-red-600 border border-red-200">
             Erro: {error}
           </div>
        ) : projetos.length === 0 ? (
          <div className="text-center py-12 rounded-xl border-2 border-dashed border-[var(--color-border)]">
            <p className="text-[var(--titanium-500)] mb-4">Nenhum projeto encontrado</p>
            <Button onClick={handleCreateProjeto} variant="ghost">
              Criar meu primeiro projeto
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {projetos.map((proj) => (
              <div 
                key={proj.id} 
                className="group p-5 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] hover:border-[var(--bronze-600)] transition-all cursor-pointer shadow-sm hover:shadow-md"
                onClick={() => onSelectProjeto(proj)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-lg text-[var(--color-text-primary)] group-hover:text-[var(--bronze-600)] transition-colors">
                      {proj.nome}
                    </h3>
                    <p className="text-sm text-[var(--titanium-500)] mt-1">
                      {proj.descricao || 'Sem descrição'}
                    </p>
                  </div>
                  <TopoIcon Icon={Map} size={20} className="text-[var(--titanium-400)] group-hover:text-[var(--bronze-600)]" />
                </div>
                <div className="mt-4 flex items-center gap-2 text-xs text-[var(--titanium-400)]">
                  <span className="bg-[var(--navy-900)] px-2 py-1 rounded-full border border-[var(--color-border)]">
                    ID: {proj.id?.toString().slice(0,8)}...
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
