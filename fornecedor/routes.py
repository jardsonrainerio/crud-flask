# fornecedor/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db

fornecedor_bp = Blueprint('fornecedor', __name__, template_folder='templates/fornecedor')


@fornecedor_bp.route('/')
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

    # Consulta para obter o total de fornecedores
    cursor_total = db.execute('SELECT COUNT(*) as total FROM fornecedor')
    total_items = cursor_total.fetchone()['total']
    total_pages = (total_items + per_page - 1) // per_page  # Calcula o total de páginas

    # Consulta para obter os fornecedores da página atual
    cursor = db.execute('SELECT * FROM fornecedor ORDER BY id LIMIT ? OFFSET ?', (per_page, offset))
    fornecedores = cursor.fetchall()

    return render_template('fornecedor_listar.html', fornecedores=fornecedores, page=page, total_pages=total_pages)


@fornecedor_bp.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        produto = request.form['produto']
        contato = request.form['contato']
        db = get_db()
        db.execute('INSERT INTO fornecedor (nome, produto, contato) VALUES (?, ?, ?)', (nome, produto, contato))
        db.commit()
        flash('Fornecedor criado com sucesso!')
        return redirect(url_for('fornecedor.listar'))
    return render_template('fornecedor_criar.html')


@fornecedor_bp.route('/<int:id>')
def detalhes(id):
    db = get_db()
    cursor = db.execute('SELECT * FROM fornecedor WHERE id = ?', (id,))
    fornecedor = cursor.fetchone()
    if fornecedor is None:
        flash('Fornecedor não encontrado.')
        return redirect(url_for('fornecedor.listar'))
    return render_template('fornecedor_detalhes.html', fornecedor=fornecedor)


@fornecedor_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    db = get_db()
    cursor = db.execute('SELECT * FROM fornecedor WHERE id = ?', (id,))
    fornecedor = cursor.fetchone()
    if fornecedor is None:
        flash('Fornecedor não encontrado.')
        return redirect(url_for('fornecedor.listar'))

    if request.method == 'POST':
        nome = request.form['nome']
        produto = request.form['produto']
        contato = request.form['contato']
        db.execute('UPDATE fornecedor SET nome = ?, produto = ?, contato = ? WHERE id = ?',
                   (nome, produto, contato, id))
        db.commit()
        flash('Fornecedor atualizado com sucesso!')
        return redirect(url_for('fornecedor.detalhes', id=id))

    return render_template('fornecedor_editar.html', fornecedor=fornecedor)


@fornecedor_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM fornecedor WHERE id = ?', (id,))
    db.commit()
    flash('Fornecedor deletado com sucesso!')
    return redirect(url_for('fornecedor.listar'))
