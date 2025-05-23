from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from collections import defaultdict
from deep_translator import GoogleTranslator

# Traduz texto PT->EN
def traduzir_texto(texto):
    return GoogleTranslator(source='pt', target='en').translate(texto)

# Inicializa o modelo uma vez só
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def analisar_emocoes(texto, threshold=2.0):
    resultados = classifier(texto)[0]
    emocao_dict = {r['label'].lower(): r['score'] for r in resultados}

    grupos = {
        "Feliz": ["joy"],
        "Surpreso": ["surprise"],
        "Triste": ["sadness"],
        "Raiva": ["anger"],
        "Medo": ["fear"],
        "Nojo": ["disgust"],
        "Neutro": ["neutral"]
    }

    emocoes_finais = defaultdict(float)
    for grupo, labels in grupos.items():
        for label in labels:
            emocoes_finais[grupo] += emocao_dict.get(label, 0)

    total = sum(emocoes_finais.values())
    porcentagens = {k: round((v / total) * 100, 2) for k, v in emocoes_finais.items()}

    porcentagens_filtradas = {k: (v if v >= threshold else 0.0) for k, v in porcentagens.items()}

    soma_filtrada = sum(porcentagens_filtradas.values())
    if soma_filtrada > 0:
        porcentagens_normalizadas = {k: round((v / soma_filtrada) * 100, 2) for k, v in porcentagens_filtradas.items()}
    else:
        porcentagens_normalizadas = porcentagens_filtradas

    emocao_dominante = max(porcentagens_normalizadas.items(), key=lambda x: x[1])[0]

    return porcentagens_normalizadas, emocao_dominante

# FastAPI app
app = FastAPI()

# CORS - permita seu front-end acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para testar, aceita tudo, depois restringe para seu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para receber JSON
class TextoInput(BaseModel):
    texto: str

@app.post("/analisar")
async def analisar_emocoes_endpoint(dados: TextoInput):
    texto = dados.texto
    texto_traduzido = traduzir_texto(texto)
    resultado, dominante = analisar_emocoes(texto_traduzido)
    return {"resultado": resultado, "dominante": dominante}

# Adição para rodar no Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apiEmocoes:app", host="0.0.0.0", port=10000)
