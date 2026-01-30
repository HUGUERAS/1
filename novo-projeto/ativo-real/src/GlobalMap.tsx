import { useEffect, useRef, useState } from 'react';
import 'ol/ol.css';
import { DarkModeToggle } from './components/DarkModeToggle';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import XYZ from 'ol/source/XYZ';
import OSM from 'ol/source/OSM';
import { fromLonLat, toLonLat } from 'ol/proj';
import { Polygon } from 'ol/geom';
import { Draw, Modify, Snap, Select } from 'ol/interaction';
import { click } from 'ol/events/condition';
import { FullScreen, MousePosition, ScaleLine, defaults as defaultControls } from 'ol/control';
import { getArea, getLength } from 'ol/sphere';
import { unByKey } from 'ol/Observable';
import Overlay from 'ol/Overlay';
import { KML, GeoJSON } from 'ol/format';
import { Circle as CircleStyle, Fill, Stroke, Style, Text } from 'ol/style';
import proj4 from 'proj4';
import { register } from 'ol/proj/proj4';
import shp from 'shpjs';

// Ícones SVG Topográficos
import TopoIcon from './components/ui/TopoIcon';
import GpsCenterIcon from './assets/icons/topography/32px/gps-center.svg?react';
import DrawPolygonIcon from './assets/icons/topography/24px/draw-polygon.svg?react';
import EditVerticesIcon from './assets/icons/topography/24px/edit-vertices.svg?react';
import MeasureIcon from './assets/icons/topography/24px/total-station.svg?react';
import EraserIcon from './assets/icons/topography/24px/eraser.svg?react';
import LayersIcon from './assets/icons/topography/24px/sigef-parcel.svg?react';
import ImportIcon from './assets/icons/topography/24px/payment-receive.svg?react';
import SyncIcon from './assets/icons/topography/24px/sync-dashboard.svg?react';
import PanHandIcon from './assets/icons/topography/24px/pan-hand.svg?react';
import FileKmlIcon from './assets/icons/topography/24px/file-kml.svg?react';
import FileJsonIcon from './assets/icons/topography/24px/file-json.svg?react';
import SaveDraftIcon from './assets/icons/topography/24px/save-draft.svg?react';
// Ícones prontos para uso futuro: undo, redo, stats-poly, history, clear-map

// --- CONFIGURAÇÃO TÉCNICA (SIRGAS 2000) ---
proj4.defs("EPSG:31983", "+proj=utm +zone=23 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");
register(proj4);

// --- ESTILOS DO MAPA (Classificação Visual) ---
const mapStyles = {
  cliente: new Style({
    stroke: new Stroke({ color: '#0044ff', width: 3 }),
    fill: new Fill({ color: 'rgba(0, 68, 255, 0.2)' }),
    text: new Text({ text: 'CLIENTE', font: 'bold 12px sans-serif', fill: new Fill({ color: '#0044ff' }), stroke: new Stroke({ color: 'white', width: 3 }), overflow: true })
  }),
  vizinho: (nome: string) => new Style({
    stroke: new Stroke({ color: '#ff8800', width: 3 }),
    fill: new Fill({ color: 'rgba(255, 136, 0, 0.2)' }),
    text: new Text({ text: nome || 'VIZINHO', font: 'bold 12px sans-serif', fill: new Fill({ color: '#ff8800' }), stroke: new Stroke({ color: 'white', width: 3 }), overflow: true })
  }),
  padrao: new Style({
    stroke: new Stroke({ color: '#ffcc33', width: 2 }),
    fill: new Fill({ color: 'rgba(255, 255, 255, 0.1)' }),
    image: new CircleStyle({ radius: 5, fill: new Fill({ color: '#999' }) })
  })
};

// --- INTERFACE DE PROPS ---
interface GlobalMapProps {
  userProfile: string;
  projetoId: number | null;
  onLogout: () => void;
}

// --- ESTILOS CSS (Interface) ---
const layoutStyle: React.CSSProperties = { 
  display: 'flex', 
  width: '100vw', 
  height: '100vh', 
  overflow: 'hidden', 
  fontFamily: 'Segoe UI, sans-serif',
  background: 'var(--color-background)',
  transition: 'background var(--transition-base)'
};

const sidebarStyle: React.CSSProperties = { 
  width: '280px', 
  background: 'var(--glass-background)',
  backdropFilter: 'var(--glass-blur)',
  border: 'var(--glass-border)',
  boxShadow: 'var(--shadow-2xl)', 
  zIndex: 10, 
  display: 'flex', 
  flexDirection: 'column', 
  padding: 'var(--space-6)',
  overflowY: 'auto',
  maxHeight: '100vh',
  transition: 'all var(--transition-base)'
};

const mapContainerStyle: React.CSSProperties = { flex: 1, position: 'relative' };

const menuBtnStyle = (ativo: boolean, perigo = false): React.CSSProperties => ({
  display: 'flex', 
  alignItems: 'center', 
  gap: 'var(--space-3)', 
  width: '100%', 
  padding: 'var(--space-3) var(--space-4)',
  marginBottom: 'var(--space-2)', 
  border: 'none', 
  borderRadius: 'var(--radius-lg)', 
  cursor: 'pointer', 
  fontSize: 'var(--text-sm)', 
  fontWeight: 'var(--font-medium)',
  background: perigo 
    ? 'rgba(239, 68, 68, 0.1)' 
    : (ativo ? 'var(--gradient-bronze)' : 'transparent'),
  color: perigo 
    ? '#EF4444' 
    : (ativo ? 'white' : 'var(--color-text-primary)'),
  borderLeft: perigo 
    ? '4px solid #EF4444' 
    : (ativo ? '4px solid var(--color-primary)' : '4px solid transparent'),
  boxShadow: ativo ? 'var(--shadow-bronze)' : 'none',
  transition: 'all var(--transition-fast)'
});

const sectionTitleStyle: React.CSSProperties = { 
  fontSize: 'var(--text-xs)', 
  textTransform: 'uppercase', 
  color: 'var(--color-text-secondary)', 
  marginTop: 'var(--space-6)', 
  marginBottom: 'var(--space-3)', 
  letterSpacing: 'var(--tracking-wider)', 
  fontWeight: 'var(--font-bold)' 
};

