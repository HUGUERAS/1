-- Script de Features Completas (WMS, Chat, Timeline, Arquivos)
-- Criado: 2026-02-01

-- ==================== WMS LAYERS ====================
-- Permite ao topógrafo adicionar camadas WMS (SIGEF, CAR, FUNAI)
CREATE TABLE
IF NOT EXISTS wms_layers
(
    id SERIAL PRIMARY KEY,
    projeto_id INTEGER REFERENCES projetos
(id) ON
DELETE CASCADE,
    name VARCHAR(100)
NOT NULL,
    url TEXT NOT NULL,
    visible BOOLEAN DEFAULT true,
    opacity NUMERIC
(3, 2) DEFAULT 1.0 CHECK
(opacity >= 0 AND opacity <= 1),
    
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX
IF NOT EXISTS idx_wms_projeto ON wms_layers
(projeto_id);

-- ==================== CHAT MESSAGES ====================
-- Chat simples entre topógrafo e cliente
CREATE TABLE
IF NOT EXISTS chat_messages
(
    id SERIAL PRIMARY KEY,
    projeto_id INTEGER REFERENCES projetos
(id) ON
DELETE CASCADE,
    sender_id INTEGER
REFERENCES users
(id),
    sender_role VARCHAR
(20) NOT NULL, -- TOPOGRAFO, CLIENTE
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX
IF NOT EXISTS idx_chat_projeto ON chat_messages
(projeto_id);
CREATE INDEX
IF NOT EXISTS idx_chat_created ON chat_messages
(criado_em DESC);

-- ==================== STATUS HISTORY ====================
-- Rastreio de mudanças de status (Timeline)
CREATE TABLE
IF NOT EXISTS status_history
(
    id SERIAL PRIMARY KEY,
    lote_id INTEGER REFERENCES lotes
(id) ON
DELETE CASCADE,
    status_anterior status_lote,
    status_novo status_lote
NOT NULL,
    observacao TEXT,
    alterado_por INTEGER REFERENCES users
(id),
    
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX
IF NOT EXISTS idx_status_lote ON status_history
(lote_id);

-- ==================== ARQUIVOS (JSONB) ====================
-- Armazena metadados de arquivos (KML, GeoJSON, PDF, Excel)
-- Conteúdo pequeno vai em Base64, grande vai em URL externa
CREATE TABLE
IF NOT EXISTS arquivos
(
    id SERIAL PRIMARY KEY,
    lote_id INTEGER REFERENCES lotes
(id) ON
DELETE CASCADE,
    nome VARCHAR(200)
NOT NULL,
    tipo VARCHAR
(50) NOT NULL, -- KML, GEOJSON, PDF, EXCEL, SHAPEFILE
    tamanho_kb INTEGER,
    conteudo_base64 TEXT, -- Para arquivos < 1MB
    url_externa TEXT, -- Para arquivos grandes (futura integração Blob)
    metadata JSONB, -- Coordenadas, features, etc
    
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX
IF NOT EXISTS idx_arquivos_lote ON arquivos
(lote_id);

-- ==================== GLEBA MÃE (Geometria do Projeto) ====================
-- Adiciona geometria à tabela projetos
ALTER TABLE projetos ADD COLUMN
IF NOT EXISTS geom GEOMETRY
(POLYGON, 4674);
CREATE INDEX
IF NOT EXISTS idx_projetos_geom ON projetos USING GIST
(geom);

-- ==================== TRIGGERS ====================

-- Trigger: Atualizar updated_at em WMS Layers
DROP TRIGGER IF EXISTS trigger_update_wms
ON wms_layers;
CREATE TRIGGER trigger_update_wms 
BEFORE
UPDATE ON wms_layers 
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at
();

-- Trigger: Registrar mudança de status automaticamente
CREATE OR REPLACE FUNCTION log_status_change
()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
    INSERT INTO status_history
        (lote_id, status_anterior, status_novo)
    VALUES
        (NEW.id, OLD.status, NEW.status);
END
IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_log_status
ON lotes;
CREATE TRIGGER trigger_log_status 
AFTER
UPDATE ON lotes 
FOR EACH ROW
EXECUTE FUNCTION log_status_change
();

-- ==================== FUNCAO CALC_AREA_HA ====================
-- (Referenciada no 01_schema.sql mas não estava definida)
CREATE OR REPLACE FUNCTION calc_area_ha
()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.geom IS NOT NULL THEN
        -- Calcula área em hectares usando geografia geodésica
        NEW.area_ha = ST_Area
    (NEW.geom::geography) / 10000.0;
NEW.perimetro_m = ST_Perimeter
(NEW.geom::geography);
END
IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
