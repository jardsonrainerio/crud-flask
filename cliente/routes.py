# cliente/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db
import sqlite3

cliente_bp = Blueprint('cliente', __name__, template_folder='templates/cliente')


@cliente_bp.route('/')
def listar():
    db = get_db()

    # Obtém o número da página a partir dos parâmetros da URL, padrão 1
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    per_page = 5  # Itens por página
    offset = (page - 1) * per_page

    # Consulta para obter o total de clientes
    cursor_total = db.execute('SELECT COUNT(*) as total FROM cliente')
    total_items = cursor_total.fetchone()['total']
    total_pages = (total_items + per_page - 1) // per_page  # Calcula o total de páginas

    # Consulta para obter os clientes da página atual
    cursor = db.execute('SELECT * FROM cliente ORDER BY id LIMIT ? OFFSET ?', (per_page, offset))
    clientes = cursor.fetchall()

    return render_template('cliente_listar.html', clientes=clientes, page=page, total_pages=total_pages)


@cliente_bp.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        db = get_db()
        try:
            db.execute('INSERT INTO cliente (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
            db.commit()
            flash('Cliente criado com sucesso!')
            return redirect(url_for('cliente.listar'))
        except sqlite3.IntegrityError:
            flash('Erro: Email já existe.')
    return render_template('cliente_criar.html')


@cliente_bp.route('/<int:id>')
def detalhes(id):
    db = get_db()
    cursor = db.execute('SELECT * FROM cliente WHERE id = ?', (id,))
    cliente = cursor.fetchone()
    if cliente is None:
        flash('Cliente não encontrado.')
        return redirect(url_for('cliente.listar'))
    return render_template('cliente_detalhes.html', cliente=cliente)


@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    db = get_db()
    cursor = db.execute('SELECT * FROM cliente WHERE id = ?', (id,))
    cliente = cursor.fetchone()
    if cliente is None:
        flash('Cliente não encontrado.')
        return redirect(url_for('cliente.listar'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        try:
            db.execute('UPDATE cliente SET nome = ?, email = ?, telefone = ? WHERE id = ?', (nome, email, telefone, id))
            db.commit()
            flash('Cliente atualizado com sucesso!')
            return redirect(url_for('cliente.detalhes', id=id))
        except sqlite3.IntegrityError:
            flash('Erro: Email já existe.')

    return render_template('cliente_editar.html', cliente=cliente)


@cliente_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM cliente WHERE id = ?', (id,))
    db.commit()
    flash('Cliente deletado com sucesso!')
    return redirect(url_for('cliente.listar'))
