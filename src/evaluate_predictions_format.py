import json
import re

def detect_type(answer):
    answer = answer.strip()

    # Boolean
    if answer.lower() in {"true", "false", "yes", "no"}:
        return "Boolean"

    # Number
    if re.fullmatch(r"-?\d+(\.\d+)?", answer):
        return "Number"

    # List
    if answer.startswith("[") and answer.endswith("]"):
        try:
            parsed = json.loads(answer)
            if all(isinstance(x, (int, float)) for x in parsed):
                return "List[number]"
            if all(isinstance(x, str) for x in parsed):
                return "List[category]"
        except:
            return "Invalid"

    # Category (palavra ou frase curta)
    if len(answer.split()) <= 3:
        return "Category"

    return "Invalid"


def evaluate_format(file_path):
    counts = {
        "Boolean": 0,
        "Number": 0,
        "Category": 0,
        "List[category]": 0,
        "List[number]": 0,
        "Invalid": 0
    }

    total = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            total += 1
            t = detect_type(line.strip())
            counts[t] += 1

    print(f"\nTotal de respostas: {total}\n")
    for key, value in counts.items():
        percent = (value / total * 100) if total > 0 else 0
        print(f"{key:<15}: {value:>5} respostas  ({percent:.2f}%)")


if __name__ == "__main__":
    evaluate_format("predictions_clean.txt")  # ajuste se necessário
