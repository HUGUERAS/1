-- 💳 Migration: Pay As You Go (Assinaturas Recorrentes)
-- Adiciona suporte para modelo de assinatura com diferentes planos
-- Autor: GitHub Copilot
-- Data: 31/01/2026

-- =====================================================
-- 1. ENUM para Status de Assinatura
-- =====================================================
DO $$ BEGIN
    CREATE TYPE status_assinatura AS ENUM (
        'TRIAL',           -- Trial gratuito (30 dias)
        'PENDENTE',        -- Aguardando pagamento
        'ATIVA',           -- Assinatura ativa
        'CANCELADA',       -- Cancelada pelo usuário
        'SUSPENSA',        -- Suspensa por falta de pagamento
        'EXPIRADA'         -- Trial/assinatura expirada
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- =====================================================
-- 2. Tabela de Planos de Pagamento
-- =====================================================
CREATE TABLE IF NOT EXISTS planos_pagamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,  -- FREE, BASICO, PROFISSIONAL, ENTERPRISE
    descricao TEXT,
    preco_mensal NUMERIC(10, 2) NOT NULL DEFAULT 0,
    
    -- Limites de Uso
    max_projetos INTEGER DEFAULT -1,  -- -1 = ilimitado
    max_lotes_por_projeto INTEGER DEFAULT -1,
    storage_mb INTEGER DEFAULT 100,
    
    -- Recursos/Features
    permite_export_kml BOOLEAN DEFAULT FALSE,
    permite_export_shp BOOLEAN DEFAULT FALSE,
    permite_export_dxf BOOLEAN DEFAULT FALSE,
    permite_api_access BOOLEAN DEFAULT FALSE,
    
    -- Metadata flexível para features futuras
    features JSONB,
    
    -- Controle
    ativo BOOLEAN DEFAULT TRUE,
    ordem_exibicao INTEGER DEFAULT 0,  -- Para ordenar na UI
    
    -- Auditoria
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 3. Tabela de Assinaturas
-- =====================================================
CREATE TABLE IF NOT EXISTS assinaturas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES lotes(id),  -- Vincula ao topógrafo/cliente
    plano_id INTEGER REFERENCES planos_pagamento(id),
    
    -- Status e Ciclo de Vida
    status status_assinatura NOT NULL DEFAULT 'TRIAL',
    
    -- Datas Importantes
    inicio_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expira_em TIMESTAMP,  -- Data de expiração do período atual
    cancelada_em TIMESTAMP,
    suspensa_em TIMESTAMP,
    proximo_pagamento TIMESTAMP,  -- Próxima cobrança programada
    
    -- Integração com Gateway de Pagamento
    gateway_subscription_id VARCHAR(100),  -- ID na InfinitePay/Stripe
    gateway_customer_id VARCHAR(100),      -- ID do cliente no gateway
    metodo_pagamento VARCHAR(20),          -- PIX, CARTAO, BOLETO
    
    -- Histórico e Auditoria
    metadata JSONB,  -- {upgrades: [], downgrades: [], payments: []}
    tentativas_cobranca INTEGER DEFAULT 0,
    ultima_tentativa_cobranca TIMESTAMP,
    
    -- Timestamps
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT check_expira_em CHECK (expira_em IS NULL OR expira_em > inicio_em)
);

-- =====================================================
-- 4. Tabela de Histórico de Assinaturas
-- =====================================================
CREATE TABLE IF NOT EXISTS historico_assinaturas (
    id SERIAL PRIMARY KEY,
    assinatura_id INTEGER REFERENCES assinaturas(id) ON DELETE CASCADE,
    
    -- Ação Realizada
    acao VARCHAR(50) NOT NULL,  -- CRIADA, RENOVADA, UPGRADE, DOWNGRADE, CANCELADA, SUSPENSA
    
    -- Mudança de Plano (se aplicável)
    plano_anterior_id INTEGER REFERENCES planos_pagamento(id),
    plano_novo_id INTEGER REFERENCES planos_pagamento(id),
    
    -- Valores
    valor_pago NUMERIC(10, 2),
    
    -- Detalhes Adicionais
    detalhes JSONB,  -- Informações extras sobre a ação
    
    -- Auditoria
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    criado_por VARCHAR(100)  -- Email/ID do usuário que fez a ação
);

