import React, { useEffect, useRef, useState } from 'react';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Draw, Snap } from 'ol/interaction';
import { fromLonLat, toLonLat } from 'ol/proj';
import { api } from '../services/api';
import { Button } from './ui/Button'; 

// 🎨 Agente 3: Especialista em Mapas
// Responsabilidade: Capturar coordenadas e feedback visual. NENHUMA lógica complexa aqui.

const MapEditor = ({ projetoId, onBack }) => {
  const mapRef = useRef(null);
  const [mapObj, setMapObj] = useState(null);
  const [status, setStatus] = useState('Pronto para desenhar');

  useEffect(() => {
    if (mapRef.current && !mapObj) {
      // 1. Inicialização do Mapa
      const source = new VectorSource();
      const vector = new VectorLayer({
        source: source,
        style: {
            'fill-color': 'rgba(255, 255, 255, 0.2)',
            'stroke-color': '#ffcc33',
            'stroke-width': 2,
            'circle-radius': 7,
            'circle-fill-color': '#ffcc33',
        },
      });

      const map = new Map({
        target: mapRef.current,
        layers: [
          new TileLayer({
            source: new OSM(), // Mapa base (OpenStreetMap)
          }),
          vector,
        ],
        view: new View({
          center: fromLonLat([-47.9292, -15.7801]), // Brasília
          zoom: 12, // Zoom inicial
        }),
      });

      // 2. Ferramentas de Interação
      
      // DRAW: Permite desenhar polígonos
      const draw = new Draw({
        source: source,
        type: 'Polygon',
      });

      // SNAP: Imã magnético para garantir precisão topológica (conecta vértices exatos)
      const snap = new Snap({ source: source });

      map.addInteraction(draw);
      map.addInteraction(snap);

      // 3. Evento: Ao terminar o desenho
      draw.on('drawend', async (event) => {
        const feature = event.feature;
        const geometry = feature.getGeometry();
        
        // Coletar coordenadas em EPSG:3857 (Web Mercator)
        const coords3857 = geometry.getCoordinates()[0]; // Outer ring
        
        // Converter para EPSG:4326 (Lat/Lon) para enviar ao backend
        const coords4326 = coords3857.map(coord => {
            const lonlat = toLonLat(coord);
            return [lonlat[1], lonlat[0]]; // [Lat, Lon] formato esperado pelo Python Schema
        });

        setStatus('Validando com Agente Backend...');

        try {
          // 4. Delegação: Envia para a API validar a Regra de Negócio
          const payload = {
            matricula: `MAT-${Date.now()}`, // Gerando ID temporário
            proprietario: "Usuário Atual",
            projeto_id: projetoId, // Associando ao projeto selecionado
            coordinates: coords4326
          };

          const data = await api.createLote(payload);
          
          setStatus(`✅ Lote aprovado! ID: ${data.id} - Área: ${data.area_ha} ha`);
          console.log("Sucesso:", data);
          
          // Opcional: Mudar cor para verde para indicar sucesso (necessita style function, simplificando aqui)
          
        } catch (error) {
          const errorMsg = error.message || "Erro de validação";
          console.error("Erro na validação:", error);
          
          // 5. Feedback de Erro de Regra de Negócio (Sobreposição)
          
            alert(`⛔ BLOQUEADO PELO BACKEND:\n\n${errorMsg}`);
            setStatus(`❌ Rejeitado: ${errorMsg}`);
            
            // Remove o desenho inválido do mapa
            source.removeFeature(feature);
        }
      });

      setMapObj(map);
    }
  }, [mapRef, mapObj]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {/* Toolbar Header (Overlay) */}
      <div style={{
        position: 'absolute',
        top: 20,
        left: 20,
        zIndex: 100,
        background: 'rgba(255,255,255,0.9)',
        padding: '10px',
        borderRadius: '8px',
        display: 'flex',
        gap: '10px',
        alignItems: 'center'
      }}>
        {onBack && (
          <Button onClick={onBack} variant="ghost" style={{ padding: '8px 12px', fontSize: '14px' }}>
            ← Voltar
          </Button>
        )}
        <span style={{ fontWeight: 'bold', color: '#1e293b' }}>
          {projetoId ? `Editando Projeto #${projetoId}` : 'Modo Livre'}
        </span>
      </div>

      <div 
        ref={mapRef} 
        style={{ width: '100%', height: '100%', cursor: 'crosshair' }} 
      />

      <div style={{
        position: 'absolute',
        bottom: 20,
        left: 20,
        background: 'white',
        padding: '10px 20px',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        zIndex: 100,
        fontWeight: 'bold',
        color: '#333'
      }}>
        Status: {status}
      </div>
    </div>
  );
};

export default MapEditor;
