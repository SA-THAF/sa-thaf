-- ============================================================================
-- CTW MANUTENÇÃO — REFATORAÇÃO PARA POSTGRESQL COM SOFT DELETE (v2)
-- ============================================================================
-- Esta versão foi adaptada ao esquema com nomes de coluna específicos por
-- tabela (id_perfil, id_usuario, id_ss, id_os, etc. em vez de "id" genérico).
--
-- NOTAS DE ARQUITETURA:
--
-- 1) PADRÃO ESCOLHIDO POR TABELA
--    - Catálogos pequenos e de baixíssima exclusão (perfis, setores, turmas)
--      usam soft delete "in-place": coluna deleted_at na própria tabela +
--      índice único parcial. Um DELETE nessas tabelas é interceptado e
--      convertido em UPDATE — a linha nunca some fisicamente.
--    - As demais 10 tabelas usam HERANÇA: tabela_deletados INHERITS (tabela),
--      recebendo a coluna deleted_at. Um DELETE move a linha para o
--      histórico e conclui a remoção na tabela principal.
--
-- 2) FUNÇÕES DE TRIGGER GENÉRICAS (reaproveitadas por várias tabelas)
--    - fn_mover_para_historico(): usada pelas 10 tabelas de herança. Não
--      depende do nome da PK — copia a linha inteira com "(OLD).*".
--    - fn_soft_delete_inline(): usada por perfis/setores/turmas. Como cada
--      uma tem uma coluna de PK com nome diferente (id_perfil, id_setor,
--      id_turma), o nome da PK é passado como ARGUMENTO do trigger
--      (TG_ARGV[0]) e o valor é lido de OLD via to_jsonb(OLD)->>pk_col,
--      sem precisar de uma função por tabela.
--
-- 3) COMPORTAMENTO DE HERANÇA NO POSTGRES (importante!)
--    - "SELECT * FROM tabela" por padrão TAMBÉM retorna linhas da tabela
--      filha (tabela_deletados). Para somente ativos use "SELECT * FROM
--      ONLY tabela". As views vw_todos_* já resolvem isso para auditoria.
--    - PRIMARY KEY, UNIQUE e FOREIGN KEY do pai NÃO são herdados
--      automaticamente pelas tabelas filhas (proposital: histórico não deve
--      reforçar integridade referencial de dados já excluídos).
--    - Uma FK que referencia "tabela" só é validada contra as linhas
--      físicas da própria tabela pai (nunca contra a _deletados), então,
--      após mover um registro para o histórico, nada mais pode referenciá-lo.
--
-- 4) CASCATA (requisito 3)
--    FKs mantêm ON DELETE CASCADE/SET NULL/RESTRICT como no original. Ao
--    apagar um pai, o Postgres dispara DELETE em cascata nos filhos, o que
--    ACIONA o BEFORE DELETE de cada filho normalmente — cada filho vai para
--    seu próprio histórico automaticamente, sem código extra.
--
-- Execute conectado ao banco de destino (ex: \c ctw_manutencao).
-- ============================================================================


-- ============================================================================
-- 1. TIPOS ENUM (equivalentes aos ENUM inline do MySQL)
-- ============================================================================

CREATE TYPE status_maquina_enum      AS ENUM ('Operando','Manutenção','Parado','Crítico');
CREATE TYPE status_alerta_enum       AS ENUM ('Pendente','Resolvido');
CREATE TYPE prioridade_ss_enum       AS ENUM ('Baixa','Média','Alta');
CREATE TYPE tipo_manutencao_ss_enum  AS ENUM ('Corretiva','Preventiva','Preditiva');
CREATE TYPE status_ss_enum           AS ENUM ('Aberta','Em Análise','Aguardando Peças','Execução','Validação','Concluída');
CREATE TYPE tipo_manutencao_os_enum  AS ENUM ('Corretiva','Preventiva','Preditiva','Melhoria');
CREATE TYPE criticidade_os_enum      AS ENUM ('Baixa','Média','Alta','Crítica');
CREATE TYPE status_compra_enum       AS ENUM ('Não Visualizado','Em Análise','Pedido em Andamento','Entregue');
CREATE TYPE frequencia_cal_enum      AS ENUM ('Diária','Semanal','Quinzenal','Mensal','Semestral','Anual');
CREATE TYPE status_cal_enum          AS ENUM ('Agendada','Em Execução','Concluída','Atrasada','Cancelada');


