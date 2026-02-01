// @ts-nocheck
import { useEffect, useRef, useState } from 'react';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import XYZ from 'ol/source/XYZ';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import { Draw, Modify, Snap, Select } from 'ol/interaction';
import { click } from 'ol/events/condition';
import { ScaleLine, defaults as defaultControls } from 'ol/control';
import { getArea } from 'ol/sphere';
import { unByKey } from 'ol/Observable';
import Overlay from 'ol/Overlay';
import { GeoJSON, KML } from 'ol/format';
import { Circle as CircleStyle, Fill, Stroke, Style, Text } from 'ol/style';

// --- ESTILOS VISUAIS ---
const styles = {
  container: { position: 'relative' as const, height: '100vh', width: '100vw', overflow: 'hidden', fontFamily: 'Segoe UI, sans-serif' },
  mapa: { position: 'absolute' as const, top: 0, left: 0, right: 0, bottom: 0, zIndex: 0 },
  
  header: { position: 'absolute' as const, top: '15px', left: '15px', right: '15px', display: 'flex', justifyContent: 'space-between', zIndex: 10, pointerEvents: 'none' as const },
  btnVoltar: { pointerEvents: 'auto' as const, backgroundColor: 'white', border: 'none', padding: '10px 20px', borderRadius: '30px', boxShadow: '0 2px 8px rgba(0,0,0,0.15)', fontWeight: 'bold', color: '#555', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px' },
  btnGestao: { pointerEvents: 'auto' as const, backgroundColor: '#002B49', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '30px', boxShadow: '0 2px 8px rgba(0,0,0,0.25)', fontWeight: 'bold', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' },

  statusBar: { position: 'absolute' as const, bottom: '30px', left: '50%', transform: 'translateX(-50%)', backgroundColor: 'rgba(0, 43, 73, 0.9)', color: 'white', padding: '10px 25px', borderRadius: '30px', boxShadow: '0 4px 15px rgba(0,0,0,0.3)', zIndex: 10, fontSize: '14px', fontWeight: '500', display: 'flex', alignItems: 'center', gap: '10px', whiteSpace: 'nowrap' as const },

  toolbarEsquerda: { position: 'absolute' as const, top: '50%', left: '15px', transform: 'translateY(-50%)', display: 'flex', flexDirection: 'column' as const, gap: '15px', zIndex: 10 },
  btnFerramenta: (ativo: boolean) => ({ width: '50px', height: '50px', borderRadius: '50%', border: ativo ? '2px solid #002B49' : 'none', backgroundColor: ativo ? '#e3f2fd' : 'white', boxShadow: '0 2px 8px rgba(0,0,0,0.15)', fontSize: '1.4rem', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#444', transition: 'all 0.2s', pointerEvents: 'auto' as const }),

  btnValidar: {
    position: 'absolute' as const, top: '80px', right: '15px',
    backgroundColor: '#e74c3c', color: 'white', border: 'none', padding: '12px 20px',
    borderRadius: '8px', boxShadow: '0 4px 10px rgba(0,0,0,0.2)', fontWeight: 'bold',
    cursor: 'pointer', zIndex: 10, display: 'flex', alignItems: 'center', gap: '8px'
  },

  drawer: { position: 'absolute' as const, top: 0, right: 0, bottom: 0, width: '90%', maxWidth: '350px', backgroundColor: 'white', boxShadow: '-4px 0 15px rgba(0,0,0,0.1)', zIndex: 20, padding: '25px', overflowY: 'auto' as const, transition: 'transform 0.3s ease' },
  layerMenu: { position: 'absolute' as const, left: '70px', backgroundColor: 'white', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.15)', zIndex: 11, minWidth: '180px' }
};

// --- ESTILOS DO MAPA ---
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
  }),
  
  governo: new Style({
    stroke: new Stroke({ color: '#d32f2f', width: 2, lineDash: [10, 10] }),
    fill: new Fill({ color: 'rgba(211, 47, 47, 0.1)' }),
    text: new Text({ 
      text: 'ÁREA RESTRITA', 
      font: 'bold 10px sans-serif', 
      fill: new Fill({ color: '#d32f2f' }), 
      stroke: new Stroke({ color: 'white', width: 3 }),
      overflow: true 
    })
  }),
  
  erro: new Style({
    stroke: new Stroke({ color: '#ff0000', width: 4 }),
    fill: new Fill({ color: 'rgba(255, 0, 0, 0.5)' }),
    zIndex: 99
  })
};

// --- CARREGAR DADOS DO GOVERNO (SIGEF/FUNAI) DA API ---
const carregarDadosGovernamentais = async () => {
  try {
    const response = await fetch('/api/governo/areas');
    
    if (!response.ok) {
      console.error('Erro ao carregar dados governamentais:', response.status);
      return [];
    }
    
    const areas = await response.json();
    
    return areas.map((area: any) => {
      return new GeoJSON().readFeature({
        type: 'Feature',
        geometry: { type: 'Polygon', coordinates: [area.coords] },
        properties: { tipo: area.tipo, nome: area.nome }
      }, { featureProjection: 'EPSG:3857' });
    });
  } catch (error) {
    console.error('Erro ao conectar com API de governo:', error);
    return [];
  }
};

interface GlobalMapProps {
  userProfile: string;
  projetoId: number | null;
  onLogout: () => void;
}

export default function GlobalMapValidacao({ userProfile: _userProfile, projetoId, onLogout }: GlobalMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const popupRef = useRef<HTMLDivElement>(null);
  const overlayRef = useRef<Overlay | null>(null);
  
  const [map, setMap] = useState<Map | null>(null);
  const [vectorSource] = useState(new VectorSource());
  const [governoSource] = useState(new VectorSource());
  
  const [activeTool, setActiveTool] = useState('pan');
  const [instrucao, setInstrucao] = useState('Desenhe os lotes. Use o botão vermelho para validar.');
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [layerMenuOpen, setLayerMenuOpen] = useState(false);
  
  const [validacaoStatus, setValidacaoStatus] = useState<'ok' | 'erro' | 'loading' | null>(null);
  const [errosDetectados, setErrosDetectados] = useState<any[]>([]);

  // 1. INICIALIZAÇÃO
  useEffect(() => {
    if (!mapRef.current) return;

    // Carregar dados governamentais (async)
    (async () => {
      const dadosGoverno = await carregarDadosGovernamentais();
      dadosGoverno.forEach(feature => {
        if (Array.isArray(feature)) {
          feature.forEach(f => governoSource.addFeature(f));
        } else {
          governoSource.addFeature(feature);
        }
      });
    })();

    const sateliteLayer = new TileLayer({ 
      source: new XYZ({ 
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
        maxZoom: 19 
      }), 
      visible: true,
      properties: { title: 'Satélite', type: 'base' }
    });
    
    const osmLayer = new TileLayer({ 
      source: new OSM(), 
      visible: false,
      properties: { title: 'Ruas', type: 'base' }
    });
    
    // Camada Governamental (sempre visível, atrás)
    const governoLayer = new VectorLayer({
      source: governoSource,
      zIndex: 1,
      style: mapStyles.governo,
      properties: { title: 'Áreas Governamentais', type: 'overlay' }
    });

    // Camada do Usuário (na frente)
    const desenhoLayer = new VectorLayer({
      source: vectorSource,
      zIndex: 2,
      style: (feature) => {
        const tipo = feature.get('tipo');
        const nome = feature.get('proprietario');
        const temErro = feature.get('erro');
        
        if (temErro) return mapStyles.erro;
        if (tipo === 'cliente') return mapStyles.cliente;
        if (tipo === 'vizinho') return mapStyles.vizinho(nome);
        return mapStyles.padrao;
      }
    });

    const overlay = new Overlay({
      element: popupRef.current!,
      autoPan: { animation: { duration: 250 } }
    });
    overlayRef.current = overlay;

    const mapObject = new Map({
      target: mapRef.current,
      layers: [sateliteLayer, osmLayer, governoLayer, desenhoLayer],
      view: new View({ center: fromLonLat([-47.8822, -15.7942]), zoom: 14 }),
      overlays: [overlay],
      controls: defaultControls().extend([new ScaleLine({ units: 'metric' })])
    });

    setMap(mapObject);

    // Auto-load rascunho
    const chave = projetoId ? `rascunho_projeto_${projetoId}` : 'rascunho_ativo_real';
    const saved = localStorage.getItem(chave);
    if (saved) {
      const features = new GeoJSON().readFeatures(saved, { featureProjection: 'EPSG:3857' });
      vectorSource.addFeatures(features);
    }

    return () => mapObject.setTarget(undefined);
  }, []);

  // 2. AUTO-SAVE
  useEffect(() => {
    if (!vectorSource) return;
    const chave = projetoId ? `rascunho_projeto_${projetoId}` : 'rascunho_ativo_real';
    const salvar = () => {
      const json = new GeoJSON().writeFeatures(vectorSource.getFeatures(), { featureProjection: 'EPSG:3857' });
      localStorage.setItem(chave, json);
    };
    vectorSource.on('addfeature', salvar);
    vectorSource.on('changefeature', salvar);
    vectorSource.on('removefeature', salvar);
    return () => {
      vectorSource.un('addfeature', salvar);
      vectorSource.un('changefeature', salvar);
      vectorSource.un('removefeature', salvar);
    };
  }, [vectorSource, projetoId]);

  // 3. GERENCIADOR DE FERRAMENTAS
  useEffect(() => {
    if (!map) return;
    
    // Limpar interações
    map.getInteractions().forEach((i) => {
      if (i instanceof Draw || i instanceof Modify || i instanceof Snap || i instanceof Select) {
        map.removeInteraction(i);
      }
    });

    let listener: any;

    switch (activeTool) {
      case 'draw':
        const draw = new Draw({ source: vectorSource, type: 'Polygon' });
        draw.on('drawstart', (e) => {
          listener = e.feature.getGeometry()?.on('change', (evt: any) => {
            const area = (getArea(evt.target) / 10000).toFixed(4);
            setInstrucao(`Área: ${area} ha`);
          });
        });
        draw.on('drawend', (e) => { 
          unByKey(listener); 
          setInstrucao('Lote criado. Valide com o botão vermelho.');
          
          // Validação automática ao desenhar
          setTimeout(() => validarLote(e.feature), 500);
        });
        map.addInteraction(draw);
        map.addInteraction(new Snap({ source: vectorSource }));
        setInstrucao('Clique para começar a desenhar o lote');
        break;

      case 'modify':
        map.addInteraction(new Modify({ source: vectorSource }));
        map.addInteraction(new Snap({ source: vectorSource }));
        setInstrucao('Clique e arraste os vértices para ajustar');
        break;

      case 'eraser':
        const select = new Select({ condition: click });
        select.on('select', (e) => {
          if (e.selected.length > 0) {
            if (window.confirm('Excluir este lote?')) {
              vectorSource.removeFeature(e.selected[0]);
              overlayRef.current?.setPosition(undefined);
            }
            select.getFeatures().clear();
          }
        });
        map.addInteraction(select);
        setInstrucao('Clique no lote para excluir');
        break;

      default:
        setInstrucao('Use as ferramentas da esquerda');
        break;
    }

    return () => { if (listener) unByKey(listener); };
  }, [activeTool, map, vectorSource]);

  // === FUNÇÕES DE VALIDAÇÃO ===
  
  const validarLote = (feature: any) => {
    const geom = feature.getGeometry();
    if (!geom) return;

    const areasGoverno = governoSource.getFeatures();
    let temSobreposicao = false;

    for (const areaGoverno of areasGoverno) {
      const geomGoverno = areaGoverno.getGeometry();
      if (geomGoverno && (geom as any).intersects(geomGoverno)) {
        temSobreposicao = true;
        feature.set('erro', true);
        feature.set('motivoErro', `Sobreposição com ${areaGoverno.get('tipo')}: ${areaGoverno.get('nome')}`);
        break;
      }
    }

    if (temSobreposicao) {
      setInstrucao('⚠️ ERRO: Sobreposição detectada!');
      alert(`🚨 ERRO DE VALIDAÇÃO\n\n${feature.get('motivoErro')}\n\nO lote será marcado em VERMELHO.\nAções disponíveis:\n• Ajustar limites (ferramenta ✏️)\n• Excluir lote (ferramenta 🗑️)`);
    } else {
      feature.set('erro', false);
      feature.unset('motivoErro');
      setInstrucao('✅ Lote validado com sucesso!');
    }

    // Forçar redesenho
    vectorSource.changed();
  };

  const validarTodosLotes = () => {
    setValidacaoStatus('loading');
    setInstrucao('🔄 Validando todos os lotes...');

    const features = vectorSource.getFeatures();
    const erros: any[] = [];

    features.forEach((feature, index) => {
      const geom = feature.getGeometry();
      if (!geom) return;

      const areasGoverno = governoSource.getFeatures();
      
      for (const areaGoverno of areasGoverno) {
        const geomGoverno = areaGoverno.getGeometry();
        if (geomGoverno && (geom as any).intersects(geomGoverno)) {
          feature.set('erro', true);
          feature.set('motivoErro', `Sobreposição com ${areaGoverno.get('tipo')}: ${areaGoverno.get('nome')}`);
          erros.push({
            lote: feature.get('proprietario') || `Lote ${index + 1}`,
            motivo: feature.get('motivoErro')
          });
          break;
        } else {
          feature.set('erro', false);
          feature.unset('motivoErro');
        }
      }
    });

    vectorSource.changed();
    setErrosDetectados(erros);

    setTimeout(() => {
      if (erros.length > 0) {
        setValidacaoStatus('erro');
        setInstrucao(`❌ ${erros.length} erro(s) detectado(s)`);
        alert(`🚨 VALIDAÇÃO SIGEF/FUNAI\n\nErros encontrados: ${erros.length}\n\n${erros.map(e => `• ${e.lote}: ${e.motivo}`).join('\n')}\n\nLotes com erro estão marcados em VERMELHO.`);
      } else {
        setValidacaoStatus('ok');
        setInstrucao('✅ Todos os lotes validados!');
        alert('✅ VALIDAÇÃO CONCLUÍDA\n\nTodos os lotes estão conformes com SIGEF/FUNAI.');
      }
    }, 1000);
  };

  const trocarBase = (titulo: string) => {
    map?.getLayers().forEach(l => {
      if (l.get('type') === 'base') l.setVisible(l.get('title') === titulo);
    });
  };

  const handleExport = (formato: 'KML' | 'JSON') => {
    if (!vectorSource.getFeatures().length) return alert('Mapa vazio!');
    
    const formatador = formato === 'KML' ? new KML({ extractStyles: true }) : new GeoJSON();
    const ext = formato === 'KML' ? 'kml' : 'json';
    const mime = formato === 'KML' ? 'application/vnd.google-earth.kml+xml' : 'application/json';
    
    const data = formatador.writeFeatures(vectorSource.getFeatures(), { 
      dataProjection: 'EPSG:4326', 
      featureProjection: 'EPSG:3857' 
    });
    
    const blob = new Blob([data], { type: mime });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `projeto_validado.${ext}`;
    link.click();
  };

  return (
    <div style={styles.container}>
      {/* MAPA */}
      <div ref={mapRef} style={styles.mapa} />

      {/* HEADER */}
      <header style={styles.header}>
        <button style={styles.btnVoltar} onClick={onLogout}>
          ← Voltar
        </button>
        <button style={styles.btnGestao} onClick={() => setDrawerOpen(!drawerOpen)}>
          👥 Envolvidos ({0})
        </button>
      </header>

      {/* BOTÃO DE VALIDAÇÃO SIGEF */}
      <button 
        style={{
          ...styles.btnValidar,
          backgroundColor: validacaoStatus === 'ok' ? '#27ae60' : validacaoStatus === 'erro' ? '#e74c3c' : '#f39c12'
        }}
        onClick={validarTodosLotes}
      >
        {validacaoStatus === 'loading' ? '🔄' : validacaoStatus === 'ok' ? '✅' : validacaoStatus === 'erro' ? '❌' : '🛡️'}
        Validar SIGEF/FUNAI
      </button>

      {/* TOOLBAR ESQUERDA */}
      <div style={styles.toolbarEsquerda}>
        <button 
          style={styles.btnFerramenta(activeTool === 'pan')} 
          onClick={() => setActiveTool('pan')}
          title="Navegação"
        >
          ✋
        </button>
        <button 
          style={styles.btnFerramenta(activeTool === 'draw')} 
          onClick={() => setActiveTool('draw')}
          title="Desenhar Lote"
        >
          ✏️
        </button>
        <button 
          style={styles.btnFerramenta(activeTool === 'modify')} 
          onClick={() => setActiveTool('modify')}
          title="Editar Lote"
        >
          🔧
        </button>
        <button 
          style={styles.btnFerramenta(activeTool === 'eraser')} 
          onClick={() => setActiveTool('eraser')}
          title="Excluir Lote"
        >
          🗑️
        </button>
        
        <div style={{ position: 'relative' }}>
          <button 
            style={styles.btnFerramenta(layerMenuOpen)} 
            onClick={() => setLayerMenuOpen(!layerMenuOpen)}
            title="Camadas"
          >
            🌍
          </button>
          {layerMenuOpen && (
            <div style={styles.layerMenu}>
              <label style={{ display: 'block', marginBottom: '8px' }}>
                <input type="radio" name="base" defaultChecked onChange={() => trocarBase('Satélite')} />
                {' '}Satélite
              </label>
              <label style={{ display: 'block' }}>
                <input type="radio" name="base" onChange={() => trocarBase('Ruas')} />
                {' '}Ruas (OSM)
              </label>
              <hr style={{ margin: '10px 0', border: 'none', borderTop: '1px solid #ddd' }} />
              <label style={{ display: 'block', color: '#d32f2f', fontWeight: 'bold' }}>
                <input type="checkbox" defaultChecked disabled />
                {' '}Áreas SIGEF/FUNAI
              </label>
            </div>
          )}
        </div>
      </div>

      {/* BARRA DE STATUS */}
      <div style={styles.statusBar}>
        <span>{instrucao}</span>
        {errosDetectados.length > 0 && (
          <span style={{ 
            backgroundColor: '#e74c3c', 
            padding: '4px 10px', 
            borderRadius: '12px',
            fontSize: '12px'
          }}>
            {errosDetectados.length} erro(s)
          </span>
        )}
      </div>

      {/* DRAWER DE ENVOLVIDOS */}
      {drawerOpen && (
        <div style={styles.drawer}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
            <h2 style={{ margin: 0, fontSize: '18px' }}>Gestão de Envolvidos</h2>
            <button 
              onClick={() => setDrawerOpen(false)}
              style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer' }}
            >
              ✖
            </button>
          </div>
          
          <p style={{ fontSize: '13px', color: '#666' }}>
            Lista vazia. Adicione proprietários e vizinhos ao projeto.
          </p>

          <button
            style={{
              width: '100%',
              padding: '12px',
              background: '#002B49',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
            onClick={() => {
              const nome = prompt('Nome do envolvido:');
              if (nome) alert(`Funcionalidade em desenvolvimento: ${nome}`);
            }}
          >
            + Adicionar Envolvido
          </button>

          <hr style={{ margin: '20px 0' }} />

          <h3 style={{ fontSize: '14px', marginBottom: '10px' }}>Exportar Projeto</h3>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              style={{ flex: 1, padding: '10px', border: '1px solid #ddd', borderRadius: '6px', cursor: 'pointer' }}
              onClick={() => handleExport('KML')}
            >
              💾 KML
            </button>
            <button
              style={{ flex: 1, padding: '10px', border: '1px solid #ddd', borderRadius: '6px', cursor: 'pointer' }}
              onClick={() => handleExport('JSON')}
            >
              💾 JSON
            </button>
          </div>
        </div>
      )}

      {/* POPUP (para futuras interações) */}
      <div ref={popupRef} style={{ display: 'none' }} />
    </div>
  );
}
