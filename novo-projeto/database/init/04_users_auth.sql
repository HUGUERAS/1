-- 🔐 Migration: Sistema de Autenticação JWT
-- Adiciona tabela de usuários com roles e autenticação segura
-- Autor: GitHub Copilot - Refatoração Single-Page
-- Data: 31/01/2026

-- =====================================================
-- 1. ENUM para Roles de Usuário
-- =====================================================
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM (
        'ADMIN',           -- Administrador do sistema
        'TOPOGRAFO',       -- Topógrafo/Engenheiro
        'CLIENTE',         -- Proprietário de terra (cliente)
        'AGRICULTOR'       -- Agricultor/Produtor rural
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- =====================================================
-- 2. Tabela de Usuários
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'CLIENTE',
    
    -- Perfil
    avatar VARCHAR(500),
    telefone VARCHAR(20),
    cpf_cnpj VARCHAR(20),
    
    -- Controle de Acesso
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP,
    
    -- Timestamps
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP,
    
    -- Constraints
    CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT check_name_length CHECK (LENGTH(name) >= 3)
);

-- =====================================================
-- 3. Índices para Performance
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_email_verified ON users(email_verified);
CREATE INDEX IF NOT EXISTS idx_users_ultimo_login ON users(ultimo_login);

-- =====================================================
-- 4. Trigger para Atualizar Timestamps
-- =====================================================
CREATE OR REPLACE FUNCTION update_users_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_users ON users;
CREATE TRIGGER trigger_update_users 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE PROCEDURE update_users_timestamp();

-- =====================================================
-- 5. Atualizar Tabelas Existentes
-- =====================================================

-- Adicionar relacionamento em projetos
ALTER TABLE projetos 
ADD COLUMN IF NOT EXISTS criado_por INTEGER REFERENCES users(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_projetos_criado_por ON projetos(criado_por);

-- Atualizar relacionamento em assinaturas
DO $$ 
BEGIN
    -- Remove coluna antiga se existir
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assinaturas' AND column_name = 'usuario_id' 
        AND data_type != 'integer'
    ) THEN
        ALTER TABLE assinaturas DROP COLUMN usuario_id;
    END IF;
END $$;

ALTER TABLE assinaturas 
ADD COLUMN IF NOT EXISTS usuario_id INTEGER REFERENCES users(id) ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS idx_assinaturas_usuario_id ON assinaturas(usuario_id);

