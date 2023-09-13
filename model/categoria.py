from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union
from model import Base

class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column("pk_categoria", Integer, primary_key=True)
    nome = Column(String(140))
    tipo = Column(String(20))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, tipo: str, data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Categoria

        Arguments:
            nome: o nome de uma categoria.
            data_insercao: data de quando a categoria foi criada ou inserida.
                           à base
        """
        self.nome = nome
        self.tipo = tipo
        if data_insercao:
            self.data_insercao = data_insercao


