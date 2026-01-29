import { GeoJSON } from 'ol/format';
import VectorSource from 'ol/source/Vector';
import { Geometry, Polygon } from 'ol/geom';
import Feature from 'ol/Feature';

// ============== FERRAMENTAS CAD AVANÇADAS ==============

export const saveToUndoStack = (
  vectorSource: VectorSource,
  _undoStack: string[],
  setUndoStack: (fn: (prev: string[]) => string[]) => void,
  setRedoStack: (stack: string[]) => void
) => {
  const currentState = new GeoJSON().writeFeatures(
    vectorSource.getFeatures(),
    { featureProjection: 'EPSG:3857' }
  );
  setUndoStack((prev) => [...prev, currentState].slice(-20));
  setRedoStack([]);
};

export const undo = (
  vectorSource: VectorSource,
  undoStack: string[],
  setUndoStack: (fn: (prev: string[]) => string[]) => void,
  _redoStack: string[],
  setRedoStack: (fn: (prev: string[]) => string[]) => void
) => {
  if (undoStack.length === 0) return alert('⚠️ Nada para desfazer');
  
  const currentState = new GeoJSON().writeFeatures(
    vectorSource.getFeatures(),
    { featureProjection: 'EPSG:3857' }
  );
  setRedoStack((prev) => [...prev, currentState]);
  
  const previousState = undoStack[undoStack.length - 1];
  setUndoStack((prev) => prev.slice(0, -1));
  
  const features = new GeoJSON().readFeatures(previousState, {
    featureProjection: 'EPSG:3857',
  });
  vectorSource.clear();
  vectorSource.addFeatures(features);
};

export const redo = (
  vectorSource: VectorSource,
  _undoStack: string[],
  setUndoStack: (fn: (prev: string[]) => string[]) => void,
  redoStack: string[],
  setRedoStack: (fn: (prev: string[]) => string[]) => void
) => {
  if (redoStack.length === 0) return alert('⚠️ Nada para refazer');
  
  const currentState = new GeoJSON().writeFeatures(
    vectorSource.getFeatures(),
    { featureProjection: 'EPSG:3857' }
  );
  setUndoStack((prev) => [...prev, currentState]);
  
  const nextState = redoStack[redoStack.length - 1];
  setRedoStack((prev) => prev.slice(0, -1));
  
  const features = new GeoJSON().readFeatures(nextState, {
    featureProjection: 'EPSG:3857',
  });
  vectorSource.clear();
  vectorSource.addFeatures(features);
};

// OFFSET (Paralela)
export const applyOffset = (
  selectedFeature: any,
  vectorSource: VectorSource,
  offsetDistance: number,
  saveToUndoFn: () => void
) => {
  if (!selectedFeature) return alert('⚠️ Selecione uma feature (clique com Pan ativo)');
  
  const geom = selectedFeature.getGeometry();
  if (geom.getType() !== 'Polygon') return alert('⚠️ Offset só funciona com polígonos');
  
  saveToUndoFn();
  
  const coords = geom.getCoordinates()[0];
  const newCoords = coords.map((coord: number[], i: number) => {
    const prev = coords[i === 0 ? coords.length - 2 : i - 1];
    const next = coords[i === coords.length - 1 ? 1 : i + 1];
    
    const dx1 = coord[0] - prev[0];
    const dy1 = coord[1] - prev[1];
    const len1 = Math.sqrt(dx1 * dx1 + dy1 * dy1);
    
    const dx2 = next[0] - coord[0];
    const dy2 = next[1] - coord[1];
    const len2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
    
    const perpX = (-dy1 / len1 - dy2 / len2) / 2;
    const perpY = (dx1 / len1 + dx2 / len2) / 2;
    
    return [
      coord[0] + perpX * offsetDistance,
      coord[1] + perpY * offsetDistance,
    ];
  });
  
  const newFeature = selectedFeature.clone();
  newFeature.getGeometry().setCoordinates([newCoords]);
  vectorSource.addFeature(newFeature);
  
  alert(`✅ Paralela criada a ${offsetDistance}m`);
};

// ROTATE
export const applyRotate = (
  selectedFeature: any,
  vectorSource: VectorSource,
  rotateAngle: number,
  saveToUndoFn: () => void
) => {
  if (!selectedFeature) return alert('⚠️ Selecione uma feature primeiro');
  
  saveToUndoFn();
  
  const geom = selectedFeature.getGeometry();
  const extent = geom.getExtent();
  const center: [number, number] = [
    (extent[0] + extent[2]) / 2,
    (extent[1] + extent[3]) / 2,
  ];
  
  geom.rotate((rotateAngle * Math.PI) / 180, center);
  vectorSource.changed();
  
  alert(`✅ Rotacionado ${rotateAngle}° (anti-horário)`);
};

// SCALE
export const applyScale = (
  selectedFeature: any,
  vectorSource: VectorSource,
  scaleValue: number,
  saveToUndoFn: () => void
) => {
  if (!selectedFeature) return alert('⚠️ Selecione uma feature primeiro');
  
  saveToUndoFn();
  
  const geom = selectedFeature.getGeometry();
  const extent = geom.getExtent();
  const center: [number, number] = [
    (extent[0] + extent[2]) / 2,
    (extent[1] + extent[3]) / 2,
  ];
  
  geom.scale(scaleValue, scaleValue, center);
  vectorSource.changed();
  
  alert(`✅ Escala aplicada: ${scaleValue}x`);
};