-- =====================================================
-- 5. Índices para Performance
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_assinaturas_usuario ON assinaturas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_assinaturas_status ON assinaturas(status);
CREATE INDEX IF NOT EXISTS idx_assinaturas_expira ON assinaturas(expira_em);
CREATE INDEX IF NOT EXISTS idx_assinaturas_proximo_pagamento ON assinaturas(proximo_pagamento);
CREATE INDEX IF NOT EXISTS idx_assinaturas_gateway ON assinaturas(gateway_subscription_id);

CREATE INDEX IF NOT EXISTS idx_historico_assinatura ON historico_assinaturas(assinatura_id);
CREATE INDEX IF NOT EXISTS idx_historico_criado_em ON historico_assinaturas(criado_em);

CREATE INDEX IF NOT EXISTS idx_planos_ativo ON planos_pagamento(ativo);
CREATE INDEX IF NOT EXISTS idx_planos_ordem ON planos_pagamento(ordem_exibicao);

-- =====================================================
-- 6. Triggers para Atualizar Timestamps
-- =====================================================
-- Trigger para atualizar 'atualizado_em' na tabela planos_pagamento
DROP TRIGGER IF EXISTS trigger_update_planos_pagamento ON planos_pagamento;
CREATE TRIGGER trigger_update_planos_pagamento 
    BEFORE UPDATE ON planos_pagamento 
    FOR EACH ROW 
    EXECUTE PROCEDURE update_updated_at();

-- Trigger para atualizar 'atualizado_em' na tabela assinaturas
DROP TRIGGER IF EXISTS trigger_update_assinaturas ON assinaturas;
CREATE TRIGGER trigger_update_assinaturas 
    BEFORE UPDATE ON assinaturas 
    FOR EACH ROW 
    EXECUTE PROCEDURE update_updated_at();

-- =====================================================
-- 7. Dados Iniciais (Seed)
-- =====================================================
-- Inserir planos padrão
INSERT INTO planos_pagamento (nome, descricao, preco_mensal, max_projetos, max_lotes_por_projeto, storage_mb, ordem_exibicao, features)
VALUES 
    ('FREE', 'Plano gratuito para teste', 0, 2, 10, 100, 1, 
     '{"api_rate_limit": 100, "export_formats": ["PDF"], "support": "email"}'::jsonb),
    
    ('BASICO', 'Ideal para pequenos topógrafos', 99, 10, 50, 1024, 2,
     '{"api_rate_limit": 500, "export_formats": ["PDF", "KML"], "support": "email+chat", "permite_export_kml": true}'::jsonb),
    
    ('PROFISSIONAL', 'Para topógrafos profissionais', 299, 50, 200, 10240, 3,
     '{"api_rate_limit": 2000, "export_formats": ["PDF", "KML", "SHP", "DXF"], "support": "email+chat+phone", "permite_export_kml": true, "permite_export_shp": true, "permite_export_dxf": true}'::jsonb),
    
    ('ENTERPRISE', 'Sem limites para grandes operações', 999, -1, -1, 102400, 4,
     '{"api_rate_limit": -1, "export_formats": ["PDF", "KML", "SHP", "DXF", "GeoJSON"], "support": "dedicated+whatsapp", "permite_export_kml": true, "permite_export_shp": true, "permite_export_dxf": true, "permite_api_access": true}'::jsonb)
ON CONFLICT (nome) DO NOTHING;

-- =====================================================
-- 8. Funções Auxiliares
-- =====================================================

-- Função para verificar se assinatura está ativa
CREATE OR REPLACE FUNCTION assinatura_esta_ativa(p_usuario_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 
        FROM assinaturas 
        WHERE usuario_id = p_usuario_id 
          AND status = 'ATIVA'
          AND (expira_em IS NULL OR expira_em > CURRENT_TIMESTAMP)
    );
END;
$$ LANGUAGE plpgsql;