-- ============================================================================
-- 2. FUNÇÕES DE SUPORTE
-- ============================================================================

-- Move a linha excluída para "<tabela>_deletados" e deixa o DELETE concluir
-- na tabela principal. Usada pelas 10 tabelas do padrão "herança".
CREATE OR REPLACE FUNCTION fn_mover_para_historico()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE format('INSERT INTO %I SELECT ($1).*, now()', TG_TABLE_NAME || '_deletados')
    USING OLD;
    RETURN OLD; -- permite que o DELETE original prossiga na tabela principal
END;
$$ LANGUAGE plpgsql;

-- Converte um DELETE em UPDATE (deleted_at = now()) e cancela a remoção
-- física. Genérica para qualquer PK: o nome da coluna de PK é passado como
-- argumento do trigger (TG_ARGV[0]), já que cada tabela usa um nome
-- diferente (id_perfil, id_setor, id_turma...).
CREATE OR REPLACE FUNCTION fn_soft_delete_inline()
RETURNS TRIGGER AS $$
DECLARE
    pk_col text := TG_ARGV[0];
    pk_val integer;
BEGIN
    pk_val := (to_jsonb(OLD) ->> pk_col)::integer;
    EXECUTE format('UPDATE %I SET deleted_at = now() WHERE %I = $1', TG_TABLE_NAME, pk_col)
    USING pk_val;
    RETURN NULL; -- cancela o DELETE físico
END;
$$ LANGUAGE plpgsql;

-- Equivalente ao "ON UPDATE CURRENT_TIMESTAMP" do MySQL para maquinas.ultima_manutencao
CREATE OR REPLACE FUNCTION fn_touch_ultima_manutencao()
RETURNS TRIGGER AS $$
BEGIN
    NEW.ultima_manutencao := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Equivalente ao "ON UPDATE CURRENT_TIMESTAMP" do MySQL para solicitacoes_servico.atualizado_em
CREATE OR REPLACE FUNCTION fn_touch_atualizado_em()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- 3. MÓDULO DE AUTENTICAÇÃO E RBAC
-- ============================================================================

-- ---- perfis: soft delete IN-PLACE ----
CREATE TABLE perfis (
    id_perfil        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_perfil       VARCHAR(50) NOT NULL,
    descricao_perfil TEXT,
    deleted_at        TIMESTAMP DEFAULT NULL, -- NULL = ativo
    CONSTRAINT chk_perfil_nome CHECK (LOWER(nome_perfil) IN ('coordenador','gestor','professor','aluno'))
);

-- Unicidade só entre ativos: permite reaproveitar o nome de um perfil já excluído
CREATE UNIQUE INDEX idx_perfis_nome_ativo ON perfis (nome_perfil) WHERE deleted_at IS NULL;

CREATE TRIGGER trg_soft_delete_perfis
    BEFORE DELETE ON perfis
    FOR EACH ROW EXECUTE FUNCTION fn_soft_delete_inline('id_perfil');

-- ---- turmas: soft delete IN-PLACE ----
CREATE TABLE turmas (
    id_turma      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_turma  VARCHAR(20) NOT NULL,   -- Ex: 'MAN-2026-2T'
    periodo_turma VARCHAR(20) NOT NULL,   -- Ex: 'Primeiro Turno'
    deleted_at    TIMESTAMP DEFAULT NULL
);

CREATE UNIQUE INDEX idx_turmas_codigo_ativo ON turmas (codigo_turma) WHERE deleted_at IS NULL;

CREATE TRIGGER trg_soft_delete_turmas
    BEFORE DELETE ON turmas
    FOR EACH ROW EXECUTE FUNCTION fn_soft_delete_inline('id_turma');

