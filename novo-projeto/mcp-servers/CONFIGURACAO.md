# 🎯 Como Configurar o MCP no Claude Desktop

## 📍 Passo 1: Localizar o Arquivo de Configuração

### Windows:
```
%APPDATA%\Claude\claude_desktop_config.json
```

Caminho completo:
```
C:\Users\huugo\AppData\Roaming\Claude\claude_desktop_config.json
```

### macOS:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

---

## 📝 Passo 2: Editar claude_desktop_config.json

Abra o arquivo (crie se não existir) e adicione:

```json
{
  "mcpServers": {
    "ativo-real-filesystem": {
      "command": "node",
      "args": [
        "C:\\Users\\huugo\\topdemais\\mcp-servers\\dist\\filesystem-server.js"
      ]
    },
    "ativo-real-cosmosdb": {
      "command": "node",
      "args": [
        "C:\\Users\\huugo\\topdemais\\mcp-servers\\dist\\cosmosdb-server.js"
      ],
      "env": {
        "COSMOS_ENDPOINT": "https://SEU-COSMOS-ACCOUNT.documents.azure.com:443/",
        "COSMOS_KEY": "SUA-CHAVE-PRIMARIA-AQUI"
      }
    }
  }
}
```

**⚠️ IMPORTANTE:**
- Ajuste os caminhos para o seu sistema!
- No macOS/Linux, use `/` em vez de `\\`
- Troque `SEU-COSMOS-ACCOUNT` e `SUA-CHAVE-PRIMARIA` pelos valores reais

---

## 🔑 Passo 3: Obter Credenciais do Cosmos DB

### Opção A: Usar Azure Portal

1. Acesse: https://portal.azure.com
2. Vá em: **Azure Cosmos DB**
3. Selecione sua conta (ou crie uma nova)
4. No menu esquerdo: **Keys**
5. Copie:
   - **URI** → Variável `COSMOS_ENDPOINT`
   - **Primary Key** → Variável `COSMOS_KEY`

### Opção B: Criar Cosmos DB via Azure CLI

```bash
# Login
az login

# Criar resource group
az group create --name rg-ativo-real --location eastus

# Criar Cosmos DB account
az cosmosdb create \
  --name ativoreal-cosmos \
  --resource-group rg-ativo-real \
  --locations regionName=EastUS

# Obter endpoint
az cosmosdb show \
  --name ativoreal-cosmos \
  --resource-group rg-ativo-real \
  --query documentEndpoint -o tsv

# Obter chave
az cosmosdb keys list \
  --name ativoreal-cosmos \
  --resource-group rg-ativo-real \
  --query primaryMasterKey -o tsv
```

---

## ✅ Passo 4: Testar a Configuração

### 1. Reiniciar Claude Desktop
Feche completamente e abra novamente.

### 2. Verificar Status
No Claude Desktop, os servidores MCP devem aparecer como "ativos" na lista de ferramentas.

### 3. Testar MCP Filesystem

Pergunte no Claude:

```
Liste os arquivos na pasta C:\Users\huugo\topdemais\ativo-real\src
```

Claude deve usar automaticamente a ferramenta `list_files`!

### 4. Testar MCP Cosmos DB

```
Cria um projeto chamado "Fazenda Santa Clara" em Campinas-SP
```

Claude deve criar o projeto no Cosmos DB e retornar o ID!

---

## 🔧 Troubleshooting

### Erro: "MCP server failed to start"

**Causas comuns:**
1. Caminho incorreto no config.json
2. Node.js não está no PATH
3. Servidor não compilado

**Solução:**
```bash
# Verificar Node.js
node --version

# Recompilar
cd C:\Users\huugo\topdemais\mcp-servers
npm run build

# Testar manualmente
node dist\filesystem-server.js
```

### Erro: "COSMOS_ENDPOINT not configured"

**Solução:** Certifique-se de que as variáveis de ambiente estão no `claude_desktop_config.json`:

```json
"env": {
  "COSMOS_ENDPOINT": "https://ativoreal-cosmos.documents.azure.com:443/",
  "COSMOS_KEY": "abc123...xyz789"
}
```

### Claude não reconhece as ferramentas

**Solução:**
1. Reinicie Claude Desktop completamente
2. Aguarde 10-15 segundos após abrir
3. Teste com comando direto: "use a ferramenta list_files"

---

## 🎓 Exemplos de Uso

### Listar arquivos TypeScript

```
Claude, lista todos os arquivos .tsx na pasta src do projeto Ativo Real
```

### Criar projeto no Cosmos DB

```
Cria um projeto topográfico:
- Título: Loteamento Vila Nova
- Local: São Paulo-SP
- Proprietário: João Silva
```

### Ler arquivo específico

```
Lê o conteúdo do arquivo C:\Users\huugo\topdemais\ativo-real\package.json
```

### Listar projetos existentes

```
Lista todos os projetos cadastrados no Cosmos DB
```

---

## 📚 Próximos Passos

### 1. Expandir Ferramentas

Adicionar mais tools aos servidores:
- `delete_project`
- `update_project`
- `add_neighbor`
- `register_payment`

### 2. Criar MCP Azure

Para gerenciar recursos do Azure:
- Listar resources
- Ver logs do Static Web App
- Escalar Azure Functions

### 3. Dashboard Web

Interface web para:
- Monitorar servidores MCP
- Ver logs em tempo real
- Gerenciar configurações

---

## ❓ Dúvidas Comuns

**P: Posso usar sem Cosmos DB?**
R: Sim! Comente o servidor `ativo-real-cosmosdb` no config.json e use apenas o filesystem.

**P: É seguro colocar a chave no config.json?**
R: Para desenvolvimento local, sim. Para produção, use Azure Key Vault ou variáveis de ambiente do sistema.

**P: Funciona no VS Code?**
R: Não! MCP é exclusivo do Claude Desktop. No VS Code, use GitHub Copilot ou Azure AI Toolkit.

**P: Posso criar meus próprios MCPs?**
R: Sim! Basta seguir a estrutura dos servers em `mcp-servers/src/`. A documentação oficial está em: https://modelcontextprotocol.io

---

## 🆘 Suporte

Se tiver problemas:

1. Veja os logs do Claude Desktop:
   - Windows: `%APPDATA%\Claude\logs\`
   - macOS: `~/Library/Logs/Claude/`

2. Teste o servidor diretamente:
   ```bash
   cd C:\Users\huugo\topdemais\mcp-servers
   node dist/filesystem-server.js
   ```

3. Verifique versões:
   ```bash
   node --version  # Requer 18+
   npm --version
   ```

---

**✅ Configuração completa! Agora você tem Claude com superpoderes para o Ativo Real! 🚀**
