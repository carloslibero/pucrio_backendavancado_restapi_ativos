from pydantic import BaseModel
from typing import Optional, List
from model.ativo import Ativo

class AtivoSchema(BaseModel):
    """ Define como um novo ativo a ser inserido deve ser representado
    """
    ativo: str = "VALE3"
    descricao: str = "Vale S.A."
    qtde: float = 100.00
    precoMedio: float = 85.10

class AtivoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base nos dados do ativo.
    """
    ativo: str = "VALE3"

class ListagemAtivosSchema(BaseModel):
    """ Define como uma listagem de ativos será retornada.
    """
    ativos:List[AtivoSchema]

def apresenta_ativos(ativos: List[Ativo]):
    """ Retorna uma representação do ativo seguindo o schema definido em
        AtivoViewSchema.
    """
    result = []
    for ativo in ativos:
        result.append({
            "ativo": ativo.ativo,
            "descricao": ativo.descricao,
            "qtde": ativo.qtde,
            "precoMedio": ativo.precoMedio,
        })

    return {"ativos": result}

class AtivoViewSchema(BaseModel):
    """ Define como um ativo será retornado: 
    """
    ativo: str = "VALE3"
    descricao: str = "Vale S.A."
    qtde: float = 100.00
    precoMedio: float = 85.10

class AtivoDelSchema(BaseModel):
    """ Define a estrutura a ser retornada após a deleção de um ativo.
    """
    message: str

def apresenta_ativo(ativo: Ativo):
    """ Retorna uma representação do ativo seguindo o schema definido em
        AtivoViewSchema.
    """
    return {
        "ativo": ativo.ativo,
        "descricao": ativo.descricao,
        "qtde": ativo.qtde,
        "precoMedio": ativo.precoMedio,
    }