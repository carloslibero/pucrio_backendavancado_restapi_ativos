#importa as bibliotecas necessárias para o projeto
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
#from flasgger import Swagger

from sqlalchemy.exc import IntegrityError

from model import Session, Ativo
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="RestAPI Ativos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
ativo_tag = Tag(name="Ativo", description="Adição, visualização e remoção de ativos à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#Rotas para os ativos

#Rota para inserção de ativos
@app.post('/ativo', tags=[ativo_tag],
          responses={"200": AtivoViewSchema, "400": ErrorSchema})
def add_ativo(form: AtivoSchema):
    """Adiciona uma nova Ativo à base de dados

    Retorna uma representação das ativos
    """
    ativo = Ativo(
        ativo=form.ativo,
        descricao=form.descricao,
        qtde=form.qtde,
        precoMedio=form.precoMedio)
    logger.debug(f"Adicionando ativo: '{ativo.ativo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando o ativo
        session.add(ativo)
        # Confirma a alteração no bando de dados
        session.commit()
        logger.debug(f"Adicionado ativo: '{ativo.ativo}'")
        return apresenta_ativo(ativo), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo ativo :/"
        logger.warning(f"Erro ao adicionar o ativo '{ativo.ativo}', {error_msg}")
        return {"message": error_msg}, 400

#Rota para buscar os ativos cadastrados
@app.get('/ativos', tags=[ativo_tag],
         responses={"200": ListagemAtivosSchema, "404": ErrorSchema})
def get_ativos():
    """Faz a busca por todos os Ativos cadastrados

    Retorna uma representação da listagem de ativos.
    """
    logger.debug(f"Coletando ativos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    ativos = session.query(Ativo).all()

    if not ativos:
        # se não há ativos cadastrados
        return {"ativos": []}, 200
    else:
        logger.debug(f"%d ativos encontrados" % len(ativos))
        # retorna a representação de ativos
        print(ativos)
        return apresenta_ativos(ativos), 200


#Rota para buscar ativo pelo código o ativo
@app.get('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema})
def get_ativo(query: AtivoBuscaSchema):
    """Faz a busca por um Ativo a partir do código do ativo informado

    Retorna uma representação do Ativo relacionado.
    """
    ativo_codigo = query.ativo
    logger.debug(f"Coletando dados sobre ativo #{ativo_codigo}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    ativo = session.query(Ativo).filter(Ativo.ativo == ativo_codigo).first()

    if not ativo:
        # se o ativo não foi encontrado
        error_msg = "Ativo não encontrado na base :/"
        logger.warning(f"Erro ao buscar o ativo '{ativo_codigo}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Ativo encontrado: '{ativo_codigo}'")
        # retorna a representação do ativo
        return apresenta_ativo(ativo), 200


#Rota para deletar ativos pelo código
@app.delete('/ativo', tags=[ativo_tag],
            responses={"200": AtivoDelSchema, "404": ErrorSchema})
def del_ativo(query: AtivoBuscaSchema):
    """Deleta um Ativo a partir do código do ativo informado

    Retorna uma mensagem de confirmação da remoção.
    """
    ativo_codigo = unquote(unquote(query.ativo))
    print(ativo_codigo)
    logger.debug(f"Deletando dados sobre ativo #{ativo_codigo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Ativo).filter(Ativo.ativo == ativo_codigo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado ativo #{ativo_codigo}")
        return {"message": "Ativo removido", "descrição": ativo_codigo}
    else:
        # se o ativo não foi encontrado
        error_msg = "Ativo não encontrado na base :/"
        logger.warning(f"Erro ao deletar ativo #'{ativo_codigo}', {error_msg}")
        return {"mesage": error_msg}, 404