const GlobalMap: React.FC<GlobalMapProps> = ({ userProfile, projetoId, onLogout }) => {
  // REFS & STATES
  const mapRef = useRef<HTMLDivElement>(null);
  const popupRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const overlayRef = useRef<Overlay | null>(null);
  
  const [map, setMap] = useState<Map | null>(null);
  const [vectorSource] = useState(new VectorSource());
  const [activeTool, setActiveTool] = useState('pan');
  const [medidaAtual, setMedidaAtual] = useState('');
  const [layerMenuOpen, setLayerMenuOpen] = useState(false);
  const [popupData, setPopupData] = useState<any>(null);
  const [importarComoReferencia, setImportarComoReferencia] = useState(false);
  const [painelVizinhosAberto, setPainelVizinhosAberto] = useState(false);
  const [vizinhos, setVizinhos] = useState([
    { id: 1, nome: 'Minha Gleba', status: 'ok', link: null },
    { id: 2, nome: 'Vizinho Norte', status: 'pendente', link: 'https://ativo.pro/c/123' }
  ]);
  const [estatisticasAbertas, setEstatisticasAbertas] = useState(false);
  const [historicoAbertas, setHistoricoAbertas] = useState(false);
  const [notasProjeto, setNotasProjeto] = useState('');
  const [painelPagamentoAberto, setPainelPagamentoAberto] = useState(false);

  // 1. INICIALIZAÇÃO DO MAPA
  useEffect(() => {
    if (!mapRef.current) return;

    // Camadas Base
    const sateliteLayer = new TileLayer({
      source: new XYZ({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attributions: 'Tiles © Esri',
        maxZoom: 19
      }),
      visible: true,
      properties: { title: 'Satélite (Esri)', type: 'base' }
    });

    const ruasLayer = new TileLayer({
      source: new OSM(),
      visible: false,
      properties: { title: 'Ruas (OSM)', type: 'base' }
    });

    // Camada de Desenho (Com estilos inteligentes)
    const desenhoLayer = new VectorLayer({
      source: vectorSource,
      zIndex: 2,
      properties: { title: 'Vetores', type: 'overlay' },
      style: (feature) => {
        const tipo = feature.get('tipo');
        const nome = feature.get('proprietario');
        
        if (tipo === 'cliente') return mapStyles.cliente;
        if (tipo === 'vizinho') return mapStyles.vizinho(nome);
        return mapStyles.padrao;
      }
    });

    // Overlay (Popup)
    const overlay = new Overlay({
      element: popupRef.current || undefined,
      autoPan: true,
    });
    overlayRef.current = overlay;

    // Mapa
    const mapObject = new Map({
      target: mapRef.current,
      layers: [sateliteLayer, ruasLayer, desenhoLayer],
      view: new View({ center: fromLonLat([-47.8822, -15.7942]), zoom: 14 }),
      overlays: [overlay],
      controls: defaultControls().extend([
        new FullScreen(),
        new ScaleLine({ units: 'metric' }),
        new MousePosition({
          projection: 'EPSG:31983',
          coordinateFormat: (c) => c ? `E: ${c[0].toFixed(2)} m | N: ${c[1].toFixed(2)} m` : '',
          target: document.getElementById('mouse-position') || undefined,
        }),
      ]),
    });

    // Evento de Clique (Popup de Classificação)
    mapObject.on('singleclick', (evt) => {
      if (activeTool === 'pan') {
        const feature = mapObject.forEachFeatureAtPixel(evt.pixel, (f) => f);
        if (feature) {
          const props = feature.getProperties();
          const geom = feature.getGeometry();
          const areaHa = props.name || ((geom as any).getArea() / 10000).toFixed(4) + ' ha';
          setPopupData({
            feature: feature,
            area: areaHa,
            proprietario: props.proprietario || '',
            status: props.status || 'Em Análise',
            tipo: props.tipo || 'padrao'
          });
          overlay.setPosition(evt.coordinate);
        } else {
          overlay.setPosition(undefined);
        }
      }
    });

    setMap(mapObject);

    // Auto-Load (Carregar Rascunho)
    const dadosSalvos = localStorage.getItem('rascunho_ativo_real');
    if (dadosSalvos) {
      const features = new GeoJSON().readFeatures(JSON.parse(dadosSalvos), { featureProjection: 'EPSG:3857' });
      if (features.length) vectorSource.addFeatures(features);
    }

    return () => mapObject.setTarget(undefined);
  }, []);

  // 2. AUTO-SAVE
  useEffect(() => {
    if (!vectorSource) return;
    const chaveStorage = projetoId ? `rascunho_projeto_${projetoId}` : 'rascunho_ativo_real';
    const salvar = () => {
      const json = new GeoJSON().writeFeatures(vectorSource.getFeatures(), { featureProjection: 'EPSG:3857' });
      localStorage.setItem(chaveStorage, json);
    };
    vectorSource.on('addfeature', salvar);
    vectorSource.on('changefeature', salvar);
    vectorSource.on('removefeature', salvar);
    vectorSource.on('clear', salvar);
  }, [vectorSource]);

  // 3. GERENCIADOR DE FERRAMENTAS
  useEffect(() => {
    if (!map) return;
    map.getInteractions().forEach((i) => {
      if (i instanceof Draw || i instanceof Modify || i instanceof Snap || i instanceof Select) map.removeInteraction(i);
    });

    let listener: any;

    switch (activeTool) {
      case 'draw':
        const draw = new Draw({ source: vectorSource, type: 'Polygon' });
        draw.on('drawstart', (e) => {
          listener = e.feature.getGeometry()?.on('change', (evt: any) => {
            const area = (getArea(evt.target) / 10000).toFixed(4);
            setMedidaAtual(`Área: ${area} ha`);
          });
        });
        draw.on('drawend', () => { unByKey(listener); setMedidaAtual(''); });
        map.addInteraction(draw);
        map.addInteraction(new Snap({ source: vectorSource }));
        break;

      case 'measure':
        const rule = new Draw({ source: vectorSource, type: 'LineString' });
        rule.on('drawstart', (e) => {
          listener = e.feature.getGeometry()?.on('change', (evt: any) => {
            const len = getLength(evt.target);
            setMedidaAtual(len > 1000 ? `Dist: ${(len/1000).toFixed(3)} km` : `Dist: ${len.toFixed(2)} m`);
          });
        });
        rule.on('drawend', () => { unByKey(listener); });
        map.addInteraction(rule);
        break;

      case 'modify':
        map.addInteraction(new Modify({ source: vectorSource }));
        map.addInteraction(new Snap({ source: vectorSource }));
        break;

      case 'eraser':
        const select = new Select({ condition: click });
        select.on('select', (e) => {
          if (e.selected.length > 0) {
            if (window.confirm('Excluir este item?')) {
              vectorSource.removeFeature(e.selected[0]);
              overlayRef.current?.setPosition(undefined);
            }
            select.getFeatures().clear();
          }
        });
        map.addInteraction(select);
        break;
      default: break;
    }

    return () => { if (listener) unByKey(listener); };
  }, [activeTool, map, vectorSource]);

  // 4. FUNÇÕES AUXILIARES
  const handleGPS = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const coords = fromLonLat([position.coords.longitude, position.coords.latitude]);
          map?.getView().animate({ center: coords, zoom: 18, duration: 1000 });
        },
        () => alert('❌ Erro ao obter localização. Verifique as permissões do navegador.')
      );
    } else {
      alert('❌ GPS não disponível neste navegador.');
    }
  };

  // === FUNÇÕES DE GESTÃO AVANÇADA ===
  
  const calcularEstatisticas = () => {
    const features = vectorSource.getFeatures();
    let areaTotal = 0;
    let clientes = 0, vizinhos = 0, semClassificacao = 0;
    
    features.forEach(f => {
      const geom = f.getGeometry();
      if (geom) areaTotal += (geom as any).getArea() / 10000; // hectares
      
      const tipo = f.get('tipo');
      if (tipo === 'cliente') clientes++;
      else if (tipo === 'vizinho') vizinhos++;
      else semClassificacao++;
    });
    
    return {
      totalLotes: features.length,
      areaTotal: areaTotal.toFixed(2),
      clientes,
      vizinhos,
      semClassificacao
    };
  };

  const verificarSobreposicoes = () => {
    const features = vectorSource.getFeatures();
    const sobreposicoes: string[] = [];
    
    for (let i = 0; i < features.length; i++) {
      for (let j = i + 1; j < features.length; j++) {
        const geom1 = features[i].getGeometry();
        const geom2 = features[j].getGeometry();
        
        if (geom1 && geom2 && (geom1 as any).intersects(geom2)) {
          const nome1 = features[i].get('proprietario') || `Lote ${i + 1}`;
          const nome2 = features[j].get('proprietario') || `Lote ${j + 1}`;
          sobreposicoes.push(`⚠️ ${nome1} × ${nome2}`);
        }
      }
    }
    
    if (sobreposicoes.length > 0) {
      alert(`🚨 Sobreposições Detectadas:\n\n${sobreposicoes.join('\n')}\n\n⚠️ Recomenda-se revisar os limites desses lotes.`);
    } else {
      alert('✅ Nenhuma sobreposição detectada!');
    }
  };

  const salvarVersao = () => {
    const timestamp = new Date().toISOString();
    const data = new GeoJSON().writeFeatures(vectorSource.getFeatures(), { featureProjection: 'EPSG:3857' });
    const chave = projetoId ? `historico_projeto_${projetoId}` : 'historico_ativo_real';
    
    const historico = JSON.parse(localStorage.getItem(chave) || '[]');
    historico.push({ timestamp, data, notas: notasProjeto });
    
    // Manter apenas últimas 10 versões
    if (historico.length > 10) historico.shift();
    
    localStorage.setItem(chave, JSON.stringify(historico));
    alert(`✅ Versão salva: ${new Date(timestamp).toLocaleString('pt-BR')}`);
  };

  const carregarVersao = (index: number) => {
    const chave = projetoId ? `historico_projeto_${projetoId}` : 'historico_ativo_real';
    const historico = JSON.parse(localStorage.getItem(chave) || '[]');
    
    if (historico[index]) {
      const features = new GeoJSON().readFeatures(historico[index].data, { featureProjection: 'EPSG:3857' });
      vectorSource.clear();
      vectorSource.addFeatures(features);
      setNotasProjeto(historico[index].notas || '');
      alert('✅ Versão restaurada!');
    }
  };

  const gerarRelatorio = () => {
    const stats = calcularEstatisticas();
    const features = vectorSource.getFeatures();
    
    let relatorio = `📊 RELATÓRIO DO PROJETO\n`;
    relatorio += `${'='.repeat(50)}\n\n`;
    relatorio += `📍 Total de Lotes: ${stats.totalLotes}\n`;
    relatorio += `📐 Área Total: ${stats.areaTotal} ha\n`;
    relatorio += `🏠 Clientes: ${stats.clientes}\n`;
    relatorio += `🚧 Vizinhos: ${stats.vizinhos}\n`;
    relatorio += `⚪ Sem Classificação: ${stats.semClassificacao}\n\n`;
    
    relatorio += `${'='.repeat(50)}\n`;
    relatorio += `📋 LISTA DE PROPRIETÁRIOS\n`;
    relatorio += `${'='.repeat(50)}\n\n`;
    
    features.forEach((f) => {
      const prop = f.get('proprietario') || 'Sem Nome';
      const tipo = f.get('tipo') || 'padrao';
      const area = ((f.getGeometry() as any).getArea() / 10000).toFixed(4);
      const emoji = tipo === 'cliente' ? '🏠' : tipo === 'vizinho' ? '🚧' : '⚪';
      relatorio += `${emoji} ${prop} - ${area} ha\n`;
    });
    
    if (notasProjeto) {
      relatorio += `\n${'='.repeat(50)}\n`;
      relatorio += `📝 NOTAS DO PROJETO\n`;
      relatorio += `${'='.repeat(50)}\n`;
      relatorio += notasProjeto;
    }
    
    // Download como TXT
    const blob = new Blob([relatorio], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `relatorio_${new Date().toISOString().split('T')[0]}.txt`;
    link.click();
    
    alert('✅ Relatório baixado!');
  };

  const sincronizarComDashboard = () => {
    const chave = 'db_projetos_v2';
    const projetos = JSON.parse(localStorage.getItem(chave) || '[]');
    
    if (projetoId) {
      const projeto = projetos.find((p: any) => p.id === projetoId);
      if (projeto) {
        const stats = calcularEstatisticas();
        projeto.areaTotal = parseFloat(stats.areaTotal);
        projeto.lotes = stats.totalLotes;
        projeto.ultimaAtualizacao = new Date().toISOString();
        
        localStorage.setItem(chave, JSON.stringify(projetos));
        alert('✅ Dados sincronizados com o Dashboard!');
      } else {
        alert('⚠️ Projeto não encontrado no Dashboard.');
      }
    } else {
      alert('⚠️ Este é um rascunho. Crie um projeto no Dashboard primeiro.');
    }
  };

  const registrarPagamento = () => {
    const chave = 'db_projetos_v2';
    const projetos = JSON.parse(localStorage.getItem(chave) || '[]');
    
    if (!projetoId) {
      alert('⚠️ Este é um rascunho. Crie um projeto no Dashboard primeiro.');
      return;
    }
    
    const projeto = projetos.find((p: any) => p.id === projetoId);
    if (!projeto) {
      alert('⚠️ Projeto não encontrado no Dashboard.');
      return;
    }
    
    const valorInput = prompt(`💰 Registrar Pagamento\n\nValor Total: R$ ${projeto.financeiro.valorTotal.toLocaleString()}\nJá Pago: R$ ${projeto.financeiro.valorPago.toLocaleString()}\nRestante: R$ ${(projeto.financeiro.valorTotal - projeto.financeiro.valorPago).toLocaleString()}\n\nDigite o valor recebido:`);
    
    if (!valorInput) return;
    
    const valor = parseFloat(valorInput.replace(',', '.'));
    if (isNaN(valor) || valor <= 0) {
      alert('❌ Valor inválido!');
      return;
    }
    
    const novoPago = projeto.financeiro.valorPago + valor;
    const novoStatus = novoPago >= projeto.financeiro.valorTotal ? 'quitado' : 'parcial';
    
    projeto.financeiro.valorPago = novoPago;
    projeto.financeiro.status = novoStatus;
    projeto.ultimaAtualizacao = new Date().toISOString();
    
    const projetoIndex = projetos.findIndex((p: any) => p.id === projetoId);
    projetos[projetoIndex] = projeto;
    localStorage.setItem(chave, JSON.stringify(projetos));
    
    alert(`✅ Pagamento registrado!\n\nValor: R$ ${valor.toLocaleString('pt-BR', {minimumFractionDigits: 2})}\nTotal Pago: R$ ${novoPago.toLocaleString('pt-BR', {minimumFractionDigits: 2})}\nRestante: R$ ${(projeto.financeiro.valorTotal - novoPago).toLocaleString('pt-BR', {minimumFractionDigits: 2})}\n\n${novoStatus === 'quitado' ? '🎉 Projeto QUITADO!' : '⏳ Pagamento parcial'}`);
  };

  const trocarBase = (titulo: string) => {
    map?.getLayers().forEach(l => {
      if (l.get('type') === 'base') l.setVisible(l.get('title') === titulo);
    });
  };

  const handleClearAll = () => {
    if (window.confirm("ATENÇÃO: Isso apagará TODO o mapa. Continuar?")) {
      vectorSource.clear();
      localStorage.removeItem('rascunho_ativo_real');
      overlayRef.current?.setPosition(undefined);
    }
  };

  const handleExport = (formato: 'KML' | 'JSON') => {
    if(!vectorSource.getFeatures().length) return alert('Mapa vazio!');
    let formatador, ext, mime;
    if(formato === 'KML') { formatador = new KML({extractStyles:true}); ext='kml'; mime='application/vnd.google-earth.kml+xml'; }
    else { formatador = new GeoJSON(); ext='json'; mime='application/json'; }
    
    const data = formatador.writeFeatures(vectorSource.getFeatures(), { dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([data], {type: mime}));
    link.download = `projeto.${ext}`;
    link.click();
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if(!file) return;
    const ext = file.name.split('.').pop()?.toLowerCase();
    
    let features: any[] = [];
    if(ext === 'zip') {
      const ab = await file.arrayBuffer();
      const geojson = await shp(ab);
      features = new GeoJSON().readFeatures(geojson, { featureProjection: 'EPSG:3857' });
    } else {
      const txt = await file.text();
      const format = ext === 'kml' ? new KML({extractStyles:true}) : new GeoJSON();
      features = format.readFeatures(txt, { featureProjection: 'EPSG:3857' });
    }
    
    if(features.length && map) {
      if(importarComoReferencia) {
        // Criar camada de referência visual (linha amarela tracejada)
        const referenciaLayer = new VectorLayer({
          source: new VectorSource({ features }),
          zIndex: 1,
          properties: { title: file.name, type: 'referencia' },
          style: {
            'stroke-color': '#f1c40f',
            'stroke-width': 2,
            'stroke-linedash': [10, 10],
            'fill-color': 'rgba(241, 196, 15, 0.1)'
          } as any
        });
        map.addLayer(referenciaLayer);
        const extent = referenciaLayer.getSource()?.getExtent();
        if(extent) map.getView().fit(extent, {padding:[50,50,50,50]});
        alert('✅ Arquivo importado como referência visual (amarelo tracejado)!');
      } else {
        // Importar normalmente (adiciona ao vectorSource)
        vectorSource.addFeatures(features);
        map.getView().fit(vectorSource.getExtent(), {padding:[50,50,50,50]});
        alert('✅ Arquivo importado com sucesso!');
      }
    }
    e.target.value = '';
    setImportarComoReferencia(false); // Reset
  };

  // 5. RENDERIZAÇÃO (JSX)
  return (
    <div style={layoutStyle}>
      {/* Dark Mode Toggle */}
      <DarkModeToggle />
      
      {/* SIDEBAR */}
      <aside style={sidebarStyle}>
        {/* HEADER COM BOTÃO VOLTAR */}
        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
            <div style={{ width: '24px', height: '24px', background: '#002B49', borderRadius: '4px' }}></div>
            <h2 style={{ margin: 0, color: '#002B49', fontSize: '18px' }}>Ativo Real</h2>
          </div>
          {/* BOTÃO VOLTAR */}
          <button 
            style={{
              width: '100%',
              padding: '10px',
              background: '#E8F4F8',
              border: '1px solid #002B49',
              borderRadius: '6px',
              color: '#002B49',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px'
            }}
            onClick={onLogout}
          >
            ← {userProfile === 'topografo' ? 'Voltar aos Projetos' : 'Voltar ao Menu Principal'}
          </button>
          {userProfile === 'topografo' && (
            <button 
              style={{
                width: '100%',
                padding: '10px',
                background: '#002B49',
                border: 'none',
                borderRadius: '6px',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                marginTop: '8px'
              }}
              onClick={() => setPainelVizinhosAberto(true)}
            >
              👥 Painel de Gestão
            </button>
          )}
        </div>

        <div style={{padding: '8px', backgroundColor: '#F0F8FF', borderRadius: '6px', marginBottom: '15px', fontSize: '13px'}}>
          👤 Perfil: <strong>{userProfile}</strong>
        </div>

        <div style={sectionTitleStyle}>Ferramentas</div>
        <button style={menuBtnStyle(activeTool==='pan')} onClick={()=>setActiveTool('pan')}>
          <TopoIcon Icon={PanHandIcon} size={24} isActive={activeTool==='pan'} ariaLabel="Navegar" />
          Navegar
        </button>
        <button style={menuBtnStyle(false)} onClick={handleGPS}>
          <TopoIcon Icon={GpsCenterIcon} size={24} isActive={true} ariaLabel="Centralizar GPS" />
          GPS
        </button>
        <button style={menuBtnStyle(activeTool==='draw')} onClick={()=>setActiveTool('draw')}>
          <TopoIcon Icon={DrawPolygonIcon} size={24} isActive={activeTool==='draw'} ariaLabel="Desenhar Lote" />
          Desenhar Lote
        </button>
        <button style={menuBtnStyle(activeTool==='modify')} onClick={()=>setActiveTool('modify')}>
          <TopoIcon Icon={EditVerticesIcon} size={24} isActive={activeTool==='modify'} ariaLabel="Editar Vértices" />
          Editar Vértices
        </button>
        <button style={menuBtnStyle(activeTool==='measure')} onClick={()=>setActiveTool('measure')}>
          <TopoIcon Icon={MeasureIcon} size={24} isActive={activeTool==='measure'} ariaLabel="Régua" />
          Régua
        </button>
        <button style={menuBtnStyle(activeTool==='eraser', true)} onClick={()=>setActiveTool('eraser')}>
          <TopoIcon Icon={EraserIcon} size={24} isActive={activeTool==='eraser'} ariaLabel="Borracha" />
          Borracha
        </button>
        
        {/* BOTÃO PARA ENCERRAR DESENHO */}
        {activeTool !== 'pan' && (
          <button 
            style={{
              ...menuBtnStyle(false),
              backgroundColor: '#FFF3CD',
              border: '1px solid #FFC107',
              marginTop: '8px'
            }} 
            onClick={()=>setActiveTool('pan')}
          >
            ✋ Encerrar Ferramenta Atual
          </button>
        )}

        <div style={sectionTitleStyle}>Visualização</div>
        <button style={menuBtnStyle(layerMenuOpen)} onClick={()=>setLayerMenuOpen(!layerMenuOpen)}>
          <TopoIcon Icon={LayersIcon} size={24} isActive={layerMenuOpen} ariaLabel="Layers de Base" />
          Layers de Base
        </button>
        {layerMenuOpen && (
          <div style={{fontSize:'13px', paddingLeft:'10px', display:'flex', flexDirection:'column', gap:'5px', marginBottom:'10px'}}>
             <label><input type="radio" name="b" defaultChecked onChange={()=>trocarBase('Satélite (Esri)')}/> Satélite</label>
             <label><input type="radio" name="b" onChange={()=>trocarBase('Ruas (OSM)')}/> Ruas</label>
          </div>
        )}

        <div style={sectionTitleStyle}>Fluxo de Dados</div>
        <input type="file" ref={fileInputRef} style={{display:'none'}} onChange={handleImport} accept=".kml,.json,.zip" />
        <button style={menuBtnStyle(false)} onClick={()=>{setImportarComoReferencia(false); fileInputRef.current?.click();}}>
          <TopoIcon Icon={ImportIcon} size={24} isActive={true} ariaLabel="Importar Arquivo" />
          Importar Arquivo
        </button>
        <button style={{...menuBtnStyle(false), fontSize:'12px', padding:'8px 12px', background:'#FFF9E6', borderLeft:'4px solid #FFC107'}} onClick={()=>{setImportarComoReferencia(true); fileInputRef.current?.click();}}>
          <TopoIcon Icon={ImportIcon} size={24} color="#FFC107" ariaLabel="Importar Referência" />
          Importar Referência
        </button>
        <div style={{display:'flex', gap:'5px'}}>
          <button style={menuBtnStyle(false)} onClick={()=>handleExport('KML')}>
            <TopoIcon Icon={FileKmlIcon} size={24} isActive={true} ariaLabel="Exportar KML" />
            KML
          </button>
          <button style={menuBtnStyle(false)} onClick={()=>handleExport('JSON')}>
            <TopoIcon Icon={FileJsonIcon} size={24} isActive={true} ariaLabel="Exportar JSON" />
            JSON
          </button>
        </div>
        
        {/* GESTÃO DE PROJETO - AVANÇADA */}
        <div style={sectionTitleStyle}>Gestão do Projeto</div>
        
        {/* Painel Financeiro */}
        {projetoId && (
          <button 
            style={{...menuBtnStyle(painelPagamentoAberto), background: painelPagamentoAberto ? '#e8f5e9' : 'transparent', color: '#27ae60', borderLeft: painelPagamentoAberto ? '4px solid #27ae60' : '4px solid transparent'}} 
            onClick={() => setPainelPagamentoAberto(!painelPagamentoAberto)}
          >
            💰 Fluxo Financeiro
          </button>
        )}
        {painelPagamentoAberto && projetoId && (() => {
          const chave = 'db_projetos_v2';
          const projetos = JSON.parse(localStorage.getItem(chave) || '[]');
          const projeto = projetos.find((p: any) => p.id === projetoId);
          
          if (!projeto) return <div style={{fontSize:'11px', color:'#999', padding:'8px'}}>Projeto não encontrado</div>;
          
          const percentualPago = (projeto.financeiro.valorPago / projeto.financeiro.valorTotal) * 100;
          const restante = projeto.financeiro.valorTotal - projeto.financeiro.valorPago;
          
          return (
            <div style={{
              fontSize: '12px',
              padding: '12px',
              background: '#f0fdf4',
              borderRadius: '6px',
              marginBottom: '10px',
              border: '1px solid #86efac'
            }}>
              <div style={{marginBottom:'10px'}}>
                <div style={{display:'flex', justifyContent:'space-between', marginBottom:'4px'}}>
                  <span style={{fontSize:'11px', color:'#666'}}>Valor Total</span>
                  <strong style={{color:'#002B49'}}>R$ {projeto.financeiro.valorTotal.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</strong>
                </div>
                <div style={{display:'flex', justifyContent:'space-between', marginBottom:'4px'}}>
                  <span style={{fontSize:'11px', color:'#666'}}>Já Recebido</span>
                  <strong style={{color:'#27ae60'}}>R$ {projeto.financeiro.valorPago.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</strong>
                </div>
                <div style={{display:'flex', justifyContent:'space-between'}}>
                  <span style={{fontSize:'11px', color:'#666'}}>A Receber</span>
                  <strong style={{color: restante > 0 ? '#e67e22' : '#27ae60'}}>R$ {restante.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</strong>
                </div>
              </div>
              
              {/* Barra de Progresso */}
              <div style={{marginBottom:'10px'}}>
                <div style={{
                  width:'100%',
                  height:'8px',
                  background:'#e0e0e0',
                  borderRadius:'4px',
                  overflow:'hidden'
                }}>
                  <div style={{
                    width:`${percentualPago}%`,
                    height:'100%',
                    background: percentualPago === 100 ? '#27ae60' : '#3498db',
                    transition:'width 0.3s ease'
                  }}></div>
                </div>
                <div style={{fontSize:'10px', color:'#666', marginTop:'4px', textAlign:'center'}}>
                  {percentualPago.toFixed(1)}% recebido
                </div>
              </div>
              
              {/* Status Badge */}
              <div style={{
                textAlign:'center',
                padding:'6px',
                borderRadius:'4px',
                marginBottom:'10px',
                background: projeto.financeiro.status === 'quitado' ? '#27ae60' : projeto.financeiro.status === 'parcial' ? '#f39c12' : '#e74c3c',
                color:'white',
                fontWeight:'bold',
                fontSize:'11px'
              }}>
                {projeto.financeiro.status === 'quitado' ? '✅ QUITADO' : projeto.financeiro.status === 'parcial' ? '⏳ PARCIAL' : '⚠️ PENDENTE'}
              </div>
              
              {restante > 0 && (
                <button 
                  style={{
                    width:'100%',
                    padding:'10px',
                    background:'#27ae60',
                    color:'white',
                    border:'none',
                    borderRadius:'6px',
                    cursor:'pointer',
                    fontSize:'13px',
                    fontWeight:'bold',
                    transition:'all 0.2s'
                  }}
                  onClick={registrarPagamento}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#229954'}
                  onMouseLeave={(e) => e.currentTarget.style.background = '#27ae60'}
                >
                  � Registrar Recebimento
                </button>
              )}
            </div>
          );
        })()}
        
        {/* Estatísticas */}
        <button 
          style={menuBtnStyle(estatisticasAbertas)} 
          onClick={() => setEstatisticasAbertas(!estatisticasAbertas)}
        >
          📊 Estatísticas do Projeto
        </button>
        {estatisticasAbertas && (() => {
          const stats = calcularEstatisticas();
          return (
            <div style={{
              fontSize: '12px',
              padding: '12px',
              background: '#f8f9fa',
              borderRadius: '6px',
              marginBottom: '10px',
              lineHeight: '1.8'
            }}>
              <div style={{display:'flex', justifyContent:'space-between'}}>
                <span>📍 Total de Lotes:</span>
                <strong>{stats.totalLotes}</strong>
              </div>
              <div style={{display:'flex', justifyContent:'space-between'}}>
                <span>📐 Área Total:</span>
                <strong>{stats.areaTotal} ha</strong>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', color:'#0044ff'}}>
                <span>🏠 Clientes:</span>
                <strong>{stats.clientes}</strong>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', color:'#ff8800'}}>
                <span>🚧 Vizinhos:</span>
                <strong>{stats.vizinhos}</strong>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', color:'#999'}}>
                <span>⚪ Sem Classificação:</span>
                <strong>{stats.semClassificacao}</strong>
              </div>
            </div>
          );
        })()}
        
        {/* Validação */}
        <button 
          style={{...menuBtnStyle(false), fontSize:'13px'}} 
          onClick={verificarSobreposicoes}
        >
          🔍 Verificar Sobreposições
        </button>
        
        {/* Histórico de Versões */}
        <button 
          style={menuBtnStyle(historicoAbertas)} 
          onClick={() => setHistoricoAbertas(!historicoAbertas)}
        >
          � Snapshots do Projeto
        </button>
        {historicoAbertas && (() => {
          const chave = projetoId ? `historico_projeto_${projetoId}` : 'historico_ativo_real';
          const historico = JSON.parse(localStorage.getItem(chave) || '[]');
          
          return (
            <div style={{paddingLeft:'10px', marginBottom:'10px'}}>
              <button 
                style={{
                  width:'100%',
                  padding:'8px',
                  background:'#002B49',
                  color:'white',
                  border:'none',
                  borderRadius:'4px',
                  cursor:'pointer',
                  fontSize:'12px',
                  marginBottom:'8px'
                }}
                onClick={salvarVersao}
              >
                � Gerar Snapshot
              </button>
              
              {historico.length === 0 ? (
                <div style={{fontSize:'11px', color:'#999', textAlign:'center', padding:'8px'}}>
                  Nenhuma versão salva
                </div>
              ) : (
                historico.map((v: any, i: number) => (
                  <div 
                    key={i}
                    style={{
                      fontSize:'11px',
                      padding:'8px',
                      background:'#fff',
                      border:'1px solid #ddd',
                      borderRadius:'4px',
                      marginBottom:'4px',
                      cursor:'pointer',
                      transition:'all 0.2s'
                    }}
                    onClick={() => {
                      if (window.confirm(`Restaurar versão de ${new Date(v.timestamp).toLocaleString('pt-BR')}?`)) {
                        carregarVersao(i);
                      }
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#f0f8ff'}
                    onMouseLeave={(e) => e.currentTarget.style.background = '#fff'}
                  >
                    🕐 {new Date(v.timestamp).toLocaleString('pt-BR', {
                      day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit'
                    })}
                  </div>
                ))
              )}
            </div>
          );
        })()}
        
        {/* Notas do Projeto */}
        <div style={{marginBottom:'10px'}}>
          <label style={{fontSize:'11px', color:'#666', marginBottom:'4px', display:'block'}}>
            📝 Notas do Projeto
          </label>
          <textarea
            value={notasProjeto}
            onChange={(e) => setNotasProjeto(e.target.value)}
            placeholder="Anotações gerais, observações, checklist..."
            style={{
              width:'100%',
              padding:'8px',
              fontSize:'12px',
              border:'1px solid #ddd',
              borderRadius:'4px',
              minHeight:'60px',
              resize:'vertical',
              fontFamily:'inherit'
            }}
          />
        </div>
        
        {/* Ações Rápidas */}
        <button 
          style={{...menuBtnStyle(false), fontSize:'13px'}} 
          onClick={gerarRelatorio}
        >
          📋 Gerar Relatório Completo
        </button>
        
        {projetoId && (
          <button 
            style={{...menuBtnStyle(false), fontSize:'13px'}} 
            onClick={sincronizarComDashboard}
          >
            <TopoIcon Icon={SyncIcon} size={24} isActive={true} ariaLabel="Sincronizar com Dashboard" />
            Sincronizar com Dashboard
          </button>
        )}
        
        <button 
          style={menuBtnStyle(false)} 
          onClick={()=>{
            const chaveStorage = projetoId ? `rascunho_projeto_${projetoId}` : 'ativo_real_rascunho';
            const data = new GeoJSON().writeFeatures(vectorSource.getFeatures());
            localStorage.setItem(chaveStorage, data);
            alert('✅ Projeto salvo com sucesso!');
          }}
        >
          <TopoIcon Icon={SaveDraftIcon} size={24} isActive={true} ariaLabel="Salvar Rascunho" />
          Salvar Rascunho
        </button>

        {/* Validar na Nuvem (Botão Novo - Agente 3) */}
        <button 
          style={{...menuBtnStyle(false), backgroundColor: '#28a745', color: 'white'}} 
          onClick={async ()=>{
            const feats = vectorSource.getFeatures();
            if (feats.length === 0) return alert("❌ Desenhe um lote primeiro!");
            
            // Só pega o primeiro por enquanto
            const geom = feats[0].getGeometry();
            if (!geom || geom.getType() !== 'Polygon') return alert("❌ Apenas polígonos são aceitos.");

            const poly = geom as Polygon;
            
            // Converter coordenadas para Lat/Lon
            // OpenLayers usa [Lon, Lat], API espera [Lon, Lat] (tupla)
            // Mas o backend Python espera: "coordinates": [[lon, lat], ...]
            // O código Python conserta a ordem se precisar, mas vamos mandar o padrão GeoJSON
            
            const rawCoords = poly.getCoordinates()[0];
            const coordsLatLon = rawCoords.map(c => {
               const ll = toLonLat(c);
               return [ll[0], ll[1]]; // lon, lat
            });

            const payload = {
               matricula: "RASCUNHO-" + Date.now(),
               proprietario: "Topógrafo (Teste)",
               projeto_id: projetoId ? projetoId : null,
               coordinates: coordsLatLon
            };

            try {
               alert("⏳ Enviando para validação no servidor...");
               const res = await fetch('https://func-bemreal-ai1-1406.azurewebsites.net/api/lotes', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify(payload)
               });
               const data = await res.json();
               
               if(!res.ok) {
                 // Erro Técnico ou Bloqueio Crítico (se houver)
                 alert(`❌ Erro ao salvar:\n\n${data.detail || JSON.stringify(data)}`);
               } else {
                 // 30/01/2026: Cliente recebe feedback APENAS se houver sobreposição SIGEF (informativo)
                 // Para outros avisos (frestas, vizinhos), o silêncio é mantido para não confundir o leigo.
                 const avisosSigef = (data.warnings || []).filter((w: string) => w.includes("SIGEF") || w.includes("INCRA"));
                 
                 if (avisosSigef.length > 0) {
                     alert(`✅ Esboço salvo com sucesso!\n\nℹ️ NOTA INFORMATIVA:\nO sistema identificou que este desenho toca uma área certificada (SIGEF). Não se preocupe, o topógrafo analisará este detalhe técnico.`);
                 } else {
                     alert("✅ Esboço enviado com sucesso!");
                 }
                 // Limpar mapa ou atualizar status...
               }

            } catch(e) {
               alert("❌ Erro ao conectar com o servidor.");
               console.error(e);
            }
          }}
        >
          <TopoIcon Icon={ImportIcon} size={24} isActive={true} ariaLabel="Validar" />
          Validar & Gravar (Nuvem)
        </button>

        <button 
          style={menuBtnStyle(false)} 
          onClick={()=>{
            const chaveStorage = projetoId ? `rascunho_projeto_${projetoId}` : 'ativo_real_rascunho';
            const saved = localStorage.getItem(chaveStorage);
            if(saved) {
              const features = new GeoJSON().readFeatures(saved);
              vectorSource.clear();
              vectorSource.addFeatures(features);
              alert('✅ Rascunho carregado!');
            } else {
              alert('⚠️ Nenhum rascunho encontrado.');
            }
          }}
        >
          📂 Carregar Rascunho
        </button>

        <div style={{marginTop:'auto', paddingTop: '15px', borderTop: '1px solid #E0E0E0'}}>
            <button style={{...menuBtnStyle(false, true), justifyContent:'center'}} onClick={handleClearAll}>⚠️ Limpar Tudo</button>
        </div>
      </aside>

      {/* MAPA */}
      <main style={mapContainerStyle}>
        <div ref={mapRef} style={{ width: '100%', height: '100%' }} />
        
        {/* Mostrador de Medida */}
        {medidaAtual && (
           <div style={{position:'absolute', top:'20px', left:'50%', transform:'translateX(-50%)', background:'rgba(0,43,73,0.9)', color:'#FFD700', padding:'8px 20px', borderRadius:'20px', zIndex:20, fontWeight:'bold'}}>{medidaAtual}</div>
        )}

        {/* Coordenadas Rodapé */}
        <div id="mouse-position" style={{position:'absolute', bottom:'5px', right:'5px', background:'rgba(255,255,255,0.8)', padding:'2px 8px', fontSize:'11px', borderRadius:'4px'}}></div>

        {/* DRAWER LATERAL - GESTÃO DE ENVOLVIDOS */}
        {painelVizinhosAberto && (
          <div style={{
            position: 'absolute',
            top: 0,
            right: 0,
            bottom: 0,
            width: '90%',
            maxWidth: '350px',
            backgroundColor: 'white',
            boxShadow: '-4px 0 15px rgba(0,0,0,0.1)',
            zIndex: 20,
            padding: '25px',
            overflowY: 'auto',
            transition: 'transform 0.3s ease'
          }}>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'20px'}}>
              <h2 style={{margin:0, color:'#002B49', fontSize:'20px'}}>Gestão de Envolvidos</h2>
              <button 
                onClick={() => setPainelVizinhosAberto(false)} 
                style={{
                  background:'none', 
                  border:'none', 
                  fontSize:'1.5rem', 
                  cursor:'pointer',
                  color:'#999',
                  lineHeight:'1'
                }}
              >
                ✖
              </button>
            </div>
            
            <p style={{fontSize:'13px', color:'#666', marginBottom:'20px'}}>Gerencie os proprietários e vizinhos deste projeto.</p>
            
            {/* Lista de Vizinhos */}
            {vizinhos.map(v => (
              <div 
                key={v.id} 
                style={{
                  padding:'12px', 
                  background:'#f8f9fa', 
                  marginBottom:'10px', 
                  borderRadius:'8px', 
                  borderLeft:`4px solid ${v.status==='ok'?'#27ae60':'#e74c3c'}`,
                  boxShadow:'0 1px 3px rgba(0,0,0,0.05)'
                }}
              >
                <div style={{fontWeight:'bold', color:'#2c3e50', marginBottom:'4px'}}>{v.nome}</div>
                <div style={{fontSize:'0.75rem', color:'#7f8c8d', marginBottom:'8px'}}>
                  {v.status === 'ok' ? '✅ Finalizado' : '⏳ Pendente de Validação'}
                </div>
                {v.status === 'pendente' && (
                  <button 
                    style={{
                      width:'100%', 
                      padding:'6px', 
                      background:'#3498db', 
                      color:'white', 
                      border:'none', 
                      borderRadius:'4px', 
                      cursor:'pointer',
                      fontSize:'12px',
                      fontWeight:'500'
                    }}
                    onClick={() => {
                      navigator.clipboard.writeText(v.link || 'https://ativo.pro/projeto/' + projetoId);
                      alert('🔗 Link copiado! Envie ao vizinho para validar.');
                    }}
                  >
                    🔗 Copiar Link de Validação
                  </button>
                )}
              </div>
            ))}
            
            <button 
              onClick={() => {
                const nome = prompt('Nome do novo envolvido:');
                if(nome) {
                  setVizinhos([...vizinhos, {
                    id: Date.now(), 
                    nome: nome, 
                    status: 'pendente', 
                    link: 'https://ativo.pro/projeto/' + projetoId + '/validar/' + Date.now()
                  }]);
                }
              }} 
              style={{
                marginTop:'15px', 
                width:'100%', 
                padding:'12px', 
                border:'2px dashed #bdc3c7', 
                background:'transparent', 
                color:'#7f8c8d', 
                cursor:'pointer',
                borderRadius:'8px',
                fontSize:'14px',
                fontWeight:'500'
              }}
            >
              + Adicionar Envolvido
            </button>
          </div>
        )}

        {/* Popup de Classificação */}
        <div ref={popupRef} className="ol-popup" style={{display: popupData ? 'block' : 'none'}}>
           <a href="#" className="ol-popup-closer" onClick={()=>overlayRef.current?.setPosition(undefined)}>✖</a>
           {popupData && (
             <div>
               <strong>Classificar Lote</strong><br/>
               <small>Área: {popupData.area}</small>
               
               {/* Indicador Visual de Classificação Atual */}
               <div style={{
                 marginTop: '8px',
                 padding: '6px 10px',
                 borderRadius: '4px',
                 fontSize: '12px',
                 fontWeight: 'bold',
                 textAlign: 'center',
                 background: popupData.tipo === 'cliente' ? '#0044ff' : 
                            popupData.tipo === 'vizinho' ? '#ff8800' : '#ffcc33',
                 color: 'white'
               }}>
                 {popupData.tipo === 'cliente' ? '🏠 CLIENTE' : 
                  popupData.tipo === 'vizinho' ? `🚧 VIZINHO: ${popupData.proprietario}` : 
                  '⚪ SEM CLASSIFICAÇÃO'}
               </div>
               
               {/* Botões de Classificação */}
               <div style={{display:'flex', gap:'6px', marginTop:'10px'}}>
                 <button 
                   style={{
                     flex: 1,
                     padding: '8px',
                     border: 'none',
                     borderRadius: '4px',
                     background: '#0044ff',
                     color: 'white',
                     cursor: 'pointer',
                     fontWeight: 'bold',
                     fontSize: '11px'
                   }}
                   onClick={() => {
                     popupData.feature.set('tipo', 'cliente');
                     popupData.feature.set('proprietario', 'CLIENTE');
                     setPopupData({...popupData, tipo: 'cliente', proprietario: 'CLIENTE'});
                     
                     // Salvar no banco
                     const chaveStorage = projetoId ? `rascunho_projeto_${projetoId}` : 'rascunho_ativo_real';
                     const json = new GeoJSON().writeFeatures(vectorSource.getFeatures(), { featureProjection: 'EPSG:3857' });
                     localStorage.setItem(chaveStorage, json);
                   }}
                 >
                   🏠 Cliente (Dono)
                 </button>
                 
                 <button 
                   style={{
                     flex: 1,
                     padding: '8px',
                     border: 'none',
                     borderRadius: '4px',
                     background: '#ff8800',
                     color: 'white',
                     cursor: 'pointer',
                     fontWeight: 'bold',
                     fontSize: '11px'
                   }}
                   onClick={() => {
                     const nome = prompt('Nome do Vizinho:');
                     if (nome) {
                       popupData.feature.set('tipo', 'vizinho');
                       popupData.feature.set('proprietario', nome);
                       setPopupData({...popupData, tipo: 'vizinho', proprietario: nome});
                       
                       // Salvar no banco
                       const chaveStorage = projetoId ? `rascunho_projeto_${projetoId}` : 'rascunho_ativo_real';
                       const json = new GeoJSON().writeFeatures(vectorSource.getFeatures(), { featureProjection: 'EPSG:3857' });
                       localStorage.setItem(chaveStorage, json);
                     }
                   }}
                 >
                   🚧 Vizinho
                 </button>
               </div>
             </div>
           )}
        </div>
      </main>
    </div>
  );
};

export default GlobalMap;
