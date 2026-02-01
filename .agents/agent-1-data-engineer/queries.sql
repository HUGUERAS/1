-- 🧪 AGENTE 1: Queries de Validação Geométrica
-- Rodar após implementar o schema SQL

-- ============================================================
-- 1. VALIDAÇÃO DE INTEGRIDADE GEOMÉTRICA
-- ============================================================

-- Verificar se todas as geometrias são válidas
SELECT 
    'lots' as tabela,
    COUNT(*) as total,
    SUM(CASE WHEN ST_IsValid(geom) THEN 1 ELSE 0 END) as validas,
    SUM(CASE WHEN NOT ST_IsValid(geom) THEN 1 ELSE 0 END) as invalidas
FROM lots
WHERE geom IS NOT NULL;

-- Listar geometrias inválidas (se houver)
SELECT id, nome_cliente, ST_AsText(geom) 
FROM lots 
WHERE geom IS NOT NULL AND NOT ST_IsValid(geom);

-- ============================================================
-- 2. DETECÇÃO DE OVERLAPS (não deve haver!)
-- ============================================================

-- Overlaps no MESMO projeto (CRÍTICO)
SELECT 
    l1.id as lote1_id,
    l1.nome_cliente as lote1_cliente,
    l2.id as lote2_id,
    l2.nome_cliente as lote2_cliente,
    ST_Area(ST_Intersection(l1.geom, l2.geom))::numeric(10,6) as area_overlap_m2,
    (ST_Area(ST_Intersection(l1.geom, l2.geom)) / ST_Area(l1.geom) * 100)::numeric(5,2) as pct_overlap_lote1
FROM lots l1
JOIN lots l2 ON l1.project_id = l2.project_id
WHERE l1.id < l2.id 
    AND l1.geom IS NOT NULL 
    AND l2.geom IS NOT NULL
    AND ST_Intersects(l1.geom, l2.geom)
    AND ST_Area(ST_Intersection(l1.geom, l2.geom)) > 0.0000001
ORDER BY area_overlap_m2 DESC;

-- ============================================================
-- 3. VALIDAÇÃO ST_WITHIN (lotes dentro de projetos)
-- ============================================================

-- Lotes que NÃO estão dentro de seus projetos (erro!)
SELECT 
    l.id as lote_id,
    l.nome_cliente,
    l.project_id,
    p.nome as nome_projeto,
    ST_Within(l.geom, p.geom) as esta_dentro
FROM lots l
JOIN projects p ON l.project_id = p.id
WHERE l.geom IS NOT NULL 
    AND p.geom IS NOT NULL
    AND NOT ST_Within(l.geom, p.geom);

-- ============================================================
-- 4. DETECÇÃO DE VIZINHANÇA (Confrontação)
-- ============================================================

-- Lotes que compartilham borda (ST_Touches)
SELECT 
    l1.id as lote1_id,
    l1.nome_cliente as lote1_cliente,
    l2.id as lote2_id,
    l2.nome_cliente as lote2_cliente,
    ST_Length(ST_Intersection(l1.geom, l2.geom))::numeric(10,2) as comprimento_confrontacao_m,
    p.nome as projeto
FROM lots l1
JOIN lots l2 ON l1.project_id = l2.project_id
JOIN projects p ON l1.project_id = p.id
WHERE l1.id < l2.id 
    AND l1.geom IS NOT NULL 
    AND l2.geom IS NOT NULL
    AND ST_Touches(l1.geom, l2.geom)
ORDER BY comprimento_confrontacao_m DESC;

-- ============================================================
-- 5. ESTATÍSTICAS DE ÁREA
-- ============================================================

-- Área total por projeto vs soma dos lotes
SELECT 
    p.id,
    p.nome,
    ST_Area(p.geom)::numeric(15,2) as area_projeto_m2,
    (ST_Area(p.geom) / 10000)::numeric(10,4) as area_projeto_ha,
    SUM(l.area_ha)::numeric(10,4) as soma_lotes_ha,
    ((ST_Area(p.geom) / 10000) - COALESCE(SUM(l.area_ha), 0))::numeric(10,4) as area_disponivel_ha,
    COUNT(l.id) as total_lotes,
    p.status
FROM projects p
LEFT JOIN lots l ON p.id = l.project_id AND l.geom IS NOT NULL
GROUP BY p.id, p.nome, p.geom, p.status
ORDER BY p.id;

-- ============================================================
-- 6. VERIFICAÇÃO DE SRID (deve ser 4674)
-- ============================================================

SELECT 
    'lots' as tabela,
    COUNT(*) as total_registros,
    COUNT(DISTINCT ST_SRID(geom)) as srids_diferentes,
    ST_SRID(geom) as srid_encontrado
FROM lots
WHERE geom IS NOT NULL
GROUP BY ST_SRID(geom);

-- ============================================================
-- 7. PERFORMANCE: Índices Spatial
-- ============================================================

-- Verificar se índices GIST foram criados
SELECT 
    indexname,
    tablename,
    indexdef
FROM pg_indexes
WHERE tablename IN ('lots', 'projects', 'wms_layers')
    AND indexname LIKE '%geom%' OR indexname LIKE '%GIST%'
ORDER BY tablename;

-- ============================================================
-- 8. DATA QUALITY REPORT
-- ============================================================

SELECT 
    'Total Projetos' as metrica,
    COUNT(*)::text as valor
FROM projects
UNION ALL
SELECT 'Total Lotes' as metrica,
    COUNT(*)::text as valor
FROM lots
UNION ALL
SELECT 'Lotes com Geom válida' as metrica,
    COUNT(*)::text as valor
FROM lots WHERE geom IS NOT NULL AND ST_IsValid(geom)
UNION ALL
SELECT 'Pagamentos Pendentes' as metrica,
    COUNT(*)::text as valor
FROM payments WHERE status = 'PENDENTE'
UNION ALL
SELECT 'Múltiplos Clientes por Projeto' as metrica,
    COUNT(DISTINCT project_id)::text as valor
FROM (
    SELECT project_id, COUNT(DISTINCT nome_cliente) as clients
    FROM lots
    WHERE project_id IS NOT NULL
    GROUP BY project_id
    HAVING COUNT(DISTINCT nome_cliente) > 1
) subq;
