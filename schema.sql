PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS tbl_emprestimos;
DROP TABLE IF EXISTS tbl_alunos;
DROP TABLE IF EXISTS tbl_livros;

CREATE TABLE tbl_alunos (
    alu_codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    alu_nome TEXT NOT NULL,
    alu_matricula TEXT NOT NULL UNIQUE,
    alu_turma TEXT NOT NULL,
    alu_email TEXT UNIQUE
);

CREATE TABLE tbl_livros (
    liv_codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    liv_titulo TEXT NOT NULL,
    liv_autor TEXT NOT NULL,
    liv_ano INTEGER,
    liv_quantidade INTEGER NOT NULL DEFAULT 1 CHECK (liv_quantidade >= 0)
);

CREATE TABLE tbl_emprestimos (
    emp_codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_data TEXT NOT NULL,
    emp_devolucao TEXT,
    emp_status TEXT NOT NULL DEFAULT 'emprestado' CHECK (emp_status IN ('emprestado', 'devolvido', 'atrasado')),
    alu_codigo INTEGER NOT NULL,
    liv_codigo INTEGER NOT NULL,
    FOREIGN KEY (alu_codigo) REFERENCES tbl_alunos(alu_codigo),
    FOREIGN KEY (liv_codigo) REFERENCES tbl_livros(liv_codigo)
);

INSERT INTO tbl_alunos (alu_nome, alu_matricula, alu_turma, alu_email) VALUES
('João Silva', '2026001', '2A', 'joao@email.com'),
('Maria Souza', '2026002', '2B', 'maria@email.com'),
('Pedro Lima', '2026003', '3A', 'pedro@email.com');
INSERT INTO tbl_livros (liv_titulo, liv_autor, liv_ano, liv_quantidade) VALUES
('Dom Casmurro', 'Machado de Assis', 1899, 3),
('1984', 'George Orwell', 1949, 2),
('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 1943, 4);
INSERT INTO tbl_emprestimos (emp_data, emp_devolucao, emp_status, alu_codigo, liv_codigo) VALUES
('2026-09-10', NULL, 'emprestado', 1, 1),
('2026-09-01', '2026-09-08', 'devolvido', 2, 2),
('2026-08-20', NULL, 'atrasado', 3, 3);
