# 🚀 MCP Servers - Ativo Real

**Model Context Protocol servers** para integrar Claude Desktop com o projeto Ativo Real.

## ⚡ Início Rápido

```bash
# 1. Instalar dependências
npm install

# 2. Configurar automaticamente
.\setup.ps1
```

O script `setup.ps1` irá:
- ✅ Compilar os servidores TypeScript
- ✅ Criar o arquivo de configuração do Claude Desktop
- ✅ Configurar os caminhos automaticamente

---

## 📚 Documentação Completa

| Guia | Descrição | Para quem? |
|------|-----------|------------|
| **[CONFIGURACAO.md](CONFIGURACAO.md)** | Setup passo-a-passo completo | Primeira vez |
| **[TESTES.md](TESTES.md)** | Exemplos básicos de teste | Validar instalação |
| **[COMANDOS-PRONTOS.md](COMANDOS-PRONTOS.md)** | ⚡ Copy/paste direto no Claude | Uso diário |
| **[TESTES-FEATURES.md](TESTES-FEATURES.md)** | Testar funcionalidades faltantes | Desenvolvimento |
| **[CASOS-DE-USO.md](CASOS-DE-USO.md)** | 8 casos reais do Ativo Real | Cenários práticos |
| **[AUTOMACOES.md](AUTOMACOES.md)** | Workflows avançados | Produtividade |

---

## 📦 Servidores Disponíveis

### 1. MCP Filesystem 🗺️
Manipula arquivos do sistema.

**Ferramentas:**
- `read_file` - Lê arquivos
- `write_file` - Salva arquivos
- `list_files` - Lista diretórios

### 2. MCP Cosmos DB 💾
Gerencia projetos no Azure Cosmos DB.

**Ferramentas:**
- `create_project` - Cria novo projeto
- `list_projects` - Lista projetos
- `get_project` - Busca por ID

---

## 🧪 Teste Rápido (3 minutos)

No Claude Desktop, execute:

```
Claude, cria um projeto de teste no Cosmos DB:
- Título: Meu Primeiro Projeto
- Local: São Paulo-SP
- Proprietário: João Silva
```

Se funcionar, seu MCP está 100% operacional! ✅

---

## 🎯 Por que usar MCP?

**Antes (sem MCP):**
- 🐌 Horas desenvolvendo features
- 🐛 Bugs por falta de testes
- 🔄 Retrabalho constante

**Depois (com MCP):**
- ⚡ Protótipos em minutos
- ✅ Lógica validada antes de codificar
- 🎯 Zero retrabalho

**Economia real:** ~94% do tempo de desenvolvimento! 

Veja casos práticos em **[CASOS-DE-USO.md](CASOS-DE-USO.md)**

---

## 💡 Uso Rápido

**Para testar funcionalidades que ainda não existem no app:**
```
Claude, vou implementar sistema de pagamentos.
Testa a lógica com dados do Cosmos DB antes de eu criar a UI.
```

**Para gerar relatórios:**
```
Claude, analisa todos os projetos e me dá resumo financeiro.
```

**Para automatizar tarefas:**
```
Claude, faz backup de todos os projetos para C:\Backups\
```

Veja 50+ comandos prontos em **[COMANDOS-PRONTOS.md](COMANDOS-PRONTOS.md)**!
