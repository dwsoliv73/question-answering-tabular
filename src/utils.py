import os

def format_answer(answer):
    if isinstance(answer, list):
        return str(answer)
    elif isinstance(answer, float):
        return f"{answer:.2f}"
    else:
        return str(answer)

def save_debug_log(log_text, reset=False):
    mode = "w" if reset else "a"
    with open("debug_log.txt", mode, encoding="utf-8") as f:
        f.write(log_text + "\n")

def debug_info(idx, dataset_id, question, template, args, df):
    log_text = (
        f"[{idx}] {dataset_id}\n"
        f"Q: {question}\n"
        f"Template: {template}\n"
        f"Args: {args}\n"
        f"Columns: {df.columns.tolist()}\n"
    )
    save_debug_log(log_text)
