from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer

model_checkpoint = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

max_length = 384
doc_stride = 128 

def preprocess_qa_function(examples):
    questions = [q.strip() for q in examples["question"]]
    inputs = tokenizer(
        questions,
        examples["context"],
        max_length=max_length,
        truncation="only_second", 
        stride=doc_stride,
        return_overflowing_tokens=True, 
        return_offsets_mapping=True,
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
        
        sequence_ids = inputs.sequence_ids(i)
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        if offset[context_start][0] > start_char or offset[context_end][1] < end_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
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

def train(json_path):
  raw_datasets = load_dataset('json', data_files=json_path, field='data')

  train_test_split = raw_datasets['train'].train_test_split(test_size=0.1)

  datasets = DatasetDict({
      'train': train_test_split['train'],
      'test': train_test_split['test']
  })

  tokenized_datasets = datasets.map(preprocess_qa_function, batched=True, remove_columns=datasets["train"].column_names)
  print(tokenized_datasets)

  model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)

  args = TrainingArguments(
      output_dir="./resultados-qa",
      learning_rate=2e-5,
      per_device_train_batch_size=8,
      per_device_eval_batch_size=8,
      num_train_epochs=3,
      weight_decay=0.01,
      eval_strategy="epoch",
      save_strategy="epoch",
      load_best_model_at_end=True,
  )

  trainer = Trainer(
      model=model,
      args=args,
      train_dataset=tokenized_datasets["train"],
      eval_dataset=tokenized_datasets["test"],
      tokenizer=tokenizer,
  )
  
  trainer.train()

  caminho_modelo_salvo = "./meu-modelo"
  trainer.save_model(caminho_modelo_salvo)
