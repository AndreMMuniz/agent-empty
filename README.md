# 🤖 Agent Empty - Template LangGraph + RAG

Este é um template de arquitetura robusta para criação de Agentes de IA Conversacional.
Ele utiliza **FastAPI** (Backend), **LangGraph** (Orquestração), **PostgreSQL/PGVector** (Memória e Vetores) e **Streamlit** (Frontend de Teste).

## 🏗️ Arquitetura

*   **API:** FastAPI (Async)
*   **Cérebro:** LangGraph (Stateful Multi-turn)
*   **Memória:** PostgreSQL (Checkpoints de conversa)
*   **RAG:** PGVector + LangChain Postgres
*   **Observabilidade:** Logs estruturados + LLM Judge + Dashboard Debugger
*   **Interface:** Streamlit

## 🚀 Como Iniciar

### 1. Configuração do Ambiente

1.  **Clone o repositório**:
    ```bash
    git clone <seu-repo>
    cd agent-empty
    ```

2.  **Crie o ambiente virtual**:
    ```powershell
    # Windows
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```
    ```bash
    # Linux/Mac
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Suba o Banco de Dados (Docker)**:
    ```bash
    docker-compose up -d
    ```

5.  **Configure o `.env`**:
    Copie o arquivo de exemplo:
    ```bash
    cp .env.example .env
    ```
    *(Ajuste as variáveis se necessário, como modelos do Ollama)*.

### 2. Ingestão de Dados (RAG)

Coloque seus arquivos (PDF, TXT, CSV, Imagens) na pasta `data/raw/` e execute:

```bash
python -m app.rag.ingestion
```
*Dica: O arquivo `sample.txt` já está lá para teste.*

### 3. Executando o Agente

Você precisará de **dois terminais**:

**Terminal 1: Backend (API)**
```bash
python run.py
```
*Acesse a documentação da API em: http://localhost:8000/docs*

**Terminal 2: Frontend (Dashboard)**
```bash
streamlit run frontend/app.py
```
*O dashboard abrirá automaticamente em: http://localhost:8501*

## 🧪 Testes e Avaliação

### Avaliação Automática (LLM Judge)
Para rodar a bateria de testes contra o `golden_dataset.jsonl`:

1.  Certifique-se de ter o modelo `deepseek-r1:8b` (ou configure outro no `judge.py`):
    ```bash
    ollama pull deepseek-r1:8b
    ```
2.  Execute o juiz:
    ```bash
    python -m app.evaluation.judge
    ```
3.  Verifique o relatório em `data/datasets/evaluation_report.md`.

---
**Desenvolvido como Architecture Template para Agentes Inteligentes.**
