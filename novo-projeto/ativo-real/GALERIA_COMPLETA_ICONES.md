# 🎨 Galeria Completa de Ícones Técnicos - Bem Real

## 📊 Inventário Atual (Janeiro 2026)

### Resumo Executivo
- **Total de Ícones:** 39 únicos
- **Variações de Tamanho:** 24px (35), 32px (3), 16px (1)
- **Design System:** Bronze Fosco #CD7F32, Stroke 2px, Round Caps/Joins
- **Status:** ✅ Biblioteca completa e em produção

---

## 📂 Estrutura de Diretórios

```
src/assets/icons/topography/
├── 16px/
│   └── link-invite.svg          (Convites de compartilhamento)
├── 24px/
│   ├── Navigation & Tools (9)
│   ├── Drawing & Editing (7)
│   ├── Layers & Data (6)
│   ├── Export & Import (5)
│   ├── Management (4)
│   ├── AI & Chat (4)
│   └── Totals: 35 ícones
└── 32px/
    ├── ai-bot.svg               (Chatbot AI - versão CTA)
    ├── gps-center.svg           (GPS - versão CTA)
    └── new-project.svg          (Novo Projeto - versão CTA)
```

---

## 🗂️ Ícones por Categoria

### 1. 🧭 Navegação & Ferramentas (9 ícones)

#### pan-hand.svg (24px)
**Uso:** Ferramenta de navegação "Pan" (mover mapa)
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M9 12V5C9 4.44772 9.44772 4 10 4C10.5523 4 11 4.44772 11 5V12M11 12V7C11 6.44772 11.4477 6 12 6C12.5523 6 13 6.44772 13 7V12M13 12V8C13 7.44772 13.4477 7 14 7C14.5523 7 15 7.44772 15 8V12M15 12V10C15 9.44772 15.4477 9 16 9C16.5523 9 17 9.44772 17 10V14C17 16.7614 14.7614 19 12 19H11C8.23858 19 6 16.7614 6 14V10C6 9.44772 6.44772 9 7 9C7.55228 9 8 9.44772 8 10V12" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### gps-center.svg (24px + 32px)
**Uso:** Centralizar mapa na localização GPS
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="3" stroke="#CD7F32" stroke-width="2"/>
  <path d="M12 2V6M12 18V22M22 12H18M6 12H2" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <circle cx="12" cy="12" r="8" stroke="#CD7F32" stroke-width="2"/>
</svg>
```

#### total-station.svg (24px)
**Uso:** Ferramenta de medição/régua
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M3 21L21 3M3 21H7M3 21V17M21 3H17M21 3V7" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M8 16L16 8" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <circle cx="8" cy="16" r="1.5" fill="#CD7F32"/>
  <circle cx="16" cy="8" r="1.5" fill="#CD7F32"/>
</svg>
```

#### azimuth-arc.svg (24px)
**Uso:** Ferramenta de azimute/direção
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="9" stroke="#CD7F32" stroke-width="2"/>
  <path d="M12 3V12L18 16" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M12 12L15.8 8.2" stroke="#CD7F32" stroke-width="1.5" stroke-linecap="round"/>
</svg>
```

#### undo.svg (24px)
**Uso:** Desfazer última ação
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M9 14L4 9L9 4" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M4 9H15C17.7614 9 20 11.2386 20 14V14C20 16.7614 17.7614 19 15 19H13" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### redo.svg (24px)
**Uso:** Refazer ação desfeita
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M15 14L20 9L15 4" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M20 9H9C6.23858 9 4 11.2386 4 14V14C4 16.7614 6.23858 19 9 19H11" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### history.svg (24px)
**Uso:** Histórico de versões
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="9" stroke="#CD7F32" stroke-width="2"/>
  <path d="M12 7V12L15 15" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M3 12H6" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

#### input-xy.svg (24px)
**Uso:** Entrada manual de coordenadas X,Y
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M4 4V20M4 20H20" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="10" cy="10" r="2" fill="#CD7F32"/>
  <circle cx="16" cy="8" r="2" fill="#CD7F32"/>
  <circle cx="14" cy="16" r="2" fill="#CD7F32"/>
  <path d="M9 3L11 7M11 7L13 3M11 7V11" stroke="#CD7F32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M18 15L20 17M20 15L18 17" stroke="#CD7F32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### clear-map.svg (24px)
**Uso:** Limpar todos os desenhos do mapa
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M3 6H21M19 6L18 20C18 21.1046 17.1046 22 16 22H8C6.89543 22 6 21.1046 6 20L5 6" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M8 6V4C8 2.89543 8.89543 2 10 2H14C15.1046 2 16 2.89543 16 4V6" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M10 11V17M14 11V17" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

---

### 2. ✏️ Desenho & Edição (7 ícones)

#### draw-polygon.svg (24px)
**Uso:** Ferramenta de desenho de polígonos
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M12 4L20 8V16L12 20L4 16V8L12 4Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="12" cy="4" r="1.5" fill="#CD7F32"/>
  <circle cx="20" cy="8" r="1.5" fill="#CD7F32"/>
  <circle cx="20" cy="16" r="1.5" fill="#CD7F32"/>
  <circle cx="12" cy="20" r="1.5" fill="#CD7F32"/>
  <circle cx="4" cy="16" r="1.5" fill="#CD7F32"/>
  <circle cx="4" cy="8" r="1.5" fill="#CD7F32"/>
</svg>
```

