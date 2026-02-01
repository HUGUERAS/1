# 👷 Agente 1: Engenheiro de Dados (PostgreSQL + PostGIS)

**Missão**: Estruturar o banco de dados fundiário para Azure Database for PostgreSQL com integridade geométrica rigorosa.

**Status**: Pronto para começar
**Data**: 31/01/2026
**Versão**: 1.0

---

## 🎯 Responsabilidades

1. **Criar/validar esquema SQL** com PostGIS
   - Tabelas: `users`, `projects`, `lots`, `wms_layers`, `payments`, `chat_messages`
   - Enums: `tipo_projeto`, `status_projeto`, `status_lote`, `user_role`
   - Constraints: `ST_IsValid`, `ST_Within`, `ST_Intersects`
@@   - **Extra tables allowed**: Can add additional tables if needed (up to 200) as long as they are real, not mock, and don't interfere with core functionality

2. **Garantir integridade geométrica**
   - SRID obrigatório: `4674` (SIRGAS 2000 - Brasil)
   - Tipos: `GEOMETRY(Polygon, 4674)` para lotes/projetos
   - Validação: Sem auto-interseção, polígonos fechados

3. **Criar índices para performance**
   - `CREATE INDEX idx_lotes_geom ON lotes USING GIST (geom)` (spatial index)
   - `CREATE INDEX idx_lotes_token ON lotes (token_acesso)` (magic links)
   - `CREATE INDEX idx_payments_lote ON payments (lote_id)`

4. **Gerar fixtures de teste**
   - Dados realistas de imóveis brasileiros
   - Multiplos clientes por projeto (case normal)
   - Vizinhança detectável com ST_Touches

---

## 📋 Checklist de Implementação

### Fase 1: Schema Básico (PRIORIDADE 1)
- [ ] `CREATE EXTENSION IF NOT EXISTS postgis`
- [ ] Criar ENUMs (`tipo_projeto`, `status_projeto`, `status_lote`)
- [ ] Tabela `users` (id, email, password_hash, role)
- [ ] Tabela `projects` (id, nome, tipo, status, geom)
- [ ] Tabela `lots` (id, project_id, geom, area_ha, status, token_acesso)
- [ ] Constraints de integridade geométrica (ST_IsValid CHECK)

### Fase 2: Relacionamentos & Índices (PRIORIDADE 2)
- [ ] Foreign keys (lots → projects, payments → lots)
- [ ] Índices GIST para geometrias
- [ ] Índices para tokens JWT (magic links)
- [ ] Trigger para `updated_at` timestamp

### Fase 3: Dados de Teste (PRIORIDADE 3)
- [ ] 3 projetos (INDIVIDUAL, DESMEMBRAMENTO, LOTEAMENTO)
- [ ] 10+ lotes com geometrias realistas
- [ ] 5+ usuários (topógrafos + clientes)
- [ ] Vizinhança detectável entre lotes

### Fase 4: Validação (PRIORIDADE 4)
- [ ] Testar ST_IsValid em todas geometrias
- [ ] Testar ST_Intersects (deve falhar overlaps)
- [ ] Testar ST_Within (lotes dentro de projetos)
- [ ] Performance: índices GIST funcionando

---

## 🔧 Constraints de Integridade (CRÍTICO!)

```sql
-- 1. Geometria sempre válida
ALTER TABLE lots ADD CONSTRAINT check_geom_valid 
  CHECK (geom IS NULL OR ST_IsValid(geom));

-- 2. Lote dentro do projeto
ALTER TABLE lots ADD CONSTRAINT check_within_project
  CHECK (ST_Within(geom, (SELECT geom FROM projects WHERE id = project_id)));

-- 3. Lotes não se sobrepõem (no MESMO projeto)
ALTER TABLE lots ADD CONSTRAINT no_overlap_same_project
  EXCLUDE USING GIST (project_id WITH =, geom WITH &&)
  WHERE (status != 'RASCUNHO');
```

---

## 📂 Arquivos a Criar/Modificar

| Arquivo | Status | Ação |
|---------|--------|------|
| `novo-projeto/database/init/01_schema.sql` | Existente | Revisar/Expandir |
| `novo-projeto/database/init/04_users_auth.sql` | Existente | Revisar roles |
| `novo-projeto/database/fixtures/seed.sql` | NOVO | Criar dados teste |
| `.agents/agent-1-data-engineer/queries.sql` | NOVO | Queries de validação |

---

## 🧪 Queries de Validação

**Após implementar, testar:**

```sql
-- Verificar integridade geométrica
SELECT id, ST_IsValid(geom) as valido FROM lots WHERE ST_IsValid(geom) = false;

-- Detectar overlaps (deve retornar 0)
SELECT COUNT(*) FROM lots l1 
  JOIN lots l2 ON l1.project_id = l2.project_id 
  WHERE l1.id < l2.id 
  AND ST_Intersects(l1.geom, l2.geom) 
  AND ST_Area(ST_Intersection(l1.geom, l2.geom)) > 0.0000001;

-- Detectar vizinhança (confrontação)
SELECT l1.id, l2.id, ST_Length(ST_Intersection(l1.geom, l2.geom)) as comprimento_confrontacao
  FROM lots l1 JOIN lots l2 ON l1.project_id = l2.project_id
  WHERE l1.id < l2.id AND ST_Touches(l1.geom, l2.geom);
```

---

## 🚀 Próximas Etapas (Após Este Agente)

1. **Agente 2**: Backend Python (Azure Functions) - validação de geometria
2. **Agente 3**: Frontend React - interface cliente + topógrafo
3. **Agente 4**: Integração InfinitePay + Pagamentos

---

## 📚 Referências

- PostGIS Docs: https://postgis.net/docs/
- SRID 4674 (SIRGAS 2000): https://epsg.io/4674
- Azure Database for PostgreSQL: https://docs.microsoft.com/en-us/azure/postgresql/

---

**Pronto para começar? Execute:** `python .agents/agent-1-data-engineer/run.py`
