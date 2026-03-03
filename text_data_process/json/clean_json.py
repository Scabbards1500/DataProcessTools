import json

# === 文件路径配置 ===
input_file = 'D:\python\FastAPI_study\gilead_test\data\oncology_with_history_ori.json'       # 替换为你的原始 JSON 文件路径
output_file = 'D:\python\FastAPI_study\gilead_test\data\oncology_with_history_final.json'   # 去重后的输出文件路径

# === 读取 JSON 文件 ===
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# === 去重逻辑（保留第一条）===
seen_queries = set()
unique_items = []
for item in data:
    query = item.get('query')
    if query and query not in seen_queries:
        seen_queries.add(query)
        unique_items.append(item)

# === 保存结果 ===
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(unique_items, f, ensure_ascii=False, indent=2)

