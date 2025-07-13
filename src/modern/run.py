from transformers import pipeline

# Carrega o seu modelo treinado usando a pipeline
qa_pipeline = pipeline(
    "question-answering",
    model=caminho_modelo_salvo,
    tokenizer=caminho_modelo_salvo
)

# Use o mesmo contexto que foi usado no treinamento
# Vamos recriá-lo a partir do arquivo original
import pandas as pd
df_data = pd.read_csv("sample.csv")
contexto_para_teste = df_data.to_csv(index=False)

# Faça uma nova pergunta
pergunta = "Is the highest DailyRate equal to 1499?"

resultado = qa_pipeline(question=pergunta, context=contexto_para_teste)

print(f"Pergunta: {pergunta}")
print(f"Resposta: {resultado['answer']}")
print(f"Score de Confiança: {resultado['score']:.4f}")