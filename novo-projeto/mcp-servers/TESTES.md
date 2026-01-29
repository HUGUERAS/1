# 🧪 Testes para MCP Ativo Real

Execute estes testes no **Claude Desktop** após configurar os servidores.

---

## ✅ Teste 1: MCP Filesystem - Listar arquivos

**Comando:**
```
Claude, lista os arquivos TypeScript na pasta:
C:\Users\huugo\topdemais\ativo-real\src
```

**Resultado esperado:**
Claude usa `list_files` e retorna:
- App.tsx
- DashboardTopografo.tsx
- GlobalMap.tsx
- main.tsx
- index.css
- ...

---

## ✅ Teste 2: MCP Filesystem - Ler arquivo

**Comando:**
```
Lê o conteúdo do arquivo:
C:\Users\huugo\topdemais\ativo-real\package.json
```

**Resultado esperado:**
Claude usa `read_file` e mostra o package.json completo.

---

## ✅ Teste 3: MCP Cosmos DB - Criar projeto

**Comando:**
```
Cria um projeto no Cosmos DB:
- Título: Fazenda Boa Vista
- Local: Ribeirão Preto-SP
- Proprietário: Carlos Mendes
```

**Resultado esperado:**
Claude usa `create_project` e retorna:
```json
{
  "success": true,
  "id": "proj_1737560234567",
  "titulo": "Fazenda Boa Vista"
}
```

---

## ✅ Teste 4: MCP Cosmos DB - Listar projetos

**Comando:**
```
Lista todos os projetos cadastrados no Cosmos DB
```

**Resultado esperado:**
Claude usa `list_projects` e mostra array com todos os projetos.

---

## ✅ Teste 5: MCP Filesystem - Salvar arquivo

**Comando:**
```
Cria um arquivo teste.txt em C:\Users\huugo\Desktop com o texto "MCP funcionando!"
```

**Resultado esperado:**
Claude usa `write_file` e confirma criação do arquivo.

---

## 🔍 Verificando se MCP está ativo

1. Abra Claude Desktop
2. Aguarde 10 segundos (inicialização dos servidores)
3. Na barra inferior, procure ícone de ferramentas
4. Deve mostrar: `ativo-real-filesystem` e `ativo-real-cosmosdb`

---

## 🐛 Debug de Problemas

### Claude não reconhece os comandos

**Solução:** Seja mais explícito:
```
Use a ferramenta list_files para listar C:\Users\huugo
```

### Erro "COSMOS_KEY required"

**Solução:** Edite o config do Claude:
```
C:\Users\huugo\AppData\Roaming\Claude\claude_desktop_config.json
```

Substitua:
```json
"COSMOS_ENDPOINT": "https://seu-account.documents.azure.com:443/"
"COSMOS_KEY": "sua-chave-real-aqui"
```

### Servidor não inicia

**Verificar logs:**
```
C:\Users\huugo\AppData\Roaming\Claude\logs\
```

**Testar manualmente:**
```bash
cd C:\Users\huugo\topdemais\mcp-servers
node dist\filesystem-server.js
```

Deve aparecer: `MCP Filesystem iniciado!`

---

## 📊 Monitoramento

Cada vez que Claude usar uma ferramenta MCP, você verá:

```
🔧 Using tool: list_files
📂 Arguments: { "dirPath": "C:\\Users\\huugo" }
✅ Result: [...files...]
```

---

## 🎯 Testes Avançados

### Criar múltiplos projetos

```
Cria 3 projetos de teste no Cosmos DB:
1. Loteamento Vila Nova - Jundiaí-SP
2. CAR Fazenda São José - Campinas-SP
3. Georreferenciamento Sítio Recanto - Atibaia-SP
```

### Ler e processar múltiplos arquivos

```
Lista todos os arquivos .tsx em ativo-real/src e me diz qual é o maior arquivo
```

### Workflow completo

```
1. Lista os arquivos em ativo-real/src/components
2. Lê o conteúdo de DarkModeToggle.tsx
3. Salva uma cópia em C:\Users\huugo\Desktop\backup-darkmode.txt
```

Claude executará as 3 ferramentas em sequência!

---

**✅ Se todos os testes passarem, seu MCP está 100% funcional! 🚀**
