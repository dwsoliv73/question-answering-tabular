def analyze_debug_log(file_path):
    total = 0
    errors = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("[" ) and "]" in line:
            total += 1
        if "Args:" in line and "'column': None" in line:
            errors += 1

    correct = total - errors
    if total == 0:
        print("Nenhuma pergunta encontrada no log.")
        return

    print(f"Total de perguntas analisadas: {total}")
    print(f"Respostas corretas: {correct} ({correct / total * 100:.2f}%)")
    print(f"Respostas erradas (column=None): {errors} ({errors / total * 100:.2f}%)")


if __name__ == "__main__":
    debug_log_path = "debug_log.txt"  # ajuste se necessário
    analyze_debug_log(debug_log_path)
