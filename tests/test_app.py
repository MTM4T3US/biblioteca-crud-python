import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / 'teste.db'
    monkeypatch.setattr('app.DATABASE', db_path)
    app.config.update(TESTING=True)
    with app.app_context():
        from app import init_db
        init_db()
    with app.test_client() as client:
        yield client

def test_dashboard_e_listagens(client):
    assert client.get('/').status_code == 200
    assert client.get('/alunos').status_code == 200
    assert client.get('/livros').status_code == 200
    assert client.get('/emprestimos').status_code == 200

def test_criar_editar_excluir_aluno(client):
    response = client.post('/alunos/novo', data={'alu_nome':'Ana Teste','alu_matricula':'9999','alu_turma':'1A','alu_email':'ana@test.com'}, follow_redirects=True)
    assert b'Ana Teste' in response.data
    response = client.post('/alunos/4/editar', data={'alu_nome':'Ana Editada','alu_matricula':'9999','alu_turma':'1B','alu_email':'ana@test.com'}, follow_redirects=True)
    assert b'Ana Editada' in response.data
    response = client.post('/alunos/4/excluir', follow_redirects=True)
    assert b'Ana Editada' not in response.data

def test_validacao_aluno(client):
    response = client.post('/alunos/novo', data={'alu_nome':'','alu_matricula':'','alu_turma':''}, follow_redirects=True)
    assert b'obrigat' in response.data

def test_criar_editar_emprestimo(client):
    response = client.post('/emprestimos/novo', data={'emp_data':'2026-09-16','alu_codigo':'1','liv_codigo':'1','emp_status':'emprestado'}, follow_redirects=True)
    assert b'2026-09-16' in response.data
    response = client.post('/emprestimos/4/editar', data={'emp_data':'2026-09-17','alu_codigo':'2','liv_codigo':'2','emp_status':'devolvido'}, follow_redirects=True)
    assert b'2026-09-17' in response.data
