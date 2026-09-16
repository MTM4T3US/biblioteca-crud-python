# Sistema de Biblioteca Escolar

Aplicação web CRUD desenvolvida em Python e Flask para gerenciar **alunos**, **livros** e **empréstimos**. O projeto foi construído a partir do banco `db_biblioteca.sql` fornecido na atividade prática.

## Funcionalidades

A aplicação realiza cadastro, listagem, edição e exclusão de alunos e livros. Também permite registrar, listar, editar e excluir empréstimos, com seleção de aluno e livro por chave estrangeira. Há validação de campos obrigatórios, mensagens de erro para duplicidade de matrícula/e-mail e proteção contra exclusão de registros que possuem empréstimos relacionados.

## Banco de dados

O arquivo `db_biblioteca_mysql.sql` preserva o script MySQL recebido. Para facilitar a execução local sem a necessidade de instalar um servidor MySQL, `schema.sql` é a versão equivalente em SQLite, com as mesmas entidades, campos, relacionamentos, restrições e três registros iniciais por tabela.

| Entidade | Chave primária | Relacionamentos |
|---|---|---|
| `tbl_alunos` | `alu_codigo` | Um aluno pode possuir vários empréstimos |
| `tbl_livros` | `liv_codigo` | Um livro pode aparecer em vários empréstimos |
| `tbl_emprestimos` | `emp_codigo` | Referencia um aluno e um livro |

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\\Scripts\\activate    # Windows
pip install -r requirements.txt
flask --app app init-db
flask --app app run --debug
```

Acesse `http://127.0.0.1:5000`. Para recriar o banco com os dados iniciais, execute novamente `flask --app app init-db`.

## Estrutura das páginas

Os arquivos HTML foram nomeados de acordo com as entidades: `alunos.html`, `aluno_form.html`, `livros.html`, `livro_form.html`, `emprestimos.html` e `emprestimo_form.html`.

## Testes

```bash
pytest -q
```

## GitHub

```bash
git init
git add .
git commit -m "Implementa CRUD da biblioteca escolar"
gh repo create biblioteca-crud-python --private --source=. --remote=origin --push
```
