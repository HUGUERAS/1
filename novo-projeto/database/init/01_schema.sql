-- 👴 Agente 1: Script de Inicialização do Banco de Dados
-- Garante a integridade matemática e espacial dos dados

-- Habilitar extensão PostGIS (Geometria e Geografia)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabela de Projetos (Agrupador)
CREATE TABLE IF NOT EXISTS projetos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Lotes/Glebas
-- SRID 4674 = SIRGAS 2000 (Padrão IBGE para o Brasil)
CREATE TABLE IF NOT EXISTS lotes (
    id SERIAL PRIMARY KEY,
    projeto_id INTEGER REFERENCES projetos(id),
    matricula VARCHAR(50),
    proprietario VARCHAR(100),
    
    -- Coluna Geométrica: Polígono
    geom GEOMETRY(POLYGON, 4674) NOT NULL,
    
    -- Metadados calculados
    area_ha NUMERIC(10, 4), -- Área calculada em Hectares
    
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index Espacial (Essencial para performance de queries de sobreposição)
CREATE INDEX idx_lotes_geom ON lotes USING GIST (geom);

-- CONSTRAINTS DE INTEGRIDADE --

-- 1. Garante que o polígono é válido (fechado, sem auto-interseção)
ALTER TABLE lotes ADD CONSTRAINT check_geom_valid 
CHECK (ST_IsValid(geom));

-- 2. (Opcional) Trigger para calcular área automaticamente ao inserir
CREATE OR REPLACE FUNCTION calc_area_ha() RETURNS TRIGGER AS $$
BEGIN
    -- Transforma para projeção métrica (Albers ou UTM) para cálculo de área preciso no Brasil
    -- Aqui usaremos uma aproximação casting para geography
    NEW.area_ha := ST_Area(NEW.geom::geography) / 10000.0;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calc_area
BEFORE INSERT OR UPDATE ON lotes
FOR EACH ROW EXECUTE FUNCTION calc_area_ha();