// MIRROR
export const applyMirror = (
  selectedFeature: any,
  vectorSource: VectorSource,
  axis: 'x' | 'y',
  saveToUndoFn: () => void
) => {
  if (!selectedFeature) return alert('⚠️ Selecione uma feature primeiro');
  
  saveToUndoFn();
  
  const geom = selectedFeature.getGeometry();
  const extent = geom.getExtent();
  const centerX = (extent[0] + extent[2]) / 2;
  const centerY = (extent[1] + extent[3]) / 2;
  
  if (geom.getType() === 'Polygon') {
    const coords = geom.getCoordinates()[0];
    const mirrored = coords.map((coord: number[]) => {
      if (axis === 'x') {
        return [2 * centerX - coord[0], coord[1]];
      } else {
        return [coord[0], 2 * centerY - coord[1]];
      }
    });
    geom.setCoordinates([mirrored]);
  }
  
  vectorSource.changed();
  alert(`✅ Espelhado no eixo ${axis.toUpperCase()}`);
};

// TABELA DE COORDENADAS
export const exportCoordinates = (vectorSource: VectorSource) => {
  const features = vectorSource.getFeatures();
  if (features.length === 0) return alert('⚠️ Nenhuma feature para exportar');
  
  let table = 'PONTO\tEASTE (m)\tNORTE (m)\n';
  table += '='.repeat(50) + '\n';
  
  features.forEach((feature, idx) => {
    const geom = feature.getGeometry();
    if (geom && geom.getType() === 'Polygon') {
      const polygonGeom = geom as Polygon;
      const coords = polygonGeom.getCoordinates()[0];
      coords.slice(0, -1).forEach((coord: number[], i: number) => {
        table += `P${idx + 1}-V${i + 1}\t${coord[0].toFixed(2)}\t${coord[1].toFixed(2)}\n`;
      });
      table += '\n';
    }
  });
  
  navigator.clipboard.writeText(table);
  alert('✅ Tabela de coordenadas copiada para área de transferência!');
  return table;
};

// AZIMUTES E DISTÂNCIAS
export const calculateAzimuthsAndDistances = (vectorSource: VectorSource) => {
  const features = vectorSource.getFeatures();
  if (features.length === 0) return alert('⚠️ Nenhuma feature');
  
  let report = 'MEMORIAL DESCRITIVO - AZIMUTES E DISTÂNCIAS\n';
  report += '='.repeat(60) + '\n\n';
  
  features.forEach((feature, idx) => {
    const geom = feature.getGeometry();
    if (geom && geom.getType() === 'Polygon') {
      const polygonGeom = geom as Polygon;
      const coords = polygonGeom.getCoordinates()[0];
      report += `Lote ${idx + 1}:\n`;
      
      for (let i = 0; i < coords.length - 1; i++) {
        const p1 = coords[i];
        const p2 = coords[i + 1] || coords[0];
        
        const dx = p2[0] - p1[0];
        const dy = p2[1] - p1[1];
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        let azimuth = (Math.atan2(dx, dy) * 180) / Math.PI;
        if (azimuth < 0) azimuth += 360;
        
        const azDeg = Math.floor(azimuth);
        const azMin = Math.floor((azimuth - azDeg) * 60);
        const azSec = ((azimuth - azDeg - azMin / 60) * 3600).toFixed(1);
        
        report += `  P${i + 1} → P${i + 2}: Az ${azDeg}°${azMin}'${azSec}" - Dist: ${dist.toFixed(2)}m\n`;
      }
      report += '\n';
    }
  });
  
  navigator.clipboard.writeText(report);
  alert('✅ Memorial descritivo copiado para área de transferência!');
  return report;
};

// ENTRADA DE COORDENADAS DIRETAS
export const enterCoordinates = (
  vectorSource: VectorSource,
  map: any,
  saveToUndoFn: () => void
) => {
  const input = prompt(
    'Digite as coordenadas no formato: X1,Y1; X2,Y2; X3,Y3\nExemplo: 500000,7000000; 500100,7000000; 500100,7000100'
  );
  if (!input) return;
  
  try {
    const coords = input.split(';').map((pair) => {
      const [x, y] = pair.trim().split(',').map(Number);
      return [x, y];
    });
    
    if (coords.length < 3) throw new Error('Mínimo 3 pontos');
    
    saveToUndoFn();
    
    coords.push(coords[0]); // Fechar polígono
    
    const feature = new GeoJSON().readFeature(
      {
        type: 'Feature',
        geometry: { type: 'Polygon', coordinates: [coords] },
      },
      { featureProjection: 'EPSG:3857' }
    ) as Feature<Geometry>;
    
    vectorSource.addFeature(feature);
    
    if (map) {
      const extent = vectorSource.getExtent();
      map.getView().fit(extent, { padding: [50, 50, 50, 50] });
    }
    
    alert('✅ Polígono criado a partir das coordenadas!');
  } catch (err) {
    alert('❌ Formato inválido. Use: X1,Y1; X2,Y2; X3,Y3');
  }
};
