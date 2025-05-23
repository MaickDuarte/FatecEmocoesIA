# Usa imagem oficial Python como base
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia requirements.txt (ou diretamente o comando pip install)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte para dentro da imagem
COPY . .

# Expõe a porta padrão usada pelo uvicorn
EXPOSE 8080

# Comando para rodar sua API
CMD ["uvicorn", "apiEmocoes:app", "--host", "0.0.0.0", "--port", "8080"]
