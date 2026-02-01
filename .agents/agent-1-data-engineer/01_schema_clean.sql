-- ===================================================================
-- ATIVO REAL - Database Schema (PostgreSQL)
-- Engenheiro de Dados: Agent 1
-- Date: 31/01/2026
-- Plataforma: Azure Database for PostgreSQL (Managed)
-- ===================================================================

-- Enums (CREATE IF NOT EXISTS not available for types, so we create or ignore error)
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('TOPOGRAFO', 'CLIENTE');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE tipo_projeto AS ENUM ('INDIVIDUAL', 'DESMEMBRAMENTO', 'LOTEAMENTO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE status_projeto AS ENUM ('RASCUNHO', 'ATIVO', 'CONCLUÍDO', 'CANCELADO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE status_lote AS ENUM ('PENDENTE', 'PAGO', 'PROCESSANDO', 'FINALIZADO', 'CANCELADO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE status_pagamento AS ENUM ('PENDENTE', 'PROCESSANDO', 'APROVADO', 'RECUSADO', 'REEMBOLSADO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Table: Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    role user_role NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Table: Projects (Trabalhos/Projetos)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    tipo tipo_projeto NOT NULL,
    status status_projeto NOT NULL DEFAULT 'RASCUNHO',
    geom_geojson JSONB,
    area_ha DECIMAL(12, 4),
    municipio VARCHAR(255),
    endereco TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_geom ON projects USING GIN(geom_geojson);

-- Table: Lots (Lotes)
CREATE TABLE lots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    nome_cliente VARCHAR(255) NOT NULL,
    cpf_cliente VARCHAR(14),
    email_cliente VARCHAR(255),
    telefone_cliente VARCHAR(20),
    token_acesso UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    link_expira_em TIMESTAMP,
    geom_geojson JSONB NOT NULL,
    area_ha DECIMAL(12, 4),
    status status_lote NOT NULL DEFAULT 'PENDENTE',
    metadata_validacao JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lots_project_id ON lots(project_id);
CREATE INDEX idx_lots_status ON lots(status);
CREATE INDEX idx_lots_token ON lots(token_acesso);
CREATE INDEX idx_lots_geom ON lots USING GIN(geom_geojson);

-- Table: WMS Layers (Visualização)
CREATE TABLE wms_layers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    url VARCHAR(1024) NOT NULL,
    tipo VARCHAR(50) DEFAULT 'WMS',
    visivel BOOLEAN DEFAULT TRUE,
    opacidade DECIMAL(3, 2) DEFAULT 1.00,
    ordem_exibicao INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_wms_layers_project ON wms_layers(project_id);

-- Table: Payments (Pagamentos)
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lot_id UUID NOT NULL REFERENCES lots(id) ON DELETE CASCADE,
    valor_total DECIMAL(12, 2) NOT NULL,
    valor_pago DECIMAL(12, 2) DEFAULT 0,
    status status_pagamento NOT NULL DEFAULT 'PENDENTE',
    gateway_id VARCHAR(255),
    gateway_resposta JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_lot_id ON payments(lot_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_gateway_id ON payments(gateway_id);

-- Table: Chat Messages (Mensagens)
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mensagem TEXT NOT NULL,
    attachments JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chat_project ON chat_messages(project_id);
CREATE INDEX idx_chat_sender ON chat_messages(sender_id);
CREATE INDEX idx_chat_created ON chat_messages(created_at);

-- Table: Audit Log (Auditoria)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tabela VARCHAR(100),
    operacao VARCHAR(10),
    record_id UUID,
    user_id UUID REFERENCES users(id),
    dados_anteriores JSONB,
    dados_novos JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_table ON audit_log(tabela);
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_created ON audit_log(created_at);

-- Trigger Function: Update Timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER trigger_users_updated BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER trigger_projects_updated BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER trigger_lots_updated BEFORE UPDATE ON lots FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER trigger_payments_updated BEFORE UPDATE ON payments FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER trigger_wms_layers_updated BEFORE UPDATE ON wms_layers FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER trigger_chat_updated BEFORE UPDATE ON chat_messages FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- ===================================================================
-- Fixtures: Test Data
-- ===================================================================

-- Users
INSERT INTO users (email, password_hash, nome, telefone, role) VALUES
    ('topografo@bemreal.com', '$2b$12$placeholder', 'João Topógrafo', '+55 11 98765-4321', 'TOPOGRAFO'),
    ('cliente1@email.com', '$2b$12$placeholder', 'Maria da Silva', '+55 11 91234-5678', 'CLIENTE'),
    ('cliente2@email.com', '$2b$12$placeholder', 'Pedro dos Santos', '+55 11 99876-5432', 'CLIENTE')
ON CONFLICT DO NOTHING;

-- Projects
INSERT INTO projects (user_id, nome, descricao, tipo, status, area_ha, municipio) VALUES
    (
        (SELECT id FROM users WHERE email = 'topografo@bemreal.com' LIMIT 1),
        'Loteamento Vila Nova',
        'Loteamento residencial com 20 lotes',
        'LOTEAMENTO',
        'ATIVO',
        5.5,
        'São Paulo'
    ),
    (
        (SELECT id FROM users WHERE email = 'topografo@bemreal.com' LIMIT 1),
        'Regularização Individual',
        'Regularização de propriedade rural',
        'INDIVIDUAL',
        'ATIVO',
        25.0,
        'Mogi-Mirim'
    )
ON CONFLICT DO NOTHING;

-- Lots
INSERT INTO lots (project_id, nome_cliente, cpf_cliente, email_cliente, geom_geojson, area_ha, status) VALUES
    (
        (SELECT id FROM projects WHERE nome = 'Loteamento Vila Nova' LIMIT 1),
        'Maria da Silva',
        '12345678901',
        'cliente1@email.com',
        '{"type": "Polygon", "coordinates": [[[-46.633309, -23.550520], [-46.632809, -23.550520], [-46.632809, -23.551020], [-46.633309, -23.551020], [-46.633309, -23.550520]]]}',
        0.25,
        'PENDENTE'
    ),
    (
        (SELECT id FROM projects WHERE nome = 'Loteamento Vila Nova' LIMIT 1),
        'Pedro dos Santos',
        '98765432101',
        'cliente2@email.com',
        '{"type": "Polygon", "coordinates": [[[-46.632809, -23.550520], [-46.632309, -23.550520], [-46.632309, -23.551020], [-46.632809, -23.551020], [-46.632809, -23.550520]]]}',
        0.25,
        'PENDENTE'
    )
ON CONFLICT DO NOTHING;

-- WMS Layers
INSERT INTO wms_layers (project_id, nome, url, tipo, visivel, opacidade) VALUES
    (
        (SELECT id FROM projects WHERE nome = 'Loteamento Vila Nova' LIMIT 1),
        'SIGEF',
        'https://sigef.incra.gov.br/wms',
        'WMS',
        TRUE,
        0.7
    ),
    (
        (SELECT id FROM projects WHERE nome = 'Loteamento Vila Nova' LIMIT 1),
        'CAR',
        'https://car.env.sp.gov.br/wms',
        'WMS',
        TRUE,
        0.5
    )
ON CONFLICT DO NOTHING;

-- ===================================================================
-- Verification Queries
-- ===================================================================

SELECT 'SCHEMA SUMMARY' as status,
       'Tables Created' as metric,
       COUNT(*) as count
FROM (
    SELECT 'users' as table_name UNION ALL
    SELECT 'projects' UNION ALL
    SELECT 'lots' UNION ALL
    SELECT 'payments' UNION ALL
    SELECT 'chat_messages' UNION ALL
    SELECT 'wms_layers' UNION ALL
    SELECT 'audit_log'
) AS tables;

SELECT 'DATA COUNT' as status,
       'users' as entity,
       COUNT(*) as count FROM users
UNION ALL
SELECT 'DATA COUNT', 'projects', COUNT(*) FROM projects
UNION ALL
SELECT 'DATA COUNT', 'lots', COUNT(*) FROM lots
UNION ALL
SELECT 'DATA COUNT', 'wms_layers', COUNT(*) FROM wms_layers;
