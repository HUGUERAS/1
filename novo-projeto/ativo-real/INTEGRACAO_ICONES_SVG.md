# 🎨 Guia de Integração - Ícones Topográficos BEM REAL (React + Vite)

## ✅ Configuração Inicial Completa

### 1. Plugin Instalado
```bash
✓ vite-plugin-svgr instalado
```

### 2. Vite Configurado
- SVGs importados como componentes React
- TypeScript habilitado
- Acessibilidade (role="img") automática

### 3. Componente TopoIcon Criado
- Localização: `src/components/ui/TopoIcon.tsx`
- Cores automáticas: Bronze (#CD7F32) ativo / Cinza (#A0A0A0) inativo
- Tamanhos: 16px, 24px, 32px

---

## 📂 Estrutura de Diretórios

```
src/assets/icons/topography/
├── 16px/          # Labels secundários, elementos densos
├── 24px/          # Tamanho PADRÃO (barras de ferramentas)
└── 32px/          # Ações principais, modais, destaque
```

**Adicione seus 15 arquivos SVG** nesta estrutura, exemplo:
```
24px/
├── measure.svg
├── gps.svg
├── layers.svg
├── import.svg
├── export.svg
├── rotate.svg
├── scale.svg
├── mirror-x.svg
├── mirror-y.svg
├── snapshot.svg
├── undo.svg
├── redo.svg
├── topographer.svg
├── ruler.svg
└── reference.svg
```

---

## 🔧 Como Usar nos Componentes

### Exemplo 1: Substituir Emoji Simples

**Antes:**
```tsx
<button style={menuBtnStyle(false)} onClick={handleGPS}>
  📍 GPS
</button>
```

**Depois:**
```tsx
import GpsIcon from '../assets/icons/topography/24px/gps.svg?react';
import TopoIcon from '../components/ui/TopoIcon';

<button style={menuBtnStyle(false)} onClick={handleGPS}>
  <TopoIcon Icon={GpsIcon} size={24} isActive={true} ariaLabel="GPS" />
  GPS
</button>
```

### Exemplo 2: Ícone com Estado Dinâmico

```tsx
import LayersIcon from '../assets/icons/topography/24px/layers.svg?react';

<button 
  style={menuBtnStyle(showGovernmentLayers)} 
  onClick={toggleGovernmentLayers}
>
  <TopoIcon 
    Icon={LayersIcon} 
    size={24} 
    isActive={showGovernmentLayers} 
    ariaLabel="Layers Governamentais"
  />
  Layers Governamentais
</button>
```

### Exemplo 3: Cor Customizada

```tsx
import ImportIcon from '../assets/icons/topography/24px/import.svg?react';

<button 
  style={{
    ...menuBtnStyle(false),
    background: '#FFF9E6',
    borderLeft: '4px solid #FFC107'
  }}
>
  <TopoIcon 
    Icon={ImportIcon} 
    size={24} 
    color="#FFC107" // Amarelo customizado
    ariaLabel="Importar Referência"
  />
  Importar Referência
</button>
```

---

## 🗺️ Mapeamento Sugerido de Ícones

### GlobalMap.tsx

| Botão Atual | Emoji | SVG Recomendado | Arquivo Esperado |
|-------------|-------|-----------------|------------------|
| **GPS** | 📍 | Manter ou ícone de localização | `gps.svg` |
| **Medições** | 📏 | Caliper técnico | `measure.svg` |
| **Layers de Base** | 📑 | Pilha de camadas | `layers.svg` |
| **Importar** | 📥 | Seta para baixo | `import.svg` |
| **Exportar** | 📤 | Seta para cima | `export.svg` |
| **Espelhar X** | ↔️ | Espelhamento horizontal | `mirror-x.svg` |
| **Espelhar Y** | ↕️ | Espelhamento vertical | `mirror-y.svg` |
| **Rotacionar** | 🔄 | Rotação circular | `rotate.svg` |
| **Escala** | 📐 | Ferramenta escala | `scale.svg` |
| **Desfazer** | ↩️ | Seta voltar | `undo.svg` |
| **Refazer** | ↪️ | Seta avançar | `redo.svg` |
| **Snapshot** | 📸 | Câmera/versão | `snapshot.svg` |
| **Referência** | 🟡 | Borda tracejada | `reference.svg` |
| **Régua** | 📏 | Régua técnica | `ruler.svg` |
| **Topógrafo** | 📐 | Estação Total | `topographer.svg` |

### DashboardTopografo.tsx

| Botão Atual | Emoji | SVG Recomendado |
|-------------|-------|-----------------|
| **Gestão** | ⚙️ | Engrenagem (manter?) |
| **Receber** | 💰 | Ícone de dinheiro |

---

## 🎨 Regras de Cores

### Padrão Automático (via `isActive`)
```tsx
isActive={true}  → #CD7F32 (Bronze Fosco)
isActive={false} → #A0A0A0 (Cinza Inativo)
```

### Cores Customizadas
Use a prop `color` para casos especiais:
```tsx
color="#FFC107" // Amarelo (Referência)
color="#D9534F" // Vermelho (Limpar Tudo)
color="#002B49" // Azul Escuro (Ações principais)
```

---

## ⚡ Otimizações de Performance

### 1. Importação Dinâmica (Para Muitos Ícones)
```tsx
// Crie um index.ts com todos os ícones
export { default as GpsIcon } from './24px/gps.svg?react';
export { default as LayersIcon } from './24px/layers.svg?react';
// ... todos os 15 ícones

// Importe de uma vez
import * as TopoIcons from '../assets/icons/topography';
```

### 2. CSS para Hover (Performance Melhor)
```css
/* GlobalMap.css */
.tool-button svg {
  stroke: var(--icon-color, #A0A0A0);
  transition: stroke 0.2s ease-in-out;
}

.tool-button:hover svg,
.tool-button.active svg {
  --icon-color: #CD7F32;
}
```

### 3. Memoização (Para Ícones Complexos)
```tsx
import { memo } from 'react';

const TopoIcon = memo<TopoIconProps>(({ Icon, size, isActive, color, className, ariaLabel }) => {
  // ... código existente
});
```

---

## 📝 Checklist de Implementação

### Fase 1: Preparação (✅ COMPLETA)
- [x] Instalar `vite-plugin-svgr`
- [x] Configurar `vite.config.ts`
- [x] Criar componente `TopoIcon`
- [x] Criar estrutura de pastas

### Fase 2: Adicionar SVGs (⏳ AGUARDANDO SEUS ARQUIVOS)
- [ ] Copiar seus 15 SVGs para `src/assets/icons/topography/24px/`
- [ ] Opcionalmente adicionar versões 16px e 32px
- [ ] Validar viewBox correto em cada SVG

### Fase 3: Substituir Emojis no GlobalMap.tsx
- [ ] Importar todos os SVGs no topo do arquivo
- [ ] Substituir ~15 botões com emojis
- [ ] Testar estados ativos/inativos
- [ ] Ajustar espaçamentos se necessário

### Fase 4: Substituir Emojis no DashboardTopografo.tsx
- [ ] Importar SVGs necessários
- [ ] Substituir botões "Gestão" e "Receber"

### Fase 5: Testes e Deploy
- [ ] `npm run dev` - Testar localmente
- [ ] Verificar cores em hover/active
- [ ] Testar responsividade (mobile)
- [ ] `npm run build` - Build de produção
- [ ] `swa deploy` - Deploy Azure

---

## 🚀 Script de Migração Automática (Após Adicionar SVGs)

Quando seus SVGs estiverem prontos, posso executar uma migração automática com este padrão:

```tsx
// Mapeamento automático
const iconMap = {
  '📍': GpsIcon,
  '📏': MeasureIcon,
  '📑': LayersIcon,
  '📥': ImportIcon,
  '📤': ExportIcon,
  // ... todos os 15
};

// Replace automático
emoji → <TopoIcon Icon={iconMap[emoji]} size={24} />
```

---

## 💡 Dica Final

**Teste incremental**: Substitua 1-2 ícones primeiro, verifique no navegador, e então prossiga com o resto. Isso evita erros em lote.

---

## 🔗 Referências

- [vite-plugin-svgr](https://www.npmjs.com/package/vite-plugin-svgr)
- [React ARIA](https://react-spectrum.adobe.com/react-aria/) - Acessibilidade
- Cores BEM REAL: Bronze #CD7F32, Cinza #A0A0A0, Amarelo #FFC107
