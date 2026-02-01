import React, { useState } from 'react';

/**
 * FileUploader.tsx
 * Upload de arquivos geoespaciais (KML, GeoJSON, Shapefile, Excel)
 */

interface FileUploaderProps {
  loteId: number;
  onUploadSuccess?: (file: any) => void;
}

const ALLOWED_TYPES = {
  'application/vnd.google-earth.kml+xml': 'KML',
  'application/json': 'GEOJSON',
  'application/x-zip-compressed': 'SHAPEFILE',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'EXCEL',
  'application/pdf': 'PDF',
};

export const FileUploader: React.FC<FileUploaderProps> = ({ loteId, onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setError(null);
    setProgress(0);

    // Validar tipo de arquivo
    const fileType = Object.entries(ALLOWED_TYPES).find(([mime]) =>
      file.type.includes(mime) || file.name.endsWith(mime.split('/').pop() || '')
    );

    if (!fileType) {
      setError('Tipo de arquivo não suportado. Use KML, GeoJSON, Shapefile, Excel ou PDF.');
      return;
    }

    const [_, tipoArquivo] = fileType;

    // Verificar tamanho (limite 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('Arquivo muito grande. Limite: 5MB');
      return;
    }

    setUploading(true);

    try {
      // Converter para Base64
      const base64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          const result = reader.result as string;
          resolve(result.split(',')[1]); // Remove "data:..." prefix
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });

      // Upload para backend
      const response = await fetch('/api/arquivos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lote_id: loteId,
          nome: file.name,
          tipo: tipoArquivo,
          tamanho_kb: Math.round(file.size / 1024),
          conteudo_base64: base64,
          metadata: {
            original_name: file.name,
            upload_date: new Date().toISOString(),
          },
        }),
      });

      if (!response.ok) {
        throw new Error('Erro ao fazer upload');
      }

      const uploadedFile = await response.json();
      setProgress(100);

      if (onUploadSuccess) {
        onUploadSuccess(uploadedFile);
      }

      // Reset após 2s
      setTimeout(() => {
        setUploading(false);
        setProgress(0);
      }, 2000);
    } catch (err) {
      setError('Erro ao fazer upload. Tente novamente.');
      setUploading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">📂 Upload de Arquivos</h3>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <input
          type="file"
          id="file-upload"
          className="hidden"
          onChange={handleFileUpload}
          accept=".kml,.geojson,.json,.zip,.shp,.xlsx,.xls,.pdf"
          disabled={uploading}
        />

        <label
          htmlFor="file-upload"
          className={`cursor-pointer inline-block px-6 py-3 rounded-md text-white font-medium ${uploading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'
            }`}
        >
          {uploading ? 'Enviando...' : '📤 Selecionar Arquivo'}
        </label>

        <p className="text-sm text-gray-500 mt-3">
          Formatos suportados: KML, GeoJSON, Shapefile, Excel, PDF
        </p>
        <p className="text-xs text-gray-400">Tamanho máximo: 5MB</p>

        {/* Progress Bar */}
        {uploading && (
          <div className="mt-4">
            <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className="bg-blue-600 h-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 mt-2">{progress}% concluído</p>
          </div>
        )}

        {/* Success */}
        {progress === 100 && !uploading && (
          <div className="mt-4 text-green-600 font-medium">
            ✅ Upload concluído com sucesso!
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 text-red-600 text-sm">
            ❌ {error}
          </div>
        )}
      </div>

      {/* File Type Icons */}
      <div className="mt-6 grid grid-cols-5 gap-3 text-center text-xs">
        <div>
          <div className="text-2xl">📍</div>
          <div className="text-gray-600">KML</div>
        </div>
        <div>
          <div className="text-2xl">🗺️</div>
          <div className="text-gray-600">GeoJSON</div>
        </div>
        <div>
          <div className="text-2xl">📦</div>
          <div className="text-gray-600">Shapefile</div>
        </div>
        <div>
          <div className="text-2xl">📊</div>
          <div className="text-gray-600">Excel</div>
        </div>
        <div>
          <div className="text-2xl">📄</div>
          <div className="text-gray-600">PDF</div>
        </div>
      </div>
    </div>
  );
};
