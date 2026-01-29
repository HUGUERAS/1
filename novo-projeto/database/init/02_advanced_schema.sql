-- 👴 Agente 1: Atualização do Schema para Suporte a Projetos Pai e Validação SIGEF

-- Tabela de Referência Oficial (SIGEF/INCRA)
-- Esta tabela deve ser populada via ETL com os shapefiles do INCRA
CREATE TABLE IF NOT EXISTS sigef_incra (
    id SERIAL PRIMARY KEY,
    codigo_imovel VARCHAR(50),
    detentor VARCHAR(200),
    geom GEOMETRY(POLYGON, 4674) -- SIRGAS 2000
);
CREATE INDEX IF NOT EXISTS idx_sigef_geom ON sigef_incra USING GIST (geom);

-- Alteração na Tabela Projetos para ter Geometria (A Fazenda Mãe)
ALTER TABLE projetos ADD COLUMN IF NOT EXISTS geom GEOMETRY(POLYGON, 4674);
ALTER TABLE projetos ADD COLUMN IF NOT EXISTS matricula_mae VARCHAR(50);
CREATE INDEX IF NOT EXISTS idx_projetos_geom ON projetos USING GIST (geom);

-- Constraints Avançadas (Regras de Ouro)

-- Regra: Lotes não podem sobrepor áreas certificadas do SIGEF
-- (Essa validação é complexa demais para Check Constraint simples, faremos na trigger ou APP)

-- Regra: Lotes devem estar contidos (ST_Within) na geometria do Projeto Pai (se existir)
-- Implementado via Trigger para performance/flexibilidade
CREATE OR REPLACE FUNCTION check_lote_within_project() RETURNS TRIGGER AS $$
DECLARE
    project_geom GEOMETRY;
BEGIN
    IF NEW.projeto_id IS NOT NULL THEN
        SELECT geom INTO project_geom FROM projetos WHERE id = NEW.projeto_id;
        
        -- Se o projeto tem geometria definida, o lote tem que estar dentro
        IF project_geom IS NOT NULL AND NOT ST_CoveredBy(NEW.geom, project_geom) THEN
            RAISE EXCEPTION 'Violação Espacial: O lote desenhado excede os limites da fazenda original (Projeto Pai).';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_lote_project ON lotes;
CREATE TRIGGER trg_check_lote_project
BEFORE INSERT OR UPDATE ON lotes
FOR EACH ROW EXECUTE FUNCTION check_lote_within_project();