-- Adicionar relacionamento em lotes (para tracking de quem criou)
ALTER TABLE lotes 
ADD COLUMN IF NOT EXISTS criado_por INTEGER REFERENCES users(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_lotes_criado_por ON lotes(criado_por);

-- =====================================================
-- 6. Funções Auxiliares
-- =====================================================

-- Função para obter usuário por email
CREATE OR REPLACE FUNCTION get_user_by_email(p_email VARCHAR)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    role user_role,
    is_active BOOLEAN,
    email_verified BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.name,
        u.email,
        u.role,
        u.is_active,
        u.email_verified
    FROM users u
    WHERE u.email = p_email;
END;
$$ LANGUAGE plpgsql;

-- Função para verificar se email já existe
CREATE OR REPLACE FUNCTION email_exists(p_email VARCHAR)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (SELECT 1 FROM users WHERE email = p_email);
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar último login
CREATE OR REPLACE FUNCTION update_last_login(p_user_id INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE users 
    SET ultimo_login = CURRENT_TIMESTAMP 
    WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 7. View de Usuários Ativos
-- =====================================================
CREATE OR REPLACE VIEW v_usuarios_ativos AS
SELECT 
    u.id,
    u.name,
    u.email,
    u.role,
    u.avatar,
    u.telefone,
    u.email_verified,
    u.criado_em,
    u.ultimo_login,
    COUNT(DISTINCT p.id) as total_projetos,
    COUNT(DISTINCT l.id) as total_lotes,
    a.id as assinatura_id,
    pl.nome as plano_nome
FROM users u
LEFT JOIN projetos p ON p.criado_por = u.id
LEFT JOIN lotes l ON l.criado_por = u.id
LEFT JOIN assinaturas a ON a.usuario_id = u.id AND a.status = 'ATIVA'
LEFT JOIN planos_pagamento pl ON a.plano_id = pl.id
WHERE u.is_active = TRUE
GROUP BY u.id, u.name, u.email, u.role, u.avatar, u.telefone, u.email_verified, 
         u.criado_em, u.ultimo_login, a.id, pl.nome;

-- =====================================================
-- 8. Tabela de Sessões (Opcional - para invalidar tokens)
-- =====================================================
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revogado BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT check_expires_future CHECK (expires_at > criado_em)
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_sessions_revogado ON user_sessions(revogado);

-- Limpar sessões expiradas automaticamente
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM user_sessions 
    WHERE expires_at < CURRENT_TIMESTAMP OR revogado = TRUE;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 9. Dados Iniciais (Seed)
-- =====================================================

-- Usuário ADMIN padrão
-- Email: admin@ativoreal.com.br
-- Senha: Admin@2026! (DEVE SER ALTERADA NA PRIMEIRA LOGIN EM PRODUÇÃO!)
-- Hash gerado com bcrypt rounds=12
INSERT INTO users (name, email, password_hash, role, is_active, email_verified)
VALUES (
    'Administrador do Sistema',
    'admin@ativoreal.com.br',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5/d8xQK8wd92u',
    'ADMIN',
    TRUE,
    TRUE
)
ON CONFLICT (email) DO NOTHING;

-- Usuário TOPOGRAFO de teste (desenvolvimento)
-- Email: topografo@teste.com
-- Senha: Topo@123
INSERT INTO users (name, email, password_hash, role, is_active, email_verified)
VALUES (
    'João Topógrafo',
    'topografo@teste.com',
    '$2b$12$EjhBdQcHYvgZ8Wkf3z8TYOvMYjKqXGZ5kN7qWzJxL8vZ9R3kL1mJO',
    'TOPOGRAFO',
    TRUE,
    TRUE
)
ON CONFLICT (email) DO NOTHING;

-- Usuário CLIENTE de teste
-- Email: cliente@teste.com
-- Senha: Cliente@123
INSERT INTO users (name, email, password_hash, role, is_active, email_verified)
VALUES (
    'Maria Proprietária',
    'cliente@teste.com',
    '$2b$12$DcgAeRbGXuYf7Vjd2y7SPeu1IiJpWfG4jM6nVxIwN7tY8Q2jK0lNG',
    'CLIENTE',
    TRUE,
    TRUE
)
ON CONFLICT (email) DO NOTHING;

-- =====================================================
-- 10. Políticas de Segurança
-- =====================================================

-- Revogar acesso público às tabelas sensíveis
REVOKE ALL ON users FROM PUBLIC;
REVOKE ALL ON user_sessions FROM PUBLIC;

-- Criar role para aplicação (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ativo_real_app') THEN
        CREATE ROLE ativo_real_app WITH LOGIN PASSWORD 'change-this-password-in-production';
    END IF;
END
$$;

-- Conceder permissões necessárias
GRANT SELECT, INSERT, UPDATE ON users TO ativo_real_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_sessions TO ativo_real_app;
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO ativo_real_app;
GRANT USAGE, SELECT ON SEQUENCE user_sessions_id_seq TO ativo_real_app;

-- =====================================================
-- 11. Comentários nas Tabelas (Documentação)
-- =====================================================
COMMENT ON TABLE users IS 'Usuários do sistema com autenticação JWT e RBAC';
COMMENT ON TABLE user_sessions IS 'Sessões ativas com refresh tokens para invalidação';

COMMENT ON COLUMN users.password_hash IS 'Hash bcrypt da senha (rounds=12)';
COMMENT ON COLUMN users.role IS 'Perfil de acesso: ADMIN, TOPOGRAFO, CLIENTE, AGRICULTOR';
COMMENT ON COLUMN users.email_verified IS 'Se o email foi verificado via token';
COMMENT ON COLUMN users.is_active IS 'Se a conta está ativa (pode fazer login)';
COMMENT ON COLUMN users.ultimo_login IS 'Timestamp do último login bem-sucedido';

COMMENT ON COLUMN user_sessions.refresh_token_hash IS 'Hash do refresh token (não armazena token em plain text)';
COMMENT ON COLUMN user_sessions.revogado IS 'Se o token foi revogado manualmente (logout)';

-- =====================================================
-- 12. Trigger para Log de Auditoria (Opcional)
-- =====================================================
CREATE TABLE IF NOT EXISTS user_audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    acao VARCHAR(50) NOT NULL,
    ip_address VARCHAR(45),
    detalhes JSONB,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_user_id ON user_audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_criado_em ON user_audit_log(criado_em);

-- Função para registrar auditoria
CREATE OR REPLACE FUNCTION log_user_action(
    p_user_id INTEGER,
    p_acao VARCHAR,
    p_ip_address VARCHAR DEFAULT NULL,
    p_detalhes JSONB DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO user_audit_log (user_id, acao, ip_address, detalhes)
    VALUES (p_user_id, p_acao, p_ip_address, p_detalhes);
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- ✅ Migration Completa
-- =====================================================
-- Para aplicar: psql -d ativoreal_geo -f 04_users_auth.sql
-- 
-- USUÁRIOS PADRÃO CRIADOS:
-- 1. admin@ativoreal.com.br / Admin@2026! (ADMIN)
-- 2. topografo@teste.com / Topo@123 (TOPOGRAFO)
-- 3. cliente@teste.com / Cliente@123 (CLIENTE)
--
-- ⚠️ IMPORTANTE: Altere as senhas padrão em produção!
-- ⚠️ Configure JWT_SECRET_KEY nas variáveis de ambiente do Azure Functions
