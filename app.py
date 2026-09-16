from pathlib import Path
import sqlite3
from flask import Flask, flash, g, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "biblioteca.db"
app = Flask(__name__)
app.config["SECRET_KEY"] = "biblioteca-crud-dev-key"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema = (BASE_DIR / "schema.sql").read_text(encoding="utf-8")
    db.executescript(schema)
    db.commit()


def row_or_404(table, key, value):
    row = get_db().execute(f"SELECT * FROM {table} WHERE {key} = ?", (value,)).fetchone()
    if row is None:
        from flask import abort
        abort(404)
    return row


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Banco inicializado.")


@app.route("/")
def index():
    db = get_db()
    counts = {
        "alunos": db.execute("SELECT COUNT(*) FROM tbl_alunos").fetchone()[0],
        "livros": db.execute("SELECT COUNT(*) FROM tbl_livros").fetchone()[0],
        "emprestimos": db.execute("SELECT COUNT(*) FROM tbl_emprestimos").fetchone()[0],
    }
    return render_template("index.html", counts=counts)


@app.route("/alunos")
def listar_alunos():
    alunos = get_db().execute("SELECT * FROM tbl_alunos ORDER BY alu_nome").fetchall()
    return render_template("alunos.html", alunos=alunos)


@app.route("/alunos/novo", methods=("GET", "POST"))
def criar_aluno():
    if request.method == "POST":
        nome = request.form.get("alu_nome", "").strip()
        matricula = request.form.get("alu_matricula", "").strip()
        turma = request.form.get("alu_turma", "").strip()
        email = request.form.get("alu_email", "").strip() or None
        if not nome or not matricula or not turma:
            flash("Nome, matrícula e turma são obrigatórios.", "error")
        else:
            try:
                db = get_db()
                db.execute("INSERT INTO tbl_alunos (alu_nome, alu_matricula, alu_turma, alu_email) VALUES (?, ?, ?, ?)", (nome, matricula, turma, email))
                db.commit()
                flash("Aluno cadastrado com sucesso.", "success")
                return redirect(url_for("listar_alunos"))
            except sqlite3.IntegrityError:
                flash("A matrícula ou o e-mail informado já está cadastrado.", "error")
    return render_template("aluno_form.html", aluno=None, titulo="Novo aluno")


@app.route("/alunos/<int:codigo>/editar", methods=("GET", "POST"))
def editar_aluno(codigo):
    aluno = row_or_404("tbl_alunos", "alu_codigo", codigo)
    if request.method == "POST":
        nome = request.form.get("alu_nome", "").strip()
        matricula = request.form.get("alu_matricula", "").strip()
        turma = request.form.get("alu_turma", "").strip()
        email = request.form.get("alu_email", "").strip() or None
        if not nome or not matricula or not turma:
            flash("Nome, matrícula e turma são obrigatórios.", "error")
        else:
            try:
                db = get_db()
                db.execute("UPDATE tbl_alunos SET alu_nome=?, alu_matricula=?, alu_turma=?, alu_email=? WHERE alu_codigo=?", (nome, matricula, turma, email, codigo))
                db.commit()
                flash("Aluno atualizado com sucesso.", "success")
                return redirect(url_for("listar_alunos"))
            except sqlite3.IntegrityError:
                flash("A matrícula ou o e-mail informado já está cadastrado.", "error")
    return render_template("aluno_form.html", aluno=aluno, titulo="Editar aluno")


@app.post("/alunos/<int:codigo>/excluir")
def excluir_aluno(codigo):
    row_or_404("tbl_alunos", "alu_codigo", codigo)
    try:
        db = get_db()
        db.execute("DELETE FROM tbl_alunos WHERE alu_codigo=?", (codigo,))
        db.commit()
        flash("Aluno excluído com sucesso.", "success")
    except sqlite3.IntegrityError:
        flash("Não é possível excluir aluno com empréstimos registrados.", "error")
    return redirect(url_for("listar_alunos"))


@app.route("/livros")
def listar_livros():
    livros = get_db().execute("SELECT * FROM tbl_livros ORDER BY liv_titulo").fetchall()
    return render_template("livros.html", livros=livros)


@app.route("/livros/novo", methods=("GET", "POST"))
def criar_livro():
    if request.method == "POST":
        titulo = request.form.get("liv_titulo", "").strip()
        autor = request.form.get("liv_autor", "").strip()
        ano = request.form.get("liv_ano", "").strip() or None
        quantidade = request.form.get("liv_quantidade", "1").strip()
        if not titulo or not autor:
            flash("Título e autor são obrigatórios.", "error")
        else:
            try:
                db = get_db()
                db.execute("INSERT INTO tbl_livros (liv_titulo, liv_autor, liv_ano, liv_quantidade) VALUES (?, ?, ?, ?)", (titulo, autor, ano, quantidade))
                db.commit()
                flash("Livro cadastrado com sucesso.", "success")
                return redirect(url_for("listar_livros"))
            except (sqlite3.IntegrityError, ValueError):
                flash("Verifique os valores informados para o livro.", "error")
    return render_template("livro_form.html", livro=None, titulo="Novo livro")


