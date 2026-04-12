#1 - Define a imagem python de referência do container
FROM python:3.12-slim

#2 - Define o diretório de trabalho dentro do container
WORKDIR /app

#3 - Copia os arquivos de requisitos para o diretório de trabalho e instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#4 - Copia o restante dos arquivos do projeto para o diretório de trabalho
COPY . .

#5 - Define o comando de execução da API
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]