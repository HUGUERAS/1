# 📊 Especificações: Relatório Técnico de Topografia

## 🎨 Sistema de Design

### Paleta de Cores
```css
/* Cores Principais */
--bronze-fosco: #CD7F32;      /* Ícones ativos, títulos */
--titanio-metalico: #B0B0B0;  /* Ícones secundários */
--azul-marinho: #001F3F;      /* Destaques de seção */
--cinza-grid: #E5E5E5;        /* Linhas de grade (0.5pt) */
```

### Tipografia Técnica
```css
/* Títulos e Cabeçalhos */
font-family: 'Roboto Condensed', 'Inter', sans-serif;
font-weight: 700; /* Bold */
font-size: 14pt;

/* Dados Tabulares (Coordenadas, Azimutes) */
font-family: 'JetBrains Mono', 'Consolas', monospace;
font-size: 10pt;
letter-spacing: 0.5px; /* Legibilidade em números */
```

### Grid de Impressão
- **Layout**: 12 colunas
- **Margens**: 20mm (padrão A4 técnico)
- **Espaçamento**: 1.5 linha para dados críticos

---

## 📄 Estrutura do Documento

### 1. Cabeçalho Institucional
```
┌─────────────────────────────────────────────┐
│ [Logo Bem Real]    Relatório Técnico       │
│                                             │
│ Projeto: [Nome do Projeto]                 │
│ Responsável: [Nome] - CREA/CFT [Número]   │
│ Data: [DD/MM/AAAA HH:MM]                   │
└─────────────────────────────────────────────┘
```

### 2. Resumo de Área (Destaque Visual)
```
╔═══════════════════════════════════════════╗
║  📐 ÁREA TOTAL: 12.345,67 m² (1,23 ha)   ║
║  📏 PERÍMETRO: 456,78 m                   ║
╚═══════════════════════════════════════════╝
```

### 3. Tabela de Coordenadas (Grid Técnico)
```
┌─────────┬────────────┬────────────┬──────────┐
│ Vértice │   X (E)    │   Y (N)    │   Z (m)  │
├─────────┼────────────┼────────────┼──────────┤
│   V1    │ 234567,890 │ 7654321,12 │  456,78  │
│   V2    │ 234568,901 │ 7654322,23 │  457,89  │
│   V3    │ 234569,012 │ 7654323,34 │  458,90  │
└─────────┴────────────┴────────────┴──────────┘
```
**Formato de Números:**
- Coordenadas: 3 casas decimais (precisão geodésica)
- Altitude: 2 casas decimais

### 4. Dados de Azimute e Distância
```
┌─────────────┬────────────┬──────────────┐
│  Segmento   │  Azimute   │  Distância   │
├─────────────┼────────────┼──────────────┤
│   V1 → V2   │  45°12'34" │   123,45 m   │
│   V2 → V3   │  90°00'00" │   234,56 m   │
│   V3 → V1   │ 225°30'15" │   345,67 m   │
└─────────────┴────────────┴──────────────┘
```

### 5. Análise de Sobreposições (SIGEF/INCRA)
```
┌────────────────┬──────────┬─────────────────┐
│  Base Oficial  │  Status  │   Observação    │
├────────────────┼──────────┼─────────────────┤
│  SIGEF         │  ✅ LIVRE │ Sem conflitos   │
│  INCRA         │  ⚠️ ALERTA│ Verificar lote  │
│  CAR           │  ✅ LIVRE │ Compatível      │
└────────────────┴──────────┴─────────────────┘
```
**Legenda de Status:**
- ✅ LIVRE: Sem conflitos detectados
- ⚠️ ALERTA: Requer verificação manual
- ❌ CONFLITO: Sobreposição confirmada

---

## 🔽 Botões de Exportação (Footer)

### Implementação HTML/React
```tsx
<div className="export-toolbar">
  <button className="export-btn export-pdf">
    <TopoIcon Icon={ExportPdfIcon} size={24} color="#CD7F32" />
    Laudo Oficial (PDF)
  </button>
  
  <button className="export-btn export-kml">
    <TopoIcon Icon={ExportKmlIcon} size={24} color="#CD7F32" />
    Visualização GIS (KML)
  </button>
  
  <button className="export-btn export-json">
    <TopoIcon Icon={ExportJsonIcon} size={24} color="#B0B0B0" />
    GeoJSON
  </button>
</div>
```

### CSS Estilização
```css
.export-toolbar {
  position: sticky;
  bottom: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0) 0%, #FFF 20%);
  padding: 20px;
  display: flex;
  gap: 12px;
  border-top: 2px solid #E5E5E5;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: 2px solid #CD7F32;
  border-radius: 6px;
  background: white;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.export-btn:hover {
  background: #CD7F32;
  color: white;
}

.export-btn:hover svg {
  stroke: white;
}
```

---

## 📊 Formatação de Dados

### Coordenadas UTM (SIRGAS 2000)
```javascript
// Formato: 234567.890 (sem separador de milhar)
function formatCoordinate(value) {
  return value.toFixed(3).replace('.', ','); // BR locale
}
```

### Azimutes
```javascript
// Formato: 45°12'34"
function formatAzimuth(decimalDegrees) {
  const degrees = Math.floor(decimalDegrees);
  const minutes = Math.floor((decimalDegrees - degrees) * 60);
  const seconds = Math.floor(((decimalDegrees - degrees) * 60 - minutes) * 60);
  return `${degrees}°${minutes.toString().padStart(2, '0')}'${seconds.toString().padStart(2, '0')}"`;
}
```

### Áreas
```javascript
// Formato: 12.345,67 m² (1,23 ha)
function formatArea(sqMeters) {
  const hectares = sqMeters / 10000;
  return `${sqMeters.toLocaleString('pt-BR', {minimumFractionDigits: 2})} m² (${hectares.toFixed(2)} ha)`;
}
```

---

## 🎯 Checklist de Conformidade

### Obrigatório (NBR 13.133)
- [ ] Coordenadas em SIRGAS 2000 (EPSG:31983)
- [ ] Azimutes calculados no sentido horário
- [ ] Memorial descritivo completo
- [ ] Assinatura digital ou física do responsável técnico
- [ ] ART/TRT anexada (CREA/CFT)

### Recomendado
- [ ] Logo institucional (alta resolução)
- [ ] QR Code para validação online
- [ ] Histórico de revisões
- [ ] Disclaimer de responsabilidade técnica

---

## 📦 Ícones Criados

1. **export-pdf.svg** (24px)
   - Cor: Bronze Fosco #CD7F32
   - Uso: Exportar laudo oficial em PDF

2. **export-kml.svg** (24px)
   - Cor: Bronze Fosco #CD7F32
   - Uso: Exportar para Google Earth / QGIS

3. **export-json.svg** (24px)
   - Cor: Titânio Metálico #B0B0B0
   - Uso: Exportar para APIs / Web GIS

Todos com stroke 2px, round caps/joins, seguindo padrão técnico BEM REAL.