-- Função para obter limites do plano ativo
CREATE OR REPLACE FUNCTION obter_limites_plano(p_usuario_id INTEGER)
RETURNS TABLE (
    max_projetos INTEGER,
    max_lotes INTEGER,
    storage_mb INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.max_projetos,
        p.max_lotes_por_projeto,
        p.storage_mb
    FROM assinaturas a
    JOIN planos_pagamento p ON a.plano_id = p.id
    WHERE a.usuario_id = p_usuario_id
      AND a.status = 'ATIVA'
      AND (a.expira_em IS NULL OR a.expira_em > CURRENT_TIMESTAMP)
    ORDER BY a.criado_em DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Função para registrar evento no histórico
CREATE OR REPLACE FUNCTION registrar_evento_assinatura(
    p_assinatura_id INTEGER,
    p_acao VARCHAR(50),
    p_plano_anterior_id INTEGER DEFAULT NULL,
    p_plano_novo_id INTEGER DEFAULT NULL,
    p_valor_pago NUMERIC(10, 2) DEFAULT NULL,
    p_detalhes JSONB DEFAULT NULL,
    p_criado_por VARCHAR(100) DEFAULT 'system'
)
RETURNS INTEGER AS $$
DECLARE
    v_historico_id INTEGER;
BEGIN
    INSERT INTO historico_assinaturas (
        assinatura_id, 
        acao, 
        plano_anterior_id, 
        plano_novo_id, 
        valor_pago, 
        detalhes, 
        criado_por
    )
    VALUES (
        p_assinatura_id,
        p_acao,
        p_plano_anterior_id,
        p_plano_novo_id,
        p_valor_pago,
        p_detalhes,
        p_criado_por
    )
    RETURNING id INTO v_historico_id;
    
    RETURN v_historico_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 9. Views Úteis
-- =====================================================

-- View de assinaturas ativas com detalhes do plano
CREATE OR REPLACE VIEW v_assinaturas_ativas AS
SELECT 
    a.id as assinatura_id,
    a.usuario_id,
    a.status,
    a.inicio_em,
    a.expira_em,
    a.proximo_pagamento,
    p.id as plano_id,
    p.nome as plano_nome,
    p.preco_mensal,
    p.max_projetos,
    p.max_lotes_por_projeto,
    p.storage_mb,
    CASE 
        WHEN a.expira_em IS NULL THEN 999999
        WHEN a.expira_em > CURRENT_TIMESTAMP THEN EXTRACT(DAY FROM (a.expira_em - CURRENT_TIMESTAMP))
        ELSE 0
    END as dias_restantes
FROM assinaturas a
JOIN planos_pagamento p ON a.plano_id = p.id
WHERE a.status IN ('ATIVA', 'TRIAL');

-- View de métricas de negócio
CREATE OR REPLACE VIEW v_metricas_assinaturas AS
SELECT 
    COUNT(*) FILTER (WHERE status = 'ATIVA') as assinaturas_ativas,
    COUNT(*) FILTER (WHERE status = 'TRIAL') as assinaturas_trial,
    COUNT(*) FILTER (WHERE status = 'CANCELADA') as assinaturas_canceladas,
    SUM(p.preco_mensal) FILTER (WHERE a.status = 'ATIVA') as mrr_total,
    AVG(p.preco_mensal) FILTER (WHERE a.status = 'ATIVA') as ticket_medio
FROM assinaturas a
LEFT JOIN planos_pagamento p ON a.plano_id = p.id;

-- =====================================================
-- 10. Comentários nas Tabelas (Documentação)
-- =====================================================
COMMENT ON TABLE planos_pagamento IS 'Planos de assinatura disponíveis no sistema';
COMMENT ON TABLE assinaturas IS 'Assinaturas ativas/inativas dos usuários';
COMMENT ON TABLE historico_assinaturas IS 'Log de todas as alterações em assinaturas';

COMMENT ON COLUMN planos_pagamento.max_projetos IS '-1 indica ilimitado';
COMMENT ON COLUMN assinaturas.expira_em IS 'Data de expiração do período atual pago';
COMMENT ON COLUMN assinaturas.proximo_pagamento IS 'Data da próxima tentativa de cobrança';

-- =====================================================
-- ✅ Migration Completa
-- =====================================================
-- Para aplicar: psql -d ativoreal_geo -f 03_pay_as_you_go_schema.sql
