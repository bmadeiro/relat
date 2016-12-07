CREATE TABLE IF NOT EXISTS projetos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    desc TEXT,
    autor VARCHAR(100) NOT NULL,
    banco VARCHAR(50),
    conexao VARCHAR(200),
    usuario_db VARCHAR(50),
    pass_db VARCHAR(100),
    criado_em DATE NOT NULL,
    alterado_em DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS relatorios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    projeto_id integer NOT NULL,
    desc TEXT,
    sql TEXT,
    proximo_id NUMBER,
    operacao VARCHAR(10),
    autor VARCHAR(100) NOT NULL,
    criado_em DATE NOT NULL,
    alterado_em DATE NOT NULL
);
