from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from model.categoria import Categoria


class CategoriaSchema(BaseModel):
    """ Define como uma nova categoria a ser inserida deve ser representada.
    """
    # id: int = 1
    nome: str = "Alimentação"
    tipo: str = "Despesa"


class CategoriaViewSchema(BaseModel):
    """ Define como um categoria será retornada.
    """
    id: int = 1
    nome: str = "Alimentação"
    tipo: str = "Despesa"


class CategoriaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID da categoria.
    """
    id: int = 0


class CategoriaBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da categoria.
    """
    nome: str = ""


class CategoriaBuscaIDSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID da categoria.
    """
    id: int = 0


class CategoriaBuscaTipoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por tipo de categoria. Que será
        feita apenas com base no tipo da categoria.
    """
    tipo: str = "Despesa"


class ListagemCategoriasSchema(BaseModel):
    """ Define como uma listagem de categorias será retornada.
    """
    categoria: List[CategoriaViewSchema]


class CategoriaPutDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    categoria: CategoriaViewSchema
    mesage: str


def apresenta_categorias(categorias: List[Categoria]):
    """ Retorna uma representação da categoria seguindo o schema definido em
        Categoria.
    """
    result = []
    for categoria in categorias:
        result.append({
            "id": categoria.id,
            "nome": categoria.nome,
            "tipo": categoria.tipo
        })

    return {"categorias": result}


def apresenta_categoria(categoria: Categoria):
    """ Retorna uma representação da Categoria seguindo o schema definido em
        Categoria.
    """
    return {
        "id": categoria.id,
        "nome": categoria.nome,
        "tipo": categoria.tipo
    }


def retorna_categoria(categoria):
    """ Retorna uma representação da despesa seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": categoria.id,
        "nome": categoria.nome,
        "tipo": categoria.tipo
    }