-- ---- usuarios: soft delete por HERANÇA ----
CREATE TABLE usuarios (
    id_usuario     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    perfil_id      INTEGER NOT NULL REFERENCES perfis(id_perfil) ON DELETE RESTRICT ON UPDATE CASCADE,
    turma_id       INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL ON UPDATE CASCADE,
    nome_usuario   VARCHAR(100) NOT NULL,
    email_usuario  VARCHAR(100) NOT NULL UNIQUE,
    senha_hash     VARCHAR(255) NOT NULL,
    criado_em      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_usuarios_perfil_id    ON usuarios (perfil_id);
CREATE INDEX idx_usuarios_turma_id     ON usuarios (turma_id);
CREATE INDEX idx_usuarios_nome_usuario ON usuarios (nome_usuario);

CREATE TABLE usuarios_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (usuarios);

CREATE INDEX idx_usuarios_deletados_deleted_at ON usuarios_deletados USING BRIN (deleted_at);
CREATE INDEX idx_usuarios_deletados_id_usuario  ON usuarios_deletados (id_usuario);

CREATE TRIGGER trg_soft_delete_usuarios
    BEFORE DELETE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_usuarios AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY usuarios
    UNION ALL
    SELECT * FROM usuarios_deletados;

-- ---- logs_auditoria: soft delete por HERANÇA ----
CREATE TABLE logs_auditoria (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario_id  INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    acao        TEXT NOT NULL,
    endereco_ip VARCHAR(45),
    criado_em   TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_logs_auditoria_usuario_id ON logs_auditoria (usuario_id);
CREATE INDEX idx_logs_auditoria_criado_em  ON logs_auditoria (criado_em);

CREATE TABLE logs_auditoria_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (logs_auditoria);

CREATE INDEX idx_logs_auditoria_deletados_deleted_at ON logs_auditoria_deletados USING BRIN (deleted_at);
CREATE INDEX idx_logs_auditoria_deletados_id ON logs_auditoria_deletados (id);

CREATE TRIGGER trg_soft_delete_logs_auditoria
    BEFORE DELETE ON logs_auditoria
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_logs_auditoria AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY logs_auditoria
    UNION ALL
    SELECT * FROM logs_auditoria_deletados;


-- ============================================================================
-- 4. MÓDULO MAPA DA OFICINA E MAQUINÁRIO
-- ============================================================================

-- ---- setores: soft delete IN-PLACE ----
CREATE TABLE setores (
    id_setor        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_setor       VARCHAR(50) NOT NULL,
    descricao_setor TEXT,
    deleted_at       TIMESTAMP DEFAULT NULL
);

CREATE UNIQUE INDEX idx_setores_nome_ativo ON setores (nome_setor) WHERE deleted_at IS NULL;

CREATE TRIGGER trg_soft_delete_setores
    BEFORE DELETE ON setores
    FOR EACH ROW EXECUTE FUNCTION fn_soft_delete_inline('id_setor');

-- ---- maquinas: soft delete por HERANÇA ----
CREATE TABLE maquinas (
    id_maquina         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    setor_id           INTEGER NOT NULL REFERENCES setores(id_setor) ON DELETE RESTRICT ON UPDATE CASCADE,
    tag_maquina        VARCHAR(20) NOT NULL UNIQUE,
    nome_maquina       VARCHAR(100) NOT NULL,
    status_vivo        status_maquina_enum DEFAULT 'Operando',
    ultima_manutencao  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_maquinas_setor_id    ON maquinas (setor_id);
CREATE INDEX idx_maquinas_status_vivo ON maquinas (status_vivo);

CREATE TABLE maquinas_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (maquinas);

CREATE INDEX idx_maquinas_deletados_deleted_at ON maquinas_deletados USING BRIN (deleted_at);
CREATE INDEX idx_maquinas_deletados_id_maquina  ON maquinas_deletados (id_maquina);

CREATE TRIGGER trg_soft_delete_maquinas
    BEFORE DELETE ON maquinas
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

-- "ON UPDATE CURRENT_TIMESTAMP" do MySQL original
CREATE TRIGGER trg_touch_maquinas
    BEFORE UPDATE ON maquinas
    FOR EACH ROW EXECUTE FUNCTION fn_touch_ultima_manutencao();

CREATE VIEW vw_todos_maquinas AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY maquinas
    UNION ALL
    SELECT * FROM maquinas_deletados;


-- ============================================================================
-- 5. MÓDULO ALMOXARIFADO E FERRAMENTARIA
-- ============================================================================

-- ---- itens_almoxarifado: soft delete por HERANÇA ----
CREATE TABLE itens_almoxarifado (
    id_ferramenta        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_ferramenta      VARCHAR(100) NOT NULL,
    dimensao_ferramenta  VARCHAR(50) DEFAULT NULL,
    quantidade_atual     INTEGER NOT NULL DEFAULT 0,
    estoque_minimo       INTEGER NOT NULL DEFAULT 1,
    unidade_medida       VARCHAR(10) DEFAULT 'UN',
    localizacao_gaveta   VARCHAR(50)
);

CREATE INDEX idx_itens_almoxarifado_nome ON itens_almoxarifado (nome_ferramenta);

CREATE TABLE itens_almoxarifado_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (itens_almoxarifado);

CREATE INDEX idx_itens_almoxarifado_deletados_deleted_at ON itens_almoxarifado_deletados USING BRIN (deleted_at);
CREATE INDEX idx_itens_almoxarifado_deletados_id ON itens_almoxarifado_deletados (id_ferramenta);

CREATE TRIGGER trg_soft_delete_itens_almoxarifado
    BEFORE DELETE ON itens_almoxarifado
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_itens_almoxarifado AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY itens_almoxarifado
    UNION ALL
    SELECT * FROM itens_almoxarifado_deletados;

-- ---- alertas_estoque: soft delete por HERANÇA ----
CREATE TABLE alertas_estoque (
    id_alerta       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id         INTEGER NOT NULL REFERENCES itens_almoxarifado(id_ferramenta) ON DELETE CASCADE,
    mensagem_alerta VARCHAR(255) NOT NULL,
    status          status_alerta_enum DEFAULT 'Pendente',
    criado_em       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alertas_estoque_item_id ON alertas_estoque (item_id);
CREATE INDEX idx_alertas_estoque_status  ON alertas_estoque (status);

CREATE TABLE alertas_estoque_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (alertas_estoque);

CREATE INDEX idx_alertas_estoque_deletados_deleted_at ON alertas_estoque_deletados USING BRIN (deleted_at);
CREATE INDEX idx_alertas_estoque_deletados_id ON alertas_estoque_deletados (id_alerta);

CREATE TRIGGER trg_soft_delete_alertas_estoque
    BEFORE DELETE ON alertas_estoque
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_alertas_estoque AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY alertas_estoque
    UNION ALL
    SELECT * FROM alertas_estoque_deletados;

-- ---- registros_quebra: soft delete por HERANÇA ----
CREATE TABLE registros_quebra (
    id_quebra        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id          INTEGER NOT NULL REFERENCES itens_almoxarifado(id_ferramenta) ON DELETE CASCADE,
    usuario_id       INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    descricao_quebra TEXT NOT NULL,
    foto_url         VARCHAR(255),
    criado_em        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_registros_quebra_item_id    ON registros_quebra (item_id);
CREATE INDEX idx_registros_quebra_usuario_id ON registros_quebra (usuario_id);

CREATE TABLE registros_quebra_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (registros_quebra);

CREATE INDEX idx_registros_quebra_deletados_deleted_at ON registros_quebra_deletados USING BRIN (deleted_at);
CREATE INDEX idx_registros_quebra_deletados_id ON registros_quebra_deletados (id_quebra);

CREATE TRIGGER trg_soft_delete_registros_quebra
    BEFORE DELETE ON registros_quebra
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_registros_quebra AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY registros_quebra
    UNION ALL
    SELECT * FROM registros_quebra_deletados;


-- ============================================================================
-- 6. MÓDULO ORDENS DE SERVIÇO (O.S.) E EXECUÇÃO DE MANUTENÇÃO
-- ============================================================================

-- ---- solicitacoes_servico: soft delete por HERANÇA ----
CREATE TABLE solicitacoes_servico (
    id_ss                      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maquina_id                 INTEGER NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    solicitante_id             INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    responsavel_id             INTEGER DEFAULT NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    professor_validador_id     INTEGER DEFAULT NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    descricao_problema         TEXT NOT NULL,
    prioridade_ss              prioridade_ss_enum DEFAULT 'Média',
    tipo_manutencao            tipo_manutencao_ss_enum DEFAULT 'Corretiva',
    status                     status_ss_enum DEFAULT 'Aberta',
    criado_em                  TIMESTAMP DEFAULT NOW(),
    atualizado_em               TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_solicitacoes_servico_maquina_id     ON solicitacoes_servico (maquina_id);
CREATE INDEX idx_solicitacoes_servico_solicitante_id ON solicitacoes_servico (solicitante_id);
CREATE INDEX idx_solicitacoes_servico_responsavel_id ON solicitacoes_servico (responsavel_id);
CREATE INDEX idx_solicitacoes_servico_prof_valid_id  ON solicitacoes_servico (professor_validador_id);
CREATE INDEX idx_solicitacoes_servico_status         ON solicitacoes_servico (status);

CREATE TABLE solicitacoes_servico_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (solicitacoes_servico);

CREATE INDEX idx_solicitacoes_servico_deletados_deleted_at ON solicitacoes_servico_deletados USING BRIN (deleted_at);
CREATE INDEX idx_solicitacoes_servico_deletados_id ON solicitacoes_servico_deletados (id_ss);

CREATE TRIGGER trg_soft_delete_solicitacoes_servico
    BEFORE DELETE ON solicitacoes_servico
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

-- "ON UPDATE CURRENT_TIMESTAMP" do MySQL original
CREATE TRIGGER trg_touch_solicitacoes_servico
    BEFORE UPDATE ON solicitacoes_servico
    FOR EACH ROW EXECUTE FUNCTION fn_touch_atualizado_em();

CREATE VIEW vw_todos_solicitacoes_servico AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY solicitacoes_servico
    UNION ALL
    SELECT * FROM solicitacoes_servico_deletados;

-- ---- ordens_servico: soft delete por HERANÇA ----
CREATE TABLE ordens_servico (
    id_os                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    solicitacao_id       INTEGER NOT NULL REFERENCES solicitacoes_servico(id_ss) ON DELETE CASCADE,
    maquina_id           INTEGER NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    turma_id             INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL,
    tipo_manutencao      tipo_manutencao_os_enum NOT NULL,
    criticidade_os       criticidade_os_enum NOT NULL,
    descricao_execucao   TEXT NOT NULL,
    pecas_usadas         TEXT,
    data_execucao        DATE NOT NULL,
    hora_inicio          TIME NOT NULL,
    hora_fim              TIME NOT NULL,
    quantidade_pessoas   INTEGER NOT NULL DEFAULT 1,
    criado_em            TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ordens_servico_solicitacao_id ON ordens_servico (solicitacao_id);
CREATE INDEX idx_ordens_servico_maquina_id     ON ordens_servico (maquina_id);
CREATE INDEX idx_ordens_servico_turma_id       ON ordens_servico (turma_id);
CREATE INDEX idx_ordens_servico_data_execucao  ON ordens_servico (data_execucao);

CREATE TABLE ordens_servico_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (ordens_servico);

CREATE INDEX idx_ordens_servico_deletados_deleted_at ON ordens_servico_deletados USING BRIN (deleted_at);
CREATE INDEX idx_ordens_servico_deletados_id ON ordens_servico_deletados (id_os);

CREATE TRIGGER trg_soft_delete_ordens_servico
    BEFORE DELETE ON ordens_servico
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_ordens_servico AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY ordens_servico
    UNION ALL
    SELECT * FROM ordens_servico_deletados;


-- ============================================================================
-- 7. MÓDULO SOLICITAÇÃO DE COMPRAS
-- ============================================================================

-- ---- solicitacoes_compras: soft delete por HERANÇA ----
CREATE TABLE solicitacoes_compras (
    id_solicitacao             INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    solicitante_id             INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    professor_responsavel_id   INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    turma_id                   INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL,
    maquina_id                 INTEGER DEFAULT NULL REFERENCES maquinas(id_maquina) ON DELETE SET NULL,
    status                     status_compra_enum DEFAULT 'Não Visualizado',
    especificacao_tecnica      TEXT NOT NULL,
    quantidade_solicitacao     INTEGER NOT NULL DEFAULT 1,
    sap_solicitacao            VARCHAR(50) DEFAULT NULL,
    justificativa_solicitacao  TEXT NOT NULL,
    patrimonio                 VARCHAR(50) DEFAULT NULL,
    equipamento                VARCHAR(100) DEFAULT NULL,
    conjunto_mecanico          VARCHAR(100) DEFAULT NULL,
    arquivos                   VARCHAR(255) DEFAULT NULL,
    criado_em                  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_solicitacoes_compras_solicitante_id  ON solicitacoes_compras (solicitante_id);
CREATE INDEX idx_solicitacoes_compras_prof_resp_id    ON solicitacoes_compras (professor_responsavel_id);
CREATE INDEX idx_solicitacoes_compras_turma_id        ON solicitacoes_compras (turma_id);
CREATE INDEX idx_solicitacoes_compras_maquina_id      ON solicitacoes_compras (maquina_id);
CREATE INDEX idx_solicitacoes_compras_status          ON solicitacoes_compras (status);

CREATE TABLE solicitacoes_compras_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (solicitacoes_compras);

CREATE INDEX idx_solicitacoes_compras_deletados_deleted_at ON solicitacoes_compras_deletados USING BRIN (deleted_at);
CREATE INDEX idx_solicitacoes_compras_deletados_id ON solicitacoes_compras_deletados (id_solicitacao);

CREATE TRIGGER trg_soft_delete_solicitacoes_compras
    BEFORE DELETE ON solicitacoes_compras
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_solicitacoes_compras AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY solicitacoes_compras
    UNION ALL
    SELECT * FROM solicitacoes_compras_deletados;


-- ============================================================================
-- 8. MÓDULO CALENDÁRIO PREVENTIVO
-- ============================================================================

-- ---- calendario_preventivo: soft delete por HERANÇA ----
CREATE TABLE calendario_preventivo (
    id_calendario           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maquina_id              INTEGER NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    turma_id                INTEGER DEFAULT NULL REFERENCES turmas(id_turma) ON DELETE SET NULL,
    responsavel_id          INTEGER DEFAULT NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    titulo_calendario       VARCHAR(100) NOT NULL,
    descricao_calendario    TEXT,
    frequencia_calendario   frequencia_cal_enum NOT NULL,
    data_proxima_execucao   DATE NOT NULL,
    status                  status_cal_enum DEFAULT 'Agendada',
    criado_em               TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_calendario_preventivo_maquina_id     ON calendario_preventivo (maquina_id);
CREATE INDEX idx_calendario_preventivo_turma_id       ON calendario_preventivo (turma_id);
CREATE INDEX idx_calendario_preventivo_responsavel_id ON calendario_preventivo (responsavel_id);
CREATE INDEX idx_calendario_preventivo_status         ON calendario_preventivo (status);
CREATE INDEX idx_calendario_preventivo_data_prox_exec ON calendario_preventivo (data_proxima_execucao);

CREATE TABLE calendario_preventivo_deletados (
    deleted_at TIMESTAMP NOT NULL DEFAULT NOW()
) INHERITS (calendario_preventivo);

CREATE INDEX idx_calendario_preventivo_deletados_deleted_at ON calendario_preventivo_deletados USING BRIN (deleted_at);
CREATE INDEX idx_calendario_preventivo_deletados_id ON calendario_preventivo_deletados (id_calendario);

CREATE TRIGGER trg_soft_delete_calendario_preventivo
    BEFORE DELETE ON calendario_preventivo
    FOR EACH ROW EXECUTE FUNCTION fn_mover_para_historico();

CREATE VIEW vw_todos_calendario_preventivo AS
    SELECT *, NULL::timestamp AS deleted_at FROM ONLY calendario_preventivo
    UNION ALL
    SELECT * FROM calendario_preventivo_deletados;

-- ============================================================================
-- FIM DO SCRIPT
-- ============================================================================


