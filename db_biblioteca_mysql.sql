CREATE DATABASE db_biblioteca;
USE db_biblioteca;

CREATE TABLE tbl_alunos(
alu_codigo INT AUTO_INCREMENT PRIMARY KEY,
alu_nome VARCHAR(50) NOT NULL,
alu_matricula VARCHAR(50) NOT NULL UNIQUE,
alu_turma VARCHAR(50) NOT NULL,
alu_email VARCHAR(50) UNIQUE
);

CREATE TABLE tbl_livros(
liv_codigo INT AUTO_INCREMENT PRIMARY KEY,
liv_titulo VARCHAR(100) NOT NULL,
liv_autor VARCHAR(50) NOT NULL,
liv_ano INT,
liv_quantidade INT NOT NULL DEFAULT 1
);

CREATE TABLE tbl_emprestimos(
emp_codigo INT AUTO_INCREMENT PRIMARY KEY,
emp_data DATE NOT NULL,
emp_devolucao DATE,
emp_status ENUM('emprestado', 'devolvido', 'atrasado'),
alu_codigo INT,
CONSTRAINT fk_emprestimos_alunos FOREIGN KEY (alu_codigo)
REFERENCES tbl_alunos(alu_codigo),
liv_codigo INT,
CONSTRAINT fk_livros_alunos FOREIGN KEY (liv_codigo)
REFERENCES tbl_livros(liv_codigo)
);

INSERT INTO tbl_alunos
(alu_nome, alu_matricula, alu_turma, alu_email)
VALUES
('João Silva', '2026001', '2A', 'joao@email.com'),
('Maria Souza', '2026002', '2B', 'maria@email.com'),
('Pedro Lima', '2026003', '3A', 'pedro@email.com');

INSERT INTO tbl_livros
(liv_titulo, liv_autor, liv_ano, liv_quantidade)
VALUES
('Dom Casmurro', 'Machado de Assis', 1899, 3),
('1984', 'George Orwell', 1949, 2),
('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 1943, 4);

INSERT INTO tbl_emprestimos
(emp_data, emp_devolucao, emp_status, alu_codigo, liv_codigo)
VALUES
('2026-09-10', NULL, 'emprestado', 1, 1),
('2026-09-01', '2026-09-08', 'devolvido', 2, 2),
('2026-08-20', NULL, 'atrasado', 3, 3);