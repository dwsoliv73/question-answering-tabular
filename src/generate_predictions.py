import os
import pandas as pd
from template_matcher import TemplateMatcher
from argument_extractor import extract_all_args
from operation_executor import execute_operation
from utils import format_answer, debug_info, save_debug_log

def main():
    # Caminho base do projeto
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Caminhos dos arquivos
    qa_path = os.path.join(base_path, "data", "raw", "competition", "test_qa.csv")
    dataset_base_path = os.path.join(base_path, "data", "raw", "competition")
    template_path = os.path.join(base_path, "src", "templates.json")
    output_path = os.path.join(base_path, "predictions.txt")

    # Limpa o log no início
    save_debug_log("Início da execução\n", reset=True)

    # Leitura das perguntas
    questions = pd.read_csv(qa_path)
    matcher = TemplateMatcher(template_path=template_path)

    predictions = []

    for idx, row in questions.iterrows():
        question = row["question"]
        dataset_id = row["dataset"]

        dataset_path = os.path.join(dataset_base_path, dataset_id, "all.parquet")
        if not os.path.exists(dataset_path):
            save_debug_log(f"[{idx}] Arquivo não encontrado: {dataset_path}")
            predictions.append("FileNotFound")
            continue

        try:
            df = pd.read_parquet(dataset_path)
        except Exception as e:
            save_debug_log(f"[{idx}] Erro ao ler {dataset_path}: {e}")
            predictions.append(f"ReadError")
            continue

        try:
            template = matcher.predict_template(question)
            args = extract_all_args(question, df)

            # Log detalhado
            debug_info(idx, dataset_id, question, template, args, df)

            if args.get("column") and args["column"] not in df.columns:
                save_debug_log(f"[{idx}] Coluna inválida: {args['column']}")
                predictions.append("InvalidColumn")
                continue

            answer = execute_operation(template, df, **args)
            formatted = format_answer(answer)
            predictions.append(formatted)

        except Exception as e:
            save_debug_log(f"[{idx}] Erro durante a operação: {e}")
            predictions.append("Error")

    with open(output_path, "w", encoding="utf-8") as f:
        for p in predictions:
            f.write(p.strip() + "\n")


if __name__ == "__main__":
    main()
