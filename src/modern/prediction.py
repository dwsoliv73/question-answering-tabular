import pandas as pd
from transformers import pipeline

def pipeline_qa(path_trained_model, df_context): 
  qa_pipeline = pipeline(
      "question-answering",
      model=path_trained_model,
      tokenizer=path_trained_model
  )

  with open("predictions.txt", "w") as f:
    for index, row in df_context.iterrows():
        pergunta = df_context['question'][index]
        resultado = qa_pipeline(question=pergunta, context=df_context['answer_text'][index])
        resposta = resultado['answer']
        f.write(f"{resposta}\n")