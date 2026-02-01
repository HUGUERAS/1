import React, { useState, useEffect } from 'react';

/**
 * WMSLayerManager.tsx
 * Gerenciador de camadas WMS para topógrafo (SIGEF, CAR, FUNAI)
 */

interface WMSLayer {
  id: number;
  projeto_id: number;
  name: string;
  url: string;
  visible: boolean;
  opacity: number;
}

interface WMSLayerManagerProps {
  projetoId: number;
  onLayersChange?: (layers: WMSLayer[]) => void;
}

const PRESET_LAYERS = [
  {
    name: 'SIGEF - Nacional',
    url: 'https://sigef.incra.gov.br/geo/wms',
  },
  {
    name: 'CAR - SICAR',
    url: 'https://www.car.gov.br/wms',
  },
  {
    name: 'FUNAI - Terras Indígenas',
    url: 'https://geoserver.funai.gov.br/geoserver/wms',
  },
];

export const WMSLayerManager: React.FC<WMSLayerManagerProps> = ({
  projetoId,
  onLayersChange,
}) => {
  const [layers, setLayers] = useState<WMSLayer[]>([]);
  const [loading, setLoading] = useState(false);
  const [newLayerName, setNewLayerName] = useState('');
  const [newLayerUrl, setNewLayerUrl] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    fetchLayers();
  }, [projetoId]);

  const fetchLayers = async () => {
    try {
      const response = await fetch(`/api/wms-layers?projeto_id=${projetoId}`);
      if (response.ok) {
        const data = await response.json();
        setLayers(data);
        if (onLayersChange) onLayersChange(data);
      }
    } catch (error) {
      console.error('Erro ao buscar camadas WMS:', error);
    }
  };

  const addLayer = async (name: string, url: string) => {
    setLoading(true);
    try {
      const response = await fetch('/api/wms-layers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projeto_id: projetoId,
          name,
          url,
          visible: true,
          opacity: 0.7,
        }),
      });

      if (response.ok) {
        await fetchLayers();
        setNewLayerName('');
        setNewLayerUrl('');
        setShowAddForm(false);
      }
    } catch (error) {
      console.error('Erro ao adicionar camada:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleVisibility = async (layerId: number, currentVisible: boolean) => {
    try {
      await fetch(`/api/wms-layers/${layerId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ visible: !currentVisible }),
      });
      await fetchLayers();
    } catch (error) {
      console.error('Erro ao atualizar visibilidade:', error);
    }
  };

  const updateOpacity = async (layerId: number, opacity: number) => {
    try {
      await fetch(`/api/wms-layers/${layerId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ opacity }),
      });
      await fetchLayers();
    } catch (error) {
      console.error('Erro ao atualizar opacidade:', error);
    }
  };

  const deleteLayer = async (layerId: number) => {
    if (!confirm('Deseja remover esta camada?')) return;

    try {
      await fetch(`/api/wms-layers/${layerId}`, { method: 'DELETE' });
      await fetchLayers();
    } catch (error) {
      console.error('Erro ao deletar camada:', error);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">🗺️ Camadas WMS</h3>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
        >
          {showAddForm ? '✕ Cancelar' : '+ Adicionar'}
        </button>
      </div>

      {/* Add Layer Form */}
      {showAddForm && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg space-y-3">
          <h4 className="font-medium text-sm">Nova Camada WMS</h4>

          {/* Preset Buttons */}
          <div className="space-y-2">
            <p className="text-xs text-gray-600">Camadas pré-configuradas:</p>
            <div className="flex flex-wrap gap-2">
              {PRESET_LAYERS.map((preset) => (
                <button
                  key={preset.name}
                  onClick={() => {
                    setNewLayerName(preset.name);
                    setNewLayerUrl(preset.url);
                  }}
                  className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded text-xs"
                >
                  {preset.name}
                </button>
              ))}
            </div>
          </div>

          <input
            type="text"
            placeholder="Nome da Camada"
            value={newLayerName}
            onChange={(e) => setNewLayerName(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          />

          <input
            type="url"
            placeholder="URL do Serviço WMS"
            value={newLayerUrl}
            onChange={(e) => setNewLayerUrl(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          />

          <button
            onClick={() => addLayer(newLayerName, newLayerUrl)}
            disabled={!newLayerName || !newLayerUrl || loading}
            className={`w-full py-2 rounded-md text-white ${loading || !newLayerName || !newLayerUrl
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-green-600 hover:bg-green-700'
              }`}
          >
            {loading ? 'Adicionando...' : 'Adicionar Camada'}
          </button>
        </div>
      )}

      {/* Layers List */}
      {layers.length === 0 ? (
        <p className="text-gray-500 text-sm text-center py-4">
          Nenhuma camada WMS adicionada ainda.
        </p>
      ) : (
        <div className="space-y-3">
          {layers.map((layer) => (
            <div key={layer.id} className="border rounded-lg p-3 space-y-2">
              {/* Header */}
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h4 className="font-medium text-sm">{layer.name}</h4>
                  <p className="text-xs text-gray-500 truncate">{layer.url}</p>
                </div>

                <div className="flex gap-2">
                  {/* Toggle Visibility */}
                  <button
                    onClick={() => toggleVisibility(layer.id, layer.visible)}
                    className={`px-3 py-1 rounded text-xs ${layer.visible
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-200 text-gray-600'
                      }`}
                  >
                    {layer.visible ? '👁️ Visível' : '🚫 Oculta'}
                  </button>

                  {/* Delete */}
                  <button
                    onClick={() => deleteLayer(layer.id)}
                    className="px-3 py-1 bg-red-100 text-red-700 rounded text-xs hover:bg-red-200"
                  >
                    🗑️
                  </button>
                </div>
              </div>

              {/* Opacity Slider */}
              <div>
                <label className="text-xs text-gray-600 block mb-1">
                  Opacidade: {Math.round(layer.opacity * 100)}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={layer.opacity}
                  onChange={(e) => updateOpacity(layer.id, parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
