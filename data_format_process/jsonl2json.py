import json


def convert_jsonl_to_json(jsonl_path, output_path):
    data = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        buffer = ''
        for line in f:
            # 连续读取直到一个完整的JSON对象
            buffer += line.strip()
            if buffer.endswith('}'):
                try:
                    item = json.loads(buffer)
                    data.append(item)
                    buffer = ''
                except json.JSONDecodeError:
                    buffer += ' '

    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(data, out_f, indent=2, ensure_ascii=False)

    print(f"✅ 转换完成！共 {len(data)} 条记录保存到 {output_path}")


# 示例使用
convert_jsonl_to_json(r"C:\Users\scaaa\Downloads\Compressed\archive_4\data\test.jsonl",
                      r"C:\Users\scaaa\Downloads\Compressed\archive_4\data\test.json")
