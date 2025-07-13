from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer

# Carrega o dataset a partir do seu arquivo JSON
# O 'field="data"' diz à biblioteca para olhar dentro da chave "data" no JSON
raw_datasets = load_dataset('json', data_files='dataset_qa_para_distilbert.json', field='data')

# (Opcional, mas recomendado) Dividir em treino e teste
# Vamos usar 90% para treino e 10% para teste
train_test_split = raw_datasets['train'].train_test_split(test_size=0.1)

# Criar um DatasetDict que é o formato padrão para o Trainer
datasets = DatasetDict({
    'train': train_test_split['train'],
    'test': train_test_split['test']
})

print(datasets)

# Usar um tokenizador "Fast" é importante para as funcionalidades de mapeamento
model_checkpoint = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

max_length = 384 # Comprimento máximo de uma feature (pergunta + contexto)
doc_stride = 128 # Sobreposição entre os pedaços quando o contexto é muito longo

def preprocess_qa_function(examples):
    # Padroniza as perguntas para evitar problemas de espaçamento
    questions = [q.strip() for q in examples["question"]]

    # Tokeniza as perguntas e contextos
    inputs = tokenizer(
        questions,
        examples["context"],
        max_length=max_length,
        truncation="only_second", # Trunca apenas o contexto, não a pergunta
        stride=doc_stride,
        return_overflowing_tokens=True, # Retorna os pedaços extras de contextos longos
        return_offsets_mapping=True, # Ajuda a mapear tokens de volta para o texto original
        padding="max_length",
    )

    offset_mapping = inputs.pop("offset_mapping")
    sample_mapping = inputs.pop("overflow_to_sample_mapping")
    answers = examples["answers"]
    start_positions = []
    end_positions = []

    for i, offset in enumerate(offset_mapping):
        sample_idx = sample_mapping[i]
        answer = answers[sample_idx]
        start_char = answer["answer_start"][0]
        end_char = start_char + len(answer["text"][0])
        
        # Encontra o início e o fim da sequência do contexto
        sequence_ids = inputs.sequence_ids(i)
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        # Se a resposta não estiver totalmente dentro do contexto atual, rotula como (0, 0)
        if offset[context_start][0] > start_char or offset[context_end][1] < end_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            # Caso contrário, encontra as posições de início e fim dos tokens
            idx = context_start
            while idx <= context_end and offset[idx][0] < start_char:
                idx += 1
            start_positions.append(idx)

            idx = context_end
            while idx >= context_start and offset[idx][1] > end_char:
                idx -= 1
            end_positions.append(idx)

    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions
    return inputs

# Aplica a função de pré-processamento ao nosso dataset
# batched=True acelera o processo. remove_columns remove as colunas antigas.

def train():
  tokenized_datasets = datasets.map(preprocess_qa_function, batched=True, remove_columns=datasets["train"].column_names)
  print(tokenized_datasets)

  # Carrega o modelo base para a tarefa de Question Answering
  model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)

  # Define os argumentos de treinamento
  # Lembre-se que o treinamento de transformers exige uma GPU para ser rápido
  args = TrainingArguments(
      output_dir="./resultados-distilbert-qa",
      learning_rate=2e-5,
      per_device_train_batch_size=8,
      per_device_eval_batch_size=8,
      num_train_epochs=3,
      weight_decay=0.01,
      eval_strategy="epoch",
      save_strategy="epoch",
      load_best_model_at_end=True,
  )

  # O Trainer gerencia todo o ciclo de treinamento e avaliação
  trainer = Trainer(
      model=model,
      args=args,
      train_dataset=tokenized_datasets["train"],
      eval_dataset=tokenized_datasets["test"],
      tokenizer=tokenizer, # Passar o tokenizador ajuda a salvar tudo junto
  )

  # Inicia o treinamento!
  trainer.train()

  # Salva o modelo final
  caminho_modelo_salvo = "./meu-modelo-distilbert-finetuned"
  trainer.save_model(caminho_modelo_salvo)