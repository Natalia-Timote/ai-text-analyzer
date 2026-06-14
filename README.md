# 🧠 AI Text Analyzer

**AI Text Analyzer** é uma aplicação Back-End desenvolvida em **Python**, que realiza análise de texto utilizando algoritmos de **NLP (Processamento de Linguagem Natural)**.
O projeto simula um serviço de análise textual, aplicando conceitos fundamentais de **API REST, validação de dados, separação de responsabilidades e testes automatizados**.

<hr>

## 🚀 Sobre o Projeto

A aplicação expõe uma API REST com dois endpoints principais:

* Verificar o status da aplicação via `/health`
* Analisar um texto e receber sentimento, palavras-chave e resumo via `/analyze`

A documentação interativa é gerada automaticamente pelo FastAPI e pode ser acessada pelo navegador, permitindo testar a API sem nenhuma ferramenta extra.

## 📚 Objetivos do Projeto

* Desenvolver uma **API REST em Python com FastAPI**
* Implementar **algoritmos de NLP** sem bibliotecas externas
* Aplicar **validação automática de dados** com Pydantic
* Trabalhar **separação de responsabilidades** entre lógica e endpoints
* Implementar **tratamento de erros e validações**
* Organizar o projeto com **testes unitários e de integração**
* Estruturar código **escalável e legível**

## 🧩 Funcionalidades

**Análise de Sentimento**
- Identificação de sentimento: Positivo, Neutro ou Negativo
- Score numérico de -1.0 a 1.0
- Baseada em léxico ponderado de palavras em português

**Extração de Palavras-chave**
- Retorna até 5 palavras mais relevantes do texto
- Remove stopwords em português automaticamente
- Ordenadas por frequência de ocorrência

**Sumarização Automática**
- Gera resumo com as frases mais relevantes
- Baseada em versão simplificada do algoritmo TextRank
- Pontua frases pela densidade de palavras-chave

**Validações automáticas**
- Texto vazio → erro 400
- Texto acima de 5000 caracteres → erro 400
- Campos ausentes → erro 422 (via Pydantic)

## 🛠️ Tecnologias Utilizadas

<p align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="80" height="80"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="80" height="80"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytest/pytest-original.svg" width="80" height="80"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" width="80" height="80"/>
</p>

**Tecnologias e conceitos aplicados no projeto:**
* **Python 3.12**
* **FastAPI**
* **Pydantic v2**
* **Uvicorn**
* **pytest + pytest-asyncio**
* **NLP local (sem APIs externas)**
* **Git & GitHub**

## 🔐 Boas Práticas

O projeto aplica:

* Validação automática de entrada via Pydantic
* Uso de try/except para tratamento de erros
* Separação de responsabilidades (lógica em `analyzer.py`, endpoints em `main.py`)
* Testes unitários das funções de NLP isoladas
* Testes de integração dos endpoints HTTP
* Arquitetura preparada para substituição por LLM externo
* Código organizado, comentado e legível

## 🖼️ Visualização do Projeto

**📄 Documentação Swagger gerada automaticamente**

Interface interativa para testar os endpoints diretamente pelo navegador.

<img src="/public/swagger-ui.png" alt="Documentação Swagger UI" width="600"/>

**✅ Resultado da análise**

Resposta da API com sentimento, score, palavras-chave e resumo.

<img src="/public/analyze-response.png" alt="Resposta do endpoint /analyze" width="600"/>

## 👩‍💻 Sobre a Autora

Desenvolvido por **Natalia Mirian Timote**, desenvolvedora e educadora em tecnologia e programação.

<a href="https://linkedin.com/in/nataliamiriantimote" target="_blank"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linkedin/linkedin-original.svg" width="40" height="40" /></a>
<a href="https://github.com/Natalia-Timote" target="_blank"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg" width="40" height="40" /></a>
