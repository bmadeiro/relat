CREATE TABLE IF NOT EXISTS projetos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    autor VARCHAR(100) NOT NULL,
    bd_tipo VARCHAR(50),
    bd VARCHAR(50),
    bd_servidor VARCHAR(50),
    bd_porta NUMBER,
    bd_conexao VARCHAR(200),
    bd_usuario VARCHAR(50),
    bd_senha VARCHAR(100),
    criado_em DATE NOT NULL,
    alterado_em DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS relatorios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    projeto_id integer NOT NULL,
    nome TEXT,
    descricao TEXT,
    autor VARCHAR(100) NOT NULL,
    query TEXT,
    ordem NUMBER,
    bd_operacao VARCHAR(10),
    criado_em DATE NOT NULL,
    alterado_em DATE NOT NULL
);