@app.route("/livros/<int:codigo>/editar", methods=("GET", "POST"))
def editar_livro(codigo):
    livro = row_or_404("tbl_livros", "liv_codigo", codigo)
    if request.method == "POST":
        titulo = request.form.get("liv_titulo", "").strip()
        autor = request.form.get("liv_autor", "").strip()
        ano = request.form.get("liv_ano", "").strip() or None
        quantidade = request.form.get("liv_quantidade", "1").strip()
        if not titulo or not autor:
            flash("Título e autor são obrigatórios.", "error")
        else:
            try:
                db = get_db()
                db.execute("UPDATE tbl_livros SET liv_titulo=?, liv_autor=?, liv_ano=?, liv_quantidade=? WHERE liv_codigo=?", (titulo, autor, ano, quantidade, codigo))
                db.commit()
                flash("Livro atualizado com sucesso.", "success")
                return redirect(url_for("listar_livros"))
            except (sqlite3.IntegrityError, ValueError):
                flash("Verifique os valores informados para o livro.", "error")
    return render_template("livro_form.html", livro=livro, titulo="Editar livro")


@app.post("/livros/<int:codigo>/excluir")
def excluir_livro(codigo):
    row_or_404("tbl_livros", "liv_codigo", codigo)
    try:
        db = get_db()
        db.execute("DELETE FROM tbl_livros WHERE liv_codigo=?", (codigo,))
        db.commit()
        flash("Livro excluído com sucesso.", "success")
    except sqlite3.IntegrityError:
        flash("Não é possível excluir livro com empréstimos registrados.", "error")
    return redirect(url_for("listar_livros"))


@app.route("/emprestimos")
def listar_emprestimos():
    emprestimos = get_db().execute("""SELECT e.*, a.alu_nome, l.liv_titulo
        FROM tbl_emprestimos e JOIN tbl_alunos a ON a.alu_codigo=e.alu_codigo
        JOIN tbl_livros l ON l.liv_codigo=e.liv_codigo ORDER BY e.emp_data DESC""").fetchall()
    return render_template("emprestimos.html", emprestimos=emprestimos)


@app.route("/emprestimos/novo", methods=("GET", "POST"))
def criar_emprestimo():
    db = get_db()
    alunos = db.execute("SELECT * FROM tbl_alunos ORDER BY alu_nome").fetchall()
    livros = db.execute("SELECT * FROM tbl_livros ORDER BY liv_titulo").fetchall()
    if request.method == "POST":
        data = request.form.get("emp_data", "").strip()
        devolucao = request.form.get("emp_devolucao", "").strip() or None
        status = request.form.get("emp_status", "emprestado")
        aluno = request.form.get("alu_codigo")
        livro = request.form.get("liv_codigo")
        if not data or not aluno or not livro or status not in ("emprestado", "devolvido", "atrasado"):
            flash("Data, aluno, livro e status são obrigatórios.", "error")
        else:
            try:
                db.execute("INSERT INTO tbl_emprestimos (emp_data, emp_devolucao, emp_status, alu_codigo, liv_codigo) VALUES (?, ?, ?, ?, ?)", (data, devolucao, status, aluno, livro))
                db.commit()
                flash("Empréstimo registrado com sucesso.", "success")
                return redirect(url_for("listar_emprestimos"))
            except sqlite3.IntegrityError:
                flash("Aluno ou livro inválido.", "error")
    return render_template("emprestimo_form.html", emprestimo=None, alunos=alunos, livros=livros, titulo="Novo empréstimo")


@app.route("/emprestimos/<int:codigo>/editar", methods=("GET", "POST"))
def editar_emprestimo(codigo):
    emprestimo = row_or_404("tbl_emprestimos", "emp_codigo", codigo)
    db = get_db()
    alunos = db.execute("SELECT * FROM tbl_alunos ORDER BY alu_nome").fetchall()
    livros = db.execute("SELECT * FROM tbl_livros ORDER BY liv_titulo").fetchall()
    if request.method == "POST":
        data = request.form.get("emp_data", "").strip()
        devolucao = request.form.get("emp_devolucao", "").strip() or None
        status = request.form.get("emp_status", "emprestado")
        aluno = request.form.get("alu_codigo")
        livro = request.form.get("liv_codigo")
        if not data or not aluno or not livro or status not in ("emprestado", "devolvido", "atrasado"):
            flash("Data, aluno, livro e status são obrigatórios.", "error")
        else:
            try:
                db.execute("UPDATE tbl_emprestimos SET emp_data=?, emp_devolucao=?, emp_status=?, alu_codigo=?, liv_codigo=? WHERE emp_codigo=?", (data, devolucao, status, aluno, livro, codigo))
                db.commit()
                flash("Empréstimo atualizado com sucesso.", "success")
                return redirect(url_for("listar_emprestimos"))
            except sqlite3.IntegrityError:
                flash("Aluno ou livro inválido.", "error")
    return render_template("emprestimo_form.html", emprestimo=emprestimo, alunos=alunos, livros=livros, titulo="Editar empréstimo")


@app.post("/emprestimos/<int:codigo>/excluir")
def excluir_emprestimo(codigo):
    row_or_404("tbl_emprestimos", "emp_codigo", codigo)
    db = get_db()
    db.execute("DELETE FROM tbl_emprestimos WHERE emp_codigo=?", (codigo,))
    db.commit()
    flash("Empréstimo excluído com sucesso.", "success")
    return redirect(url_for("listar_emprestimos"))


if __name__ == "__main__":
    if not DATABASE.exists():
        with app.app_context():
            init_db()
    app.run(debug=True)
