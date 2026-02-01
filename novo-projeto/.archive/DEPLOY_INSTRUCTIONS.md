# Guia de Deployment - Bem Real (Azure Native)

Como o ambiente atual não possui as ferramentas de linha de comando do Azure (`az` CLI e `func` CLI), preparei um script automatizado para você rodar em sua máquina local ou no Azure Cloud Shell.

## Pré-requisitos

1. **Azure CLI**: [Instalar Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
2. **Azure Functions Core Tools**: [Instalar Func Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local)
3. **PowerShell**: (Padrão no Windows, ou pwsh no Linux/Mac)

## Como Deployar

1. Abra o terminal na pasta `novo-projeto`:
   ```powershell
   cd novo-projeto
   ```

2. Execute o script de automação:
   ```powershell
   ./deploy-complete.ps1
   ```

## O que o script faz?

1. **Infraestrutura**:
   - Cria um **Resource Group** (`rg-bemreal-ai1`) no Sul do Brasil.
   - Provisiona um **PostgreSQL Flexible Server** e ativa a extensão **PostGIS** (Essencial para a lógica de validação de lotes).
   - Cria uma **Function App** (Python 3.11) para o Backend.
   - Cria um **Static Web App** (Free Tier) para o Frontend.

2. **Configuração**:
   - Gera uma senha segura para o banco.
   - Configura a Connection String (`DATABASE_URL`) automaticamente na Function App.
   - Configura CORS para permitir que o Frontend fale com o Backend.

3. **Código**:
   - Faz o build do Frontend com a URL correta da API de produção.
   - Publica o código Python para a Azure Function.
   - Faz o deploy dos arquivos estáticos (`dist/`) para o Static Web App.

## Solução de Problemas Comuns

- **Erro "PostGIS"**: Se o script falhar ao ativar o PostGIS, conecte-se ao banco via ferramenta cliente (DBeaver, pgAdmin) e rode:
  ```sql
  CREATE EXTENSION postgis;
  ```
- **Login**: Se o script reclamar de autenticação, rode `az login` antes.
