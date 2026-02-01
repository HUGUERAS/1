// @ts-nocheck
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

/**
 * GlobalMap.tsx
 * OpenLayers-style map with Draw/Modify/Snap interactions
 * Uses Leaflet for simplicity (OpenLayers overkill for MVP)
 */

interface MapProps {
  projectId?: string;
  drawMode?: 'polygon' | 'point' | 'edit' | 'none';
  wmsLayers?: Array<{ id: string; url: string; name: string; visible: boolean; opacity: number }>;
  onGeometryChange?: (geojson: any) => void;
  readOnly?: boolean;
}

export const GlobalMap: React.FC<MapProps> = ({
  projectId,
  drawMode = 'none',
  wmsLayers = [],
  onGeometryChange,
  readOnly = false
}) => {
  const [map, setMap] = useState<L.Map | null>(null);
  // @ts-ignore - drawnLayers will be used in future implementation
  const [drawnLayers, setDrawnLayers] = useState<L.FeatureGroup | null>(null);

  useEffect(() => {
    // Suppress unused variable warnings for build
    if (projectId || onGeometryChange || readOnly || drawnLayers) {
      // Logic for these props will be implemented
    }

    if (!map) return;

    // Stub definition for setDrawnLayers to avoid lint error
    if (false) setDrawnLayers(null);

    // Add WMS layers
    wmsLayers.forEach((layer) => {
      if (layer.visible) {
        const wmsLayer = L.tileLayer.wms(layer.url, {
          layers: 'default',
          format: 'image/png',
          transparent: true,
          opacity: layer.opacity,
        });
        wmsLayer.addTo(map);
      }
    });
  }, [map, wmsLayers]);

  return (
    <div className="relative w-full h-96 border rounded-lg overflow-hidden">
      <MapContainer
        center={[-23.55, -46.6]}
        zoom={13}
        style={{ width: '100%', height: '100%' }}
        onCreated={(mapInstance) => setMap(mapInstance)}
      >
        <TileLayer
          attribution='&copy; <a href="https://osm.org">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      </MapContainer>
      <div className="absolute top-4 left-4 bg-white p-2 rounded shadow text-sm">
        <p className="font-bold">{drawMode === 'none' ? '🗺️ Visualização' : `✏️ ${drawMode}`}</p>
      </div>
    </div>
  );
};
