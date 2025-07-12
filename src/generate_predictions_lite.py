import pandas as pd
import os
from src.template_matcher import TemplateMatcher
from src.argument_extractor import extract_all_args
from src.operation_executor import execute_operation
from src.utils import format_answer, debug_info, save_debug_log  # <-- importante!

def generate_predictions_lite(qa_csv_path, base_data_path, template_path, output_path):
    matcher = TemplateMatcher(template_path)
    qa_df = pd.read_csv(qa_csv_path)
    predictions = []

    # Limpa o log no início da execução
    with open("debug_log.txt", "w", encoding="utf-8") as f:
        f.write("Iniciando nova execução\n\n")
    #rode so as primeiras 20 perguntas
    
    for idx, row in qa_df.iterrows():
        # seu código continua aqui normalmente

        question = row["question"]
        dataset_id = row["dataset"]
        parquet_path = os.path.join(base_data_path, dataset_id, "sample.parquet")

        if not os.path.exists(parquet_path):
            predictions.append("FileNotFound")
            continue

        try:
            df = pd.read_parquet(parquet_path)
        except Exception as e:
            predictions.append(f"ReadError: {e}")
            continue

        try:
            template = matcher.predict_template(question)
            args = extract_all_args(question, df)

            debug_info(idx, dataset_id, question, template, args, df)

            if args["column"] is not None and args["column"] not in df.columns:
                predictions.append("InvalidColumn")
                continue

            answer = execute_operation(template, df, **args)
            formatted = format_answer(answer)
            predictions.append(formatted)

        except Exception as e:
            predictions.append(f"Error: {e}")

    with open(output_path, "w", encoding="utf-8") as f:
        for p in predictions:
            f.write(p.strip() + "\n")


if __name__ == "__main__":
    # Limpa o arquivo no início da execução
    open("debug_log.txt", "w", encoding="utf-8").close()

    generate_predictions_lite(
        qa_csv_path="data/raw/competition/test_qa.csv",
        base_data_path="data/raw/competition",
        template_path="src/templates.json",
        output_path="predictions_lite.txt"
    )

