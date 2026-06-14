"""
Testes do módulo analyzer.py

Aqui testamos a lógica pura — sem HTTP, sem mock, sem API.
Cada função é testada de forma isolada e determinística.
"""

import pytest
from app.analyzer import analyze_sentiment, extract_keywords, summarize

# ---- Sentimento ----

def test_sentiment_positive():
    text = "Python é uma linguagem incrível e fantástica para desenvolvimento."
    label, score = analyze_sentiment(text)
    assert label == "Positivo"
    assert score > 0

def test_sentiment_negative():
    text = "Este sistema é péssimo, cheio de erros e falhas terríveis."
    label, score = analyze_sentiment(text)
    assert label == "Negativo"
    assert score < 0

def test_sentiment_neutral():
    text = "O arquivo foi salvo no diretório especificado pelo usuário."
    label, score = analyze_sentiment(text)
    assert label == "Neutro"

def test_sentiment_score_range():
    """Score deve estar sempre entre -1.0 e 1.0."""
    texts = [
        "Excelente! Maravilhoso! Incrível! Fantástico!",
        "Péssimo! Terrível! Horrível! Desastre!",
        "O gato sentou no tapete.",
    ]
    for text in texts:
        _, score = analyze_sentiment(text)
        assert -1.0 <= score <= 1.0

def test_sentiment_empty_text():
    label, score = analyze_sentiment("")
    assert label == "Neutro"
    assert score == 0.0

# ---- Palavras-chave ----

def test_keywords_returns_list():
    text = "Python é usado para desenvolvimento web, análise de dados e inteligência artificial."
    keywords = extract_keywords(text)
    assert isinstance(keywords, list)

def test_keywords_max_5():
    text = "Python JavaScript TypeScript Angular React Node Django Flask FastAPI desenvolvimento frontend backend"
    keywords = extract_keywords(text)
    assert len(keywords) <= 5

def test_keywords_no_stopwords():
    """Palavras como 'de', 'para', 'com' não devem aparecer como keywords."""
    text = "Python é muito bom para desenvolvimento de aplicações modernas."
    keywords = extract_keywords(text)
    stopwords_found = [w for w in keywords if w in {"para", "muito", "é", "de"}]
    assert stopwords_found == []

def test_keywords_most_frequent_first():
    """A palavra mais repetida deve aparecer primeiro."""
    text = "Python Python Python é bom. Python é rápido. JavaScript também é bom."
    keywords = extract_keywords(text)
    assert keywords[0] == "python"

def test_keywords_empty_text():
    assert extract_keywords("") == []

# ---- Resumo ----

def test_summary_short_text_unchanged():
    """Texto com 1 frase deve retornar a própria frase."""
    text = "Python é uma linguagem de programação versátil."
    result = summarize(text)
    assert result == text

def test_summary_long_text_is_shorter():
    """Resumo deve ser menor que o texto original quando há muitas frases."""
    text = (
        "Python é uma linguagem de programação de alto nível. "
        "Foi criada por Guido van Rossum em 1991. "
        "É muito utilizada em ciência de dados e inteligência artificial. "
        "Também é popular para desenvolvimento web com frameworks como Django e FastAPI. "
        "Sua sintaxe limpa facilita o aprendizado para iniciantes."
    )
    result = summarize(text)
    assert len(result) < len(text)

def test_summary_returns_string():
    text = "Esta é uma frase de teste. Esta é outra frase importante. E mais uma aqui."
    result = summarize(text)
    assert isinstance(result, str)
    assert len(result) > 0

def test_summary_max_sentences():
    """Por padrão o resumo deve ter no máximo 2 frases."""
    text = " ".join([f"Esta é a frase número {i} do texto longo." for i in range(10)])
    result = summarize(text)
    # Conta frases pelo número de pontos finais
    sentence_count = len([s for s in result.split(".") if s.strip()])
    assert sentence_count <= 2
