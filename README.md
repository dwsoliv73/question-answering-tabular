---
## 🧠 Question Answering com Técnica Clássica de PLN

Este projeto resolve perguntas sobre tabelas (`.parquet`) usando uma pipeline baseada em técnicas clássicas de Processamento de Linguagem Natural (PLN), como **TF-IDF**, **regras heurísticas** e **execução programática com pandas**.
---

### ✅ Pré-requisitos

- Python 3.11+
- Instalar dependências:

```bash
pip install -r requirements.txt
```

---

### 📁 Estrutura de pastas

```
project/
├── data/
│   └── raw/
│       └── competition/
│           └── 066_IBM_HR/
│               └── all.parquet
│           └── test_qa.csv
├── src/
    └── modern/
        └── templates/
            └── ibm_hr.py
        ├── main.py
        ├── train.py
        ├── prediction.py
        ├── predictions.txt
│   ├── generate_predictions.py
│   ├── argument_extractor.py
│   ├── operation_executor.py
│   ├── template_matcher.py
│   ├── utils.py
│   └── clean_predictions.py
│   └── debug_log.py
│   └── evaluate_predictions_format.py
├── predictions.txt
└── predictions_clean.txt
```

---

### 🚀 Etapas de Execução

#### 1. **Gerar previsões com `all.parquet`**

```bash
python src/generate_predictions.py
```

- Isso percorre cada pergunta do `test_qa.csv`, identifica o dataset correspondente e gera uma resposta.
- As respostas são salvas em `predictions.txt`.
- Um log completo da execução é salvo em `debug_log.txt`.

📷 _Sugestão de print_: terminal com execução e exemplos de erros/sucessos do `debug_log.txt`.

---

#### 2. **Formatar as respostas para o padrão da competição**

```bash
python src/clean_predictions.py
```

- Entrada: `predictions.txt`
- Saída: `predictions_clean.txt` com respostas limpas e padronizadas:

  - Boolean: `True`, `False`
  - Number: `31.5`
  - Category: `Manager`
  - List: `["cat", "dog"]` ou `[23.5, 12.0]`

📷 _Sugestão de print_: `predictions_clean.txt` com respostas bem formatadas.

---

#### 3. **Avaliar o formato das respostas**

```bash
python src/evaluate_predictions_format.py
```

- Mostra estatísticas como:

  - Quantidade de respostas booleanas, numéricas, listas, inválidas etc.

📷 _Sugestão de print_: terminal com a análise do formato (output do script).

---

#### 4. **Analisar acertos via Debug**

```bash
python src/debug_log.py
```

- Verifica quantas perguntas falharam por `column = None`.
- Ajuda a diagnosticar falhas na extração de argumentos.

📷 _Sugestão de print_: estatística de acertos vs erros (coluna ausente, execução falha).

---

#### 4. **Técnica Moderna com DistilBERT**

```bash
cd src/modern
```

```bash
python main.py
```

### 💡 Técnica Clássica Utilizada

- **TemplateMatcher**: regras heurísticas + TF-IDF para identificar o tipo da pergunta.
- **ArgumentExtractor**: busca colunas e valores mencionados na pergunta.
- **OperationExecutor**: executa a operação correta no DataFrame.
- **Logs**: debug completo de cada execução salvo em `debug_log.txt`.

---

### 📈 Resultados Observados

- Respostas válidas em mais de **80% das perguntas** (formato).
- Pipeline robusta, com fallback em caso de erro.
- Técnica clássica ideal para perguntas diretas e datasets limpos.

---
