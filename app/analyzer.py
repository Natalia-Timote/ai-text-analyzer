"""
Módulo de análise de texto — sem dependência de APIs externas.

Técnicas usadas:
- Sentimento: léxico de palavras positivas/negativas (VADER-inspired, em PT)
- Palavras-chave: frequência de termos após remoção de stopwords
- Resumo: pontuação de frases por relevância (TextRank simplificado)
"""

import re
from collections import Counter

# --- Stopwords em português (palavras sem valor semântico) ---

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "do", "da",
    "dos", "das", "em", "no", "na", "nos", "nas", "por", "para", "com",
    "sem", "sob", "que", "se", "é", "e", "ou", "mas", "porém", "então",
    "como", "mais", "menos", "muito", "pouco", "já", "ainda", "também",
    "não", "sim", "eu", "tu", "ele", "ela", "nós", "eles", "elas",
    "me", "te", "se", "nos", "lhe", "lhes", "ao", "aos", "à", "às",
    "foi", "ser", "ter", "há", "isso", "este", "esta", "esse", "essa",
    "seu", "sua", "seus", "suas", "meu", "minha", "seus", "neste", "nessa",
}

# --- Léxico de sentimento (palavras com peso -1.0 a +1.0) ---

SENTIMENT_LEXICON: dict[str, float] = {
    # Positivas fortes
    "excelente": 1.0, "incrível": 1.0, "extraordinário": 1.0, "perfeito": 1.0,
    "fantástico": 1.0, "maravilhoso": 1.0, "brilhante": 0.9, "excepcional": 0.9,
    # Positivas médias
    "bom": 0.6, "boa": 0.6, "ótimo": 0.8, "ótima": 0.8, "legal": 0.5,
    "eficiente": 0.7, "versátil": 0.6, "poderoso": 0.7, "útil": 0.6,
    "fácil": 0.5, "rápido": 0.5, "confiável": 0.6, "inovador": 0.7,
    "moderno": 0.5, "popular": 0.4, "importante": 0.4, "interessante": 0.5,
    "recomendo": 0.7, "gosto": 0.6, "adoro": 0.9, "amo": 0.9, "adotei": 0.5,
    # Negativas médias
    "ruim": -0.6, "mau": -0.6, "má": -0.6, "difícil": -0.4, "lento": -0.5,
    "complexo": -0.3, "problema": -0.5, "erro": -0.6, "falha": -0.7,
    "instável": -0.6, "fraco": -0.5, "fraca": -0.5, "limitado": -0.4,
    # Negativas fortes
    "péssimo": -1.0, "terrível": -1.0, "horrível": -1.0, "inaceitável": -0.9,
    "desastre": -0.9, "fracasso": -0.8, "inútil": -0.8, "obsoleto": -0.6,
}

# --- Funções auxiliares ---

def _tokenize(text: str) -> list[str]:
    """Transforma texto em lista de palavras minúsculas, sem pontuação."""
    return re.findall(r'\b[a-záéíóúâêîôûãõàèìòùç]+\b', text.lower())


def _split_sentences(text: str) -> list[str]:
    """Divide texto em frases por pontuação."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]

# --- Funções principais ---

def analyze_sentiment(text: str) -> tuple[str, float]:
    """
    Calcula sentimento com base em léxico de palavras.

    Retorna: ("Positivo" | "Neutro" | "Negativo", score de -1.0 a 1.0)

    Lógica: soma os pesos de cada palavra encontrada no léxico,
    divide pelo total de palavras para normalizar.
    """
    words = _tokenize(text)
    if not words:
        return "Neutro", 0.0

    total_score = sum(SENTIMENT_LEXICON.get(w, 0.0) for w in words)
    normalized = total_score / len(words)
    normalized = max(-1.0, min(1.0, normalized * 10))  # amplifica e limita ao range

    if normalized >= 0.15:
        label = "Positivo"
    elif normalized <= -0.15:
        label = "Negativo"
    else:
        label = "Neutro"

    return label, round(normalized, 2)


def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    """
    Extrai palavras-chave por frequência, ignorando stopwords.

    Lógica: conta quantas vezes cada palavra aparece,
    remove as palavras comuns (stopwords) e retorna as mais frequentes.
    """
    words = _tokenize(text)
    meaningful = [w for w in words if w not in STOPWORDS and len(w) > 3]
    if not meaningful:
        return []

    counts = Counter(meaningful)
    return [word for word, _ in counts.most_common(top_n)]


def summarize(text: str, max_sentences: int = 2) -> str:
    """
    Gera um resumo escolhendo as frases mais relevantes.

    Lógica (TextRank simplificado):
    1. Extrai palavras-chave do texto completo
    2. Pontua cada frase pela quantidade de palavras-chave que ela contém
    3. Retorna as frases com maior pontuação (em ordem original)
    """
    sentences = _split_sentences(text)
    if not sentences:
        return text[:200]
    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    keywords = set(extract_keywords(text, top_n=10))

    def score_sentence(sentence: str) -> float:
        words = set(_tokenize(sentence))
        matches = words & keywords
        # Normaliza pelo tamanho da frase para não favorecer frases gigantes
        return len(matches) / (len(words) + 1)

    scored = sorted(enumerate(sentences), key=lambda x: score_sentence(x[1]), reverse=True)
    top_indices = sorted([i for i, _ in scored[:max_sentences]])
    return " ".join(sentences[i] for i in top_indices)
