Como rodar o projeto de Análise de Emoções
Para executar o projeto você precisa:

Ter o Python 3.10+ instalado.

Instalar as bibliotecas necessárias pelo terminal (cmd ou PowerShell):
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn transformers deep-translator

Rodar a API com o comando:
python -m uvicorn apiEmocoes:app --reload --host 0.0.0.0 --port 8000
Isso vai iniciar o servidor local da API na porta 8000.

Abrir o arquivo index.html no navegador para usar a interface gráfica.

Digitar o texto que deseja analisar, clicar em "Analisar Emoções" e ver o resultado na tela.

Resumo das bibliotecas usadas:

fastapi — para criar a API web

uvicorn — servidor para rodar a API localmente

transformers — modelo pré-treinado para análise de emoções

deep-translator — para traduzir texto do português para o inglês automaticamente