#### edit-vertices.svg (24px)
**Uso:** Editar vértices de polígonos
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M11 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20H18C19.1046 20 20 19.1046 20 18V13" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M14 6L18 10M20 4L18 6L14 10L12 11L13 9L17 5L20 4Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="12" cy="11" r="1.5" fill="#CD7F32"/>
</svg>
```

#### eraser.svg (24px)
**Uso:** Borracha para apagar elementos
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M13 5L19 11L11 19L5 13L13 5Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M8.5 16.5L11 19H20" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M9 11L13 15" stroke="#CD7F32" stroke-width="1.5" stroke-linecap="round"/>
</svg>
```

#### rotate-feature.svg (24px)
**Uso:** Rotacionar elementos selecionados
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C14.3932 3 16.5659 3.94957 18.1652 5.5" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M18 2V6H14" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### scale-feature.svg (24px)
**Uso:** Redimensionar elementos
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <rect x="4" y="4" width="16" height="16" stroke="#CD7F32" stroke-width="2"/>
  <path d="M4 4L9 9M20 20L15 15" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <circle cx="4" cy="4" r="2" fill="#CD7F32"/>
  <circle cx="20" cy="20" r="2" fill="#CD7F32"/>
</svg>
```

#### mirror-feature.svg (24px)
**Uso:** Espelhar elementos
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M12 3V21" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M7 7V17L3 12L7 7Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M17 7V17L21 12L17 7Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### client-pin.svg (24px)
**Uso:** Marcar localização de cliente
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M12 2C8.13401 2 5 5.13401 5 9C5 13.25 12 22 12 22C12 22 19 13.25 19 9C19 5.13401 15.866 2 12 2Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="12" cy="9" r="3" stroke="#CD7F32" stroke-width="2"/>
</svg>
```

---

### 3. 📑 Layers & Dados Oficiais (6 ícones)

#### sigef-parcel.svg (24px)
**Uso:** Layer SIGEF (parcelas)
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <rect x="4" y="4" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
  <rect x="13" y="4" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
  <rect x="4" y="13" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
  <rect x="13" y="13" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
</svg>
```

#### incra-land.svg (24px)
**Uso:** Layer INCRA (terras)
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M3 20L12 4L21 20H3Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M8 14H16" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <circle cx="12" cy="11" r="2" stroke="#CD7F32" stroke-width="2"/>
</svg>
```

#### car-env.svg (24px)
**Uso:** Layer CAR (ambiental)
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#CD7F32" stroke-width="2"/>
  <path d="M12 2C14 6 14 18 12 22M12 2C10 6 10 18 12 22" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M2 12H22" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

#### stats-poly.svg (24px)
**Uso:** Estatísticas de polígonos
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <rect x="4" y="14" width="4" height="6" stroke="#CD7F32" stroke-width="2"/>
  <rect x="10" y="10" width="4" height="10" stroke="#CD7F32" stroke-width="2"/>
  <rect x="16" y="6" width="4" height="14" stroke="#CD7F32" stroke-width="2"/>
  <path d="M4 14L10 10L16 6" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### sync-dashboard.svg (24px)
**Uso:** Sincronizar com dashboard
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C14.8273 3 17.35 4.28843 19 6.31381" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M21 3V7H17" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### save-draft.svg (24px)
**Uso:** Salvar rascunho
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16L21 8V19C21 20.1046 20.1046 21 19 21Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M17 21V13H7V21M7 3V8H15" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

### 4. 📤 Exportação & Importação (5 ícones)

#### export-pdf.svg (24px)
**Uso:** Exportar laudo oficial em PDF
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M7 3H17L21 7V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V7L7 3Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M7 3V7H3" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M12 11V17M12 17L9 14M12 17L15 14" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="12" y="9" font-family="monospace" font-size="4" font-weight="bold" fill="#CD7F32" text-anchor="middle">PDF</text>
</svg>
```

#### export-kml.svg (24px)
**Uso:** Exportar para Google Earth/QGIS
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M7 3H17L21 7V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V7L7 3Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M7 3V7H3" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M12 11V17M12 17L9 14M12 17L15 14" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="12" y="9" font-family="monospace" font-size="4" font-weight="bold" fill="#CD7F32" text-anchor="middle">KML</text>
</svg>
```

