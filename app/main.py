from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.analyzer import analyze_sentiment, extract_keywords, summarize

app = FastAPI(
    title="AI Text Analyzer",
    description="API REST para análise de texto com NLP local — sem APIs externas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos Pydantic (contrato da API) ---

class TextInput(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    summary: str
    sentiment: str
    sentiment_score: float    # -1.0 (negativo) até 1.0 (positivo)
    keywords: list[str]
    word_count: int
    char_count: int

class HealthResponse(BaseModel):
    status: str
    version: str

# --- Endpoints ---

@app.get("/health", response_model=HealthResponse, tags=["Status"])
async def health_check():
    """Verifica se a API está funcionando."""
    return {"status": "ok", "version": "1.0.0"}


@app.post("/analyze", response_model=AnalysisResult, tags=["Análise"])
async def analyze_text(payload: TextInput):
    """
    Analisa um texto e retorna:
    - Resumo das frases mais relevantes
    - Sentimento (Positivo / Neutro / Negativo) com score
    - Palavras-chave principais (até 5)
    - Contagem de palavras e caracteres
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="O campo 'text' não pode estar vazio.")

    if len(payload.text) > 5000:
        raise HTTPException(status_code=400, detail="Texto muito longo. Limite: 5000 caracteres.")

    sentiment_label, sentiment_score = analyze_sentiment(payload.text)

    return AnalysisResult(
        summary=summarize(payload.text),
        sentiment=sentiment_label,
        sentiment_score=sentiment_score,
        keywords=extract_keywords(payload.text),
        word_count=len(payload.text.split()),
        char_count=len(payload.text),
    )
