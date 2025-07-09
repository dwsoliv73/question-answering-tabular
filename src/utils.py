# utils.py

def format_answer(answer):
    if isinstance(answer, list):
        return str(answer)
    elif isinstance(answer, float):
        return f"{answer:.2f}"
    elif isinstance(answer, bool):
        return str(answer)
    elif answer is None:
        return "None"
    return str(answer)


def debug_info(idx, dataset_id, question, template, args, df):
    print(f"\n--- [{idx}] ---")
    print(f"📂 Dataset: {dataset_id}")
    print(f"❓ Pergunta: {question}")
    print(f"📑 Template: {template}")
    print(f"📥 Args: {args}")
    print(f"📊 Colunas: {df.columns.tolist()}")
    
    save_debug_log(f"[{idx}] {dataset_id}\nQ: {question}\nTemplate: {template}\nArgs: {args}\n")

    
def save_debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")