#### export-json.svg (24px)
**Uso:** Exportar para APIs/Web GIS
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M7 3H17L21 7V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V7L7 3Z" stroke="#B0B0B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M7 3V7H3" stroke="#B0B0B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M12 11V17M12 17L9 14M12 17L15 14" stroke="#B0B0B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="12" y="9" font-family="monospace" font-size="3.5" font-weight="bold" fill="#B0B0B0" text-anchor="middle">JSON</text>
</svg>
```

#### file-kml.svg (24px)
**Uso:** Importar arquivo KML
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M13 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V9L13 2Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M13 2V9H20" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="12" y="16" font-family="monospace" font-size="5" font-weight="bold" fill="#CD7F32" text-anchor="middle">KML</text>
</svg>
```

#### file-json.svg (24px)
**Uso:** Importar arquivo JSON/GeoJSON
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M13 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V9L13 2Z" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M13 2V9H20" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="12" y="16" font-family="monospace" font-size="4.5" font-weight="bold" fill="#CD7F32" text-anchor="middle">JSON</text>
</svg>
```

---

### 5. 🎛️ Gestão & Dashboard (4 ícones)

#### manage-panel.svg (24px)
**Uso:** Painel de gestão
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <rect x="3" y="3" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
  <rect x="14" y="3" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
  <rect x="3" y="14" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
  <rect x="14" y="14" width="7" height="7" stroke="#CD7F32" stroke-width="2"/>
  <circle cx="6.5" cy="6.5" r="1" fill="#CD7F32"/>
  <circle cx="17.5" cy="6.5" r="1" fill="#CD7F32"/>
  <circle cx="6.5" cy="17.5" r="1" fill="#CD7F32"/>
  <circle cx="17.5" cy="17.5" r="1" fill="#CD7F32"/>
</svg>
```

#### dash-projects.svg (24px)
**Uso:** Tab de projetos no dashboard
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M9 2H5C3.89543 2 3 2.89543 3 4V8C3 9.10457 3.89543 10 5 10H9C10.1046 10 11 9.10457 11 8V4C11 2.89543 10.1046 2 9 2Z" stroke="#CD7F32" stroke-width="2"/>
  <path d="M19 2H15C13.8954 2 13 2.89543 13 4V8C13 9.10457 13.8954 10 15 10H19C20.1046 10 21 9.10457 21 8V4C21 2.89543 20.1046 2 19 2Z" stroke="#CD7F32" stroke-width="2"/>
  <path d="M9 14H5C3.89543 14 3 14.8954 3 16V20C3 21.1046 3.89543 22 5 22H9C10.1046 22 11 21.1046 11 20V16C11 14.8954 10.1046 14 9 14Z" stroke="#CD7F32" stroke-width="2"/>
  <path d="M19 14H15C13.8954 14 13 14.8954 13 16V20C13 21.1046 13.8954 22 15 22H19C20.1046 22 21 21.1046 21 20V16C21 14.8954 20.1046 14 19 14Z" stroke="#CD7F32" stroke-width="2"/>
</svg>
```

#### dash-finance.svg (24px)
**Uso:** Tab financeiro no dashboard
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="9" stroke="#CD7F32" stroke-width="2"/>
  <path d="M12 6V12L16 14" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M9 2H15" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

#### new-project.svg (32px)
**Uso:** Criar novo projeto (CTA button)
```svg
<svg width="32" height="32" viewBox="0 0 32 32" fill="none">
  <rect x="6" y="6" width="20" height="20" rx="2" stroke="#CD7F32" stroke-width="2"/>
  <path d="M16 11V21M11 16H21" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

---

### 6. 💰 Pagamentos & Financeiro (1 ícone)

#### payment-receive.svg (24px)
**Uso:** Botão de receber pagamento
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <rect x="2" y="6" width="20" height="14" rx="2" stroke="#CD7F32" stroke-width="2"/>
  <path d="M2 10H22" stroke="#CD7F32" stroke-width="2"/>
  <circle cx="7" cy="15" r="1.5" fill="#CD7F32"/>
  <path d="M12 15H18" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

---

### 7. 🤖 AI & Chatbot (4 ícones)

#### ai-bot.svg (24px + 32px)
**Uso:** Assistente técnico AI
```svg
<!-- 32px version -->
<svg width="32" height="32" viewBox="0 0 32 32" fill="none">
  <rect x="6" y="10" width="20" height="14" rx="2" stroke="#CD7F32" stroke-width="2"/>
  <circle cx="11" cy="17" r="1.5" fill="#CD7F32"/>
  <circle cx="21" cy="17" r="1.5" fill="#CD7F32"/>
  <path d="M16 6V10" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M13 6H19" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
  <path d="M8 24V26C8 27.1046 8.89543 28 10 28H22C23.1046 28 24 27.1046 24 26V24" stroke="#CD7F32" stroke-width="2" stroke-linecap="round"/>
</svg>
```

