#importa as bibliotecas necessárias para a classe
from sqlalchemy import *
from datetime import datetime
from model import Base
from typing import Union

#Classe Ativo - Irá ter todos os ativos de um usuário, não suporte a login
class Ativo(Base):
    __tablename__ = 'ativo'

    ativo = Column("pk_ativo", String(6), primary_key=True)
    descricao = Column(String(255), unique=True, nullable=False)
    qtde = Column(Integer, nullable=False)
    precoMedio = Column(Numeric(10,2), nullable=False)
    
    def __init__(self, ativo:str, descricao:str, qtde:float, precoMedio:float):
        """
        Cria um novo ativo

        Parametros:
            ativo: Código B3 de até 6 dígitos, exemplo VALE3
            descrição: descrição do ativo
            qtde: Quantidade de papéis do ativo
            precoMedio: Preço médio de um dos ativos
        """
        self.ativo = ativo
        self.descricao = descricao
        self.qtde = qtde
        self.precoMedio = precoMedio