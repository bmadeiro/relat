CREATE TABLE IF NOT EXISTS projetos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL
                                 UNIQUE,
    descricao TEXT,
    autor VARCHAR(100) NOT NULL,
    bd_tipo VARCHAR(50),
    bd VARCHAR(50),
    bd_servidor VARCHAR(50),
    bd_porta NUMBER,
    bd_usuario VARCHAR(50),
    bd_senha VARCHAR(100),
    bd_str_conexao VARCHAR(200),
    criado_em      DATETIME      NOT NULL,
    alterado_em    DATETIME      NOT NULL
                                 DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS relatorios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    projeto_id integer NOT NULL,
    nome TEXT,
    descricao TEXT,
    autor VARCHAR(100) NOT NULL,
    consulta TEXT,
    ordem NUMBER,
    tipo_operacao VARCHAR(10),
    criado_em DATETIME NOT NULL,
    alterado_em DATETIME NOT NULL
                         DEFAULT (datetime('now','localtime'))
);