#### clear-chat.svg (24px)
**Uso:** Limpar histórico de chat
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M4 6H20M10 11V17M14 11V17M5 6L6 19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19L19 6M9 6V4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V6" stroke="#B0B0B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### send-message.svg (24px)
**Uso:** Enviar mensagem no chat
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### close-x.svg (24px)
**Uso:** Fechar modal/chat
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M18 6L6 18M6 6L18 18" stroke="#B0B0B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

### 8. 🔗 Compartilhamento (2 ícones)

#### link-invite.svg (16px)
**Uso:** Link de convite (pequeno, para UI densa)
```svg
<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
  <path d="M7 9L9 7M11 5L9 7M9 7L7 9M7 9L5 11" stroke="#CD7F32" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M11 3L13 5L11 7M5 9L3 11L5 13" stroke="#CD7F32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

#### logout.svg (24px)
**Uso:** Botão de logout
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M9 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H9" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M16 17L21 12M21 12L16 7M21 12H9" stroke="#CD7F32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

## 🎨 Design System - Especificações Técnicas

### Padrões Visuais
```css
/* Cores Primárias */
--bronze-fosco: #CD7F32;      /* Ícones principais */
--titanio-metalico: #B0B0B0;  /* Ícones secundários */
--azul-marinho: #001F3F;      /* Fundo padrão */

/* Estados Interativos */
--bronze-hover: #FFD700;      /* Hover state (gold) */
--gray-inactive: #A0A0A0;     /* Inactive state */
--dark-disabled: #4A4A4A;     /* Disabled state */

/* Linha e Traço */
stroke-width: 2px;            /* Peso padrão */
stroke-linecap: round;        /* Pontas arredondadas */
stroke-linejoin: round;       /* Junções arredondadas */
```

### Dimensões e Grid
```
Grid Base: 24x24px
Padding Interno: 2px (área segura)
ViewBox: "0 0 24 24" (padrão)
         "0 0 32 32" (CTA buttons)
         "0 0 16 16" (small UI)
```

### Exportação
```bash
# Otimização com SVGO
svgo --multipass --pretty --indent=2 input.svg -o output.svg

# Tamanhos de exportação
24px: Uso padrão em toolbars
32px: CTAs e botões destacados
16px: UI densa (favicons, small icons)
```

---

## 📊 Estatísticas de Uso

### Ícones Implementados (Janeiro 2026)
```
GlobalMap.tsx:           13 ícones ✅
DashboardTopografo.tsx:   5 ícones ✅
AIBotChat.tsx:            4 ícones ✅

Total Implementado:      22 ícones (56%)
Total Disponível:        39 ícones únicos
Total Pendente:          17 ícones (44%)
```

### Ícones Prontos Não Implementados
```
✓ undo, redo (edição)
✓ stats-poly (análise)
✓ history (versionamento)
✓ clear-map (limpeza)
✓ logout (autenticação)
✓ input-xy (coordenadas manuais)
✓ client-pin (marcação)
✓ azimuth-arc (direção)
✓ export-pdf, export-kml, export-json (relatórios)
```

---

## 🚀 Próximos Passos

### Curto Prazo
1. ✅ Implementar ícones de exportação no relatório técnico
2. ⏳ Adicionar undo/redo na toolbar de edição
3. ⏳ Integrar stats-poly no painel de análise
4. ⏳ Implementar logout no dashboard header

### Médio Prazo
1. Criar versões animadas (loading states)
2. Implementar icon sprite sheet (performance)
3. Adicionar variações de cor (temas claros/escuros)
4. Documentar accessibility (ARIA labels)

### Longo Prazo
1. Expandir biblioteca para 100+ ícones
2. Criar ferramenta de customização online
3. Publicar como pacote NPM (@bemreal/icons)
4. Desenvolver plugin Figma/Sketch

---

## 📚 Referências

### Ferramentas Utilizadas
- **Design:** Figma, Adobe Illustrator
- **Otimização:** SVGO, SVGOMG
- **Integração:** vite-plugin-svgr
- **Testing:** Storybook (planejado)

### Padrões Seguidos
- [Material Design Icons Guidelines](https://material.io/design/iconography)
- [Feather Icons](https://feathericons.com/) - Inspiração de estilo
- [Heroicons](https://heroicons.com/) - Referência de traços
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/) - Acessibilidade

---

**Versão:** 1.0.0  
**Data:** 22 de Janeiro de 2026  
**Licença:** Proprietária - Bem Real © 2026  
**Contato:** design@bemreal.com.br
