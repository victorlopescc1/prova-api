from config import db
class Sorvete(db.Model):
    id_sorvete = db.Column(db.Integer, primary_key=True)
    sabor = db.Column(db.String(100))
    categoria = db.Column(db.String(100))
    preco = db.Column(db.Float)
    qtd_estoque = db.Column(db.Integer)
    def __init__(self, sabor, categoria, preco, qtd_estoque):
        self.sabor = sabor
        self.categoria = categoria
        self.preco = preco
        self.qtd_estoque = qtd_estoque
    def to_dict(self):
        return {'id': self.id_sorvete,
                'sabor': self.sabor,
                'categoria': self.categoria,
                'preco': self.preco,
                'qtd_estoque': self.qtd_estoque}
class Categoria(db.Model):
    categoria_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

    def __init__(self, nome):
        self.nome = nome
    def to_dict(self):
        return {'id': self.categoria_id,
                'nome': self.nome}
class SorveteNaoEncontrado(Exception):
    pass
def sorvete_por_id(id_sorvete):
    sorvete = Sorvete.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    return sorvete.to_dict()
def listar_sorvetes():
    sorvetes = Sorvete.query.all()
    return [sorvete.to_dict() for sorvete in sorvetes]
def adicionar_sorvete(sorvete_data):
    novo_sorvete = Sorvete(sabor=sorvete_data['sabor'],
                           categoria=sorvete_data['categoria'],
                           preco=sorvete_data['preco'],
                           qtd_estoque=sorvete_data['qtd_estoque'])
    db.session.add(novo_sorvete)
    db.session.commit()
def atualizar_sorvete(id_sorvete, novos_dados):
    sorvete = Sorvete.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    sorvete.sabor = novos_dados['sabor']
    sorvete.categoria = novos_dados['categoria']
    sorvete.preco = novos_dados['preco']
    sorvete.qtd_estoque = novos_dados['qtd_estoque']
    db.session.commit()
def excluir_sorvete(id_sorvete):
    sorvete = Sorvete.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    db.session.delete(sorvete)
    db.session.commit()