import json
import os
import re

def clean_line(line):
    line = line.strip()

    try:
        lower = line.lower()

        # Boolean
        if lower in {"true", "false", "yes", "no"}:
            return line.capitalize()

        # Number (int, float, negative, decimal)
        if re.fullmatch(r"-?\d+(\.\d+)?", line):
            return str(float(line)) if '.' in line or '-' in line else str(int(line))

        # List
        if line.startswith("[") and line.endswith("]"):
            parsed = eval(line)
            if not isinstance(parsed, list):
                return "Invalid"
            if all(isinstance(x, (int, float)) for x in parsed):
                return json.dumps(parsed)
            elif all(isinstance(x, str) for x in parsed):
                return json.dumps(parsed)
            else:
                return "Invalid"

        # Category (1 a 3 palavras, alfanumérico, sem símbolos estranhos)
        if len(line.split()) <= 3 and re.match(r"^[\w\s\.\,\-\&\(\)\']+$", line):
            return line.strip()

    except:
        pass

    return "Invalid"

def clean_predictions(input_path, output_path):
    cleaned = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            cleaned.append(clean_line(line))

    with open(output_path, "w", encoding="utf-8") as f:
        for item in cleaned:
            f.write(item + "\n")

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    input_path = os.path.join(base_path, "predictions.txt")
    output_path = os.path.join(base_path, "predictions_clean.txt")
    clean_predictions(input_path, output_path)
