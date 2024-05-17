from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .sorvetes_model import SorveteNaoEncontrado, listar_sorvetes, sorvete_por_id, adicionar_sorvete, atualizar_sorvete, excluir_sorvete
from config import db

sorvetes_blueprint = Blueprint('sorvetes', __name__)

@sorvetes_blueprint.route('/', methods=['GET'])
def getIndex():
    return "Meu indexx"

@sorvetes_blueprint.route('/sorvetes', methods=['GET'])
def get_sorvetes():
    sorvetes = listar_sorvetes()
    return render_template("sorvetes.html", sorvetes=sorvetes)

@sorvetes_blueprint.route('/sorvetes/<int:id_sorvete>', methods=['GET'])
def get_sorvete(id_sorvete):
    try:
        sorvete = sorvete_por_id(id_sorvete)
        return render_template('sorvete_id.html', sorvete=sorvete)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'Sorvete não foi encontrado'}), 404

## ROTA ACESSAR O FORMULARIO DE CRIAÇÃO DE UM NOVO SORVETES   
@sorvetes_blueprint.route('/sorvetes/adicionar', methods=['GET'])
def adicionar_sorvete_page():
    return render_template('criarSorvetes.html')

## ROTA QUE CRIA UM NOVO SORVETE
@sorvetes_blueprint.route('/sorvetes', methods=['POST'])
def create_sorvete():
    sabor = request.form['sabor']
    categoria = request.form['categoria']
    preco = request.form['preco']
    qtd_estoque = request.form['qtd_estoque']
    novo_sorvete = {'sabor': sabor,
                    'categoria': categoria,
                    'preco': preco,
                    'qtd_estoque': qtd_estoque}
    adicionar_sorvete(novo_sorvete)
    return redirect(url_for('sorvetes.get_sorvetes'))

## ROTA PARA O FORMULARIO PARA EDITAR UM NOVO SORVETE
@sorvetes_blueprint.route('/sorvetes/<int:id_sorvete>/editar', methods=['GET'])
def editar_sorvete_page(id_sorvete):
    try:
        sorvete = sorvete_por_id(id_sorvete)
        return render_template('sorvete_update.html', sorvete=sorvete)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'Sorvete não foi encontrado'}), 404

## ROTA QUE EDITA UM SORVETE
@sorvetes_blueprint.route('/sorvetes/<int:id_sorvete>', methods=['PUT',"POST"])
def update_sorvete(id_sorvete):
    print("Dados foram enviados para o formulário:", request.form)
    try:
        sorvete = sorvete_por_id(id_sorvete)
        sabor = request.form['sabor']
        categoria = request.form['categoria']
        preco = request.form['preco']
        qtd_estoque = request.form['qtd_estoque']
        sorvete['sabor'] = sabor
        sorvete['categoria'] = categoria
        sorvete['preco'] = preco
        sorvete['qtd_estoque'] = qtd_estoque
        atualizar_sorvete(id_sorvete, sorvete)
        return redirect(url_for('sorvetes.get_sorvete', id_sorvete=id_sorvete))
    except SorveteNaoEncontrado:
        return jsonify({'message': 'Sorvete não foi encontrado'}), 404
   
## ROTA QUE DELETA UM SORVETE
@sorvetes_blueprint.route('/sorvetes/delete/<int:id_sorvete>', methods=['DELETE','POST'])
def delete_sorvete(id_sorvete):
    try:
        excluir_sorvete(id_sorvete)
        return redirect(url_for('sorvetes.get_sorvetes'))
    except SorveteNaoEncontrado:
        return jsonify({'message': 'Sorvete não foi encontrado'}), 404
