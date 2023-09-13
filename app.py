# openapi3 - framework baseado no Flask que verifica dados e gera documentação automatizada
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from model import Session
from logger import logger
from schemas.error import ErrorSchema
from schemas.categoria import *
from flask_cors import CORS

info = Info(title="Categorias", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags, uma para cada contexto
home_tag = Tag(name="Documentação das APIs",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

categoria_tag = Tag(
    name="Categoria", description="Adição e listagem de categorias cadastradas na base.")


# agrupa as tags nas rotas conforme seu contexto. aqui está a tag home_tag sendo usada.
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/categoria', tags=[categoria_tag],
          responses={"200": CategoriaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_categoria(form: CategoriaSchema):
    """Adiciona uma nova categoria à base de dados

    Retorna uma representação da categoria.
    """
    categoria = Categoria(
        nome=form.nome,
        tipo=form.tipo)

    logger.debug(
        f"Adicionando a categoria: '{categoria.nome}' do tipo: '{categoria.tipo}'")
    try:
        # criando conexão com a base
        session = Session()

        # adicionando uma categoria
        session.add(categoria)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(
            f"Adicionado categoria de nome: '{categoria.nome}' do tipo: '{categoria.tipo}'")

        # usa como retorno os schemas criados no diretório schemas
        return apresenta_categoria(categoria), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Categoria de mesmo nome já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar categoria '{categoria.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

@app.get('/categorias', tags=[categoria_tag],
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def get_categorias():
    """Faz a busca por todas as categorias cadastradas

    Retorna uma representação da listagem de categorias.
    """

    logger.debug(f"Coletando categorias ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    categorias = session.query(Categoria).all()

    if not categorias:
        # se não há categorias cadastradas
        return {"categorias": []}, 200
    else:
        logger.debug(f"%d categorias encontradas" % len(categorias))
        # retorna a representação de comentarios
        print(categorias)
        return apresenta_categorias(categorias), 200


@app.get('/categoriastipo', tags=[categoria_tag],
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def get_tipos(query: CategoriaBuscaTipoSchema):
    """Faz a busca por todas as categorias cadastradas

    Retorna uma representação da listagem de categorias.
    """
    categoria_tipo = query.tipo
    logger.debug(f"Coletando categorias ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    categorias = session.query(Categoria).filter(
        Categoria.tipo == categoria_tipo).all()

    if not categorias:
        # se não há categorias cadastradas
        return {"categorias": []}, 200
    else:
        logger.debug(f"%d categorias encontradas" % len(categorias))
        # retorna a representação de comentarios
        print(categorias)
        return apresenta_categorias(categorias), 200


@app.get('/categoriaNome', tags=[categoria_tag],
         responses={"200": CategoriaViewSchema, "404": ErrorSchema})
def get_categoria(query: CategoriaBuscaNomeSchema):
    """Faz a busca por uma Despesa a partir do nome. Função não usada no front-end.

    Retorna uma representação da despesa encontrada.
    """
    if query.nome !="": 

        categoria_nome = query.nome
        logger.debug(f"Coletando dados sobre nome da categoria #{categoria_nome}")

        # criando conexão com a base
        session = Session()
        # fazendo a busca
        categoria = session.query(Categoria).filter(
            Categoria.nome == categoria_nome).first()

        if not categoria:
            # se a despesa não foi encontrada
            error_msg = "Despesa não encontrada na base :/"
            logger.warning(
                f"Erro ao buscar despesa '{categoria_nome}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            logger.debug(f"Categoria encontrada: '{categoria_nome}'")
            # retorna a representação da despesa
            return retorna_categoria(categoria), 200
    else:
        error_msg = "Precisa informar categoria :/"
        logger.warning(f"Erro ao buscar categoria '{error_msg}'")
        return {"mesage": error_msg}, 404

@app.get('/categoriaID', tags=[categoria_tag],
         responses={"200": CategoriaViewSchema, "404": ErrorSchema})
def get_categoriaID(query: CategoriaBuscaIDSchema):
    """Faz a busca por uma Despesa a partir do nome. Função não usada no front-end.

    Retorna uma representação da despesa encontrada.
    """
    logger.debug(f"Preencheu id categoria? #{query.id}")
    if query.id !=0:

        categoria_id = query.id
        logger.debug(f"Coletando dados sobre id categoria #{categoria_id}")
        # criando conexão com a base

        session = Session()
        # fazendo a busca
        categoria = session.query(Categoria).filter(
            Categoria.id == categoria_id).first()

        if not categoria:
            # se a despesa não foi encontrada
            error_msg = "Categoria não encontrada na base :/"
            logger.warning(
                f"Erro ao buscar despesa '{categoria_id}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            logger.debug(f"Categoria encontrada: '{categoria_id}'")
            # retorna a representação da despesa
            return retorna_categoria(categoria), 200

    else:
        error_msg = "Precisa informar categoria :/"
        logger.warning(f"Erro ao buscar categoria '{error_msg}'")
        return {"mesage": error_msg}, 404


@app.put('/categoria', tags=[categoria_tag],
         responses={"200": CategoriaPutDelSchema, "404": ErrorSchema})
def edita_categoria(query: CategoriaViewSchema):
    """Atualiza uma categoria a partir do nome informado. 

    """
    categoria_id = query.id
    categoria_nome = unquote(unquote(query.nome))
    categoria_tipo = unquote(unquote(query.tipo))

    print(categoria_nome)
    logger.debug(f"Atualizando dados sobre categoria #{categoria_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    categoria = session.query(Categoria).filter(
        Categoria.id == categoria_id).first()

    if categoria:
        categoria.nome = categoria_nome
        categoria.tipo = categoria_tipo
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Atualizando categoria #{categoria_nome}")
        return {"mesage": "Categoria atualizada", "nome": categoria_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Categoria não encontrado na base :/"
        logger.warning(
            f"Erro ao atualizar categoria #'{categoria_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.delete('/categoria', tags=[categoria_tag],
            responses={"200": CategoriaPutDelSchema, "404": ErrorSchema})
def del_categoria(query: CategoriaBuscaNomeSchema):
    """Deleta uma categoria a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """

    categoria_nome = unquote(unquote(query.nome))

    print(categoria_nome)
    logger.debug(f"Deletando dados sobre categoria #{categoria_nome}")
    # criando conexão com a base
    session = Session()

    id_categoria = session.query(Categoria).filter(
        Categoria.nome == categoria_nome).first()

    if id_categoria:

        # fazendo a remoção
        session.query(Categoria).filter(
            Categoria.nome == categoria_nome).delete()
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado categoria #{categoria_nome}")
        return {"mesage": "Categoria removida", "nome": categoria_nome}
    else:
        # se a categoria não foi encontrada
        error_msg = "Categoria não encontrada na base :/"
        logger.warning(
            f"Erro ao deletar categoria #'{categoria_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
