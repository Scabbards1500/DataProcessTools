import json

def jsonl_to_json(input_path, output_path):
    data = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:  # 跳过空行
                data.append(json.loads(line))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Converted {input_path} → {output_path}")


if __name__ == "__main__":
    input_path = r"D:\python\DataProcessTools\text_data_process\form\time_entites.jsonl"
    output_path = r"D:\python\DataProcessTools\text_data_process\form\time_entites.json"
    jsonl_to_json(input_path, output_path)