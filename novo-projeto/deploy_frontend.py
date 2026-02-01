import os
import subprocess
import json
import sys

def run_command(command, cwd=None, capture_output=True):
    print(f"Executando: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=True, 
            stdout=subprocess.PIPE if capture_output else None, 
            stderr=subprocess.PIPE if capture_output else None,
            text=True
        )
        if capture_output:
            return result.stdout.strip()
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {command}")
        if capture_output:
            print(f"Saída: {e.stdout}")
            print(f"Erro: {e.stderr}")
        sys.exit(1)

def main():
    print("🚀 Iniciando Deploy do Frontend Ativo Real...")
    
    # 1. Obter URL do Backend
    print("\n🔍 Obtendo URL do Backend...")
    try:
        func_host = run_command('az functionapp list --resource-group rg-ativo-real --query "[0].defaultHostName" -o tsv')
        if not func_host:
            print("❌ Backend não encontrado no Resource Group 'rg-ativo-real'. Execute o deploy do backend primeiro.")
            sys.exit(1)
            
        backend_url = f"https://{func_host}/api"
        print(f"✓ Backend encontrado: {backend_url}")
    except Exception:
        print("⚠️ Erro ao buscar backend automaticamente. Usando padrão conhecido.")
        backend_url = "https://ativo-real-backend.azurewebsites.net/api"

    # 2. Atualizar .env.production
    print("\n📝 Configurando variáveis de ambiente...")
    env_path = os.path.join("ativo-real", ".env.production")
    
    env_content = f"""# Configurações de produção - Ativo Real
VITE_API_BASE_URL={backend_url}
"""
    
    with open(env_path, "w") as f:
        f.write(env_content)
    print(f"✓ {env_path} atualizado.")

    # 3. Build do Frontend
    print("\n🏗️ Construindo o Frontend (Build)...")
    frontend_dir = "ativo-real"
    
    print("Instalando dependências...")
    run_command("npm install", cwd=frontend_dir, capture_output=False)
    
    print("Compilando projeto...")
    run_command("npm run build", cwd=frontend_dir, capture_output=False)
    print("✓ Build concluído com sucesso.")

    # 4. Criar/Verificar Static Web App no Azure
    print("\n☁️ Configurando Azure Static Web App...")
    swa_name = "ativo-real-frontend"
    rg_name = "rg-ativo-real"
    
    # Verifica se já existe
    try:
        exists = run_command(f'az staticwebapp show -n {swa_name} -g {rg_name}')
        print(f"✓ Recurso {swa_name} já existe.")
    except:
        print(f"Criando recurso {swa_name}...")
        # Azure SWA Free tier tem regioes limitadas, usando 'eastus2' que é proximo/comum
        run_command(f'az staticwebapp create -n {swa_name} -g {rg_name} --location eastus2 --sku Free')
        
    # 5. Obter Token de Deploy
    print("🔑 Obtendo token de deploy...")
    token = run_command(f'az staticwebapp secrets list -n {swa_name} -g {rg_name} --query "properties.apiKey" -o tsv')
    
    if not token:
        print("❌ Falha ao obter token de deploy.")
        sys.exit(1)

    # 6. Deploy final
    print("\n🚀 Enviando arquivos para o Azure...")
    # swa deploy ./dist --deployment-token <TOKEN> --env production
    # Execute no diretório do frontend
    try:
        run_command(f'swa deploy ./dist --env production --deployment-token {token}', cwd=frontend_dir, capture_output=False)
        print("\n✅ DEPLOY DO FRONTEND CONCLUÍDO!")
        
        # Obter URL final
        swa_url = run_command(f'az staticwebapp show -n {swa_name} -g {rg_name} --query "defaultHostname" -o tsv')
        print(f"\n🌐 ACESSE SEU SISTEMA AQUI: https://{swa_url}")
        
    except Exception as e:
        print(f"❌ Erro no deploy SWA: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
