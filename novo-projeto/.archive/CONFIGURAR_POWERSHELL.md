# 🔧 CONFIGURAR POWERSHELL 7+ APÓS INSTALAÇÃO

## ✅ VOCÊ JÁ INSTALOU? ÓTIMO!

Agora precisa fazer o PowerShell funcionar:

---

## 🚀 OPÇÃO 1: REINICIAR E TESTAR (MAIS SIMPLES)

### **1. Feche TODOS os terminais abertos**
- Feche CMD
- Feche PowerShell
- Feche VS Code (se aberto)

### **2. Abra um NOVO terminal:**

**Via Menu Iniciar:**
1. Pressione `Win`
2. Digite: `PowerShell`
3. Você verá 2 opções:
   - ❌ **Windows PowerShell** (versão antiga - NÃO use)
   - ✅ **PowerShell** (versão 7+ - USE ESSA!)

### **3. Teste se funcionou:**

```powershell
pwsh --version
```

**Deve mostrar:** `PowerShell 7.x.x`

---

## 🚀 OPÇÃO 2: VERIFICAR INSTALAÇÃO

### **1. Verificar se PowerShell 7 está instalado:**

Abra CMD e execute:

```cmd
dir "C:\Program Files\PowerShell"
```

**Deve mostrar:** Uma pasta com número de versão (ex: `7`)

### **2. Testar execução direta:**

```cmd
"C:\Program Files\PowerShell\7\pwsh.exe" --version
```

**Deve mostrar:** `PowerShell 7.x.x`

---

## 🚀 OPÇÃO 3: ADICIONAR AO PATH (SE NÃO FUNCIONOU)

### **1. Abrir Variáveis de Ambiente:**

1. Pressione `Win + R`
2. Digite: `sysdm.cpl`
3. Enter
4. Aba: **Avançado**
5. Botão: **Variáveis de Ambiente**

### **2. Editar PATH:**

1. Em "Variáveis do sistema"
2. Selecione: **Path**
3. Clique: **Editar**
4. Clique: **Novo**
5. Adicione: `C:\Program Files\PowerShell\7`
6. Clique: **OK** em todas as janelas

### **3. Reiniciar terminal e testar:**

```cmd
pwsh --version
```

---

## 🎯 DEPOIS QUE FUNCIONAR:

### **Teste o deploy novamente:**

```powershell
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
.\deploy_backend.bat
```

---

## ⚠️ SE AINDA NÃO FUNCIONAR:

### **Use o Prompt de Comando (CMD) ao invés:**

Os scripts `.bat` funcionam perfeitamente no **CMD** (não precisam de PowerShell):

```cmd
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
deploy_backend.bat
```

---

## 🔍 VERIFICAR QUAL POWERSHELL VOCÊ TEM:

### **No Menu Iniciar:**

Procure por "PowerShell" e você verá:

1. **Windows PowerShell** 
   - Ícone azul claro
   - Versão 5.x (antiga)
   - ❌ NÃO use para este projeto

2. **PowerShell** (sem "Windows" no nome)
   - Ícone azul escuro/preto
   - Versão 7.x (nova)
   - ✅ USE ESSA!

---

## 📦 SE NÃO INSTALOU AINDA:

### **Download oficial:**

https://aka.ms/powershell-release?tag=stable

**OU via winget (se tiver):**

```cmd
winget install Microsoft.PowerShell
```

**OU via Microsoft Store:**

1. Abra Microsoft Store
2. Busque: "PowerShell"
3. Instale: **PowerShell** (não o "Windows PowerShell")

---

## ✅ RESUMO RÁPIDO:

1. ✅ Instalar PowerShell 7 (você já fez)
2. ✅ Fechar TODOS os terminais
3. ✅ Abrir NOVO PowerShell 7
4. ✅ Testar: `pwsh --version`
5. ✅ Executar deploy

---

## 💡 ALTERNATIVA: USE CMD!

**PowerShell NÃO é obrigatório para deploy!**

Os scripts `.bat` funcionam no **CMD** normal:

```cmd
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
deploy_backend.bat
```

---

**QUAL OPÇÃO VOCÊ PREFERE?**

1. Configurar PowerShell 7 (mais moderno)
2. Usar CMD (mais simples, já funciona)

**Me avise qual você escolheu!** 🚀
