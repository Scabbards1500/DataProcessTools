import json

def filter_json(json1_path, json2_path, output_path):
    # 读取 json1
    with open(json1_path, "r", encoding="utf-8") as f:
        data1 = json.load(f)
    # 读取 json2
    with open(json2_path, "r", encoding="utf-8") as f:
        data2 = json.load(f)

    # 如果 json1 是单个对象而不是列表，统一处理成列表
    if isinstance(data1, dict):
        data1 = [data1]
    if isinstance(data2, dict):
        data2 = [data2]

    # 提取 json1 的所有 meme_id
    meme_ids = {item["meme_id"] for item in data1 if "meme_id" in item}

    # 筛选 json2 中 id 在 meme_ids 的对象
    filtered_data = [item for item in data2 if item.get("id") in meme_ids]

    # 保存结果
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"筛选完成，共找到 {len(filtered_data)} 条数据，已保存到 {output_path}")


if __name__ == "__main__":
    filter_json(r"D:\python\SymbolEvolver\dataset\MultiOff\all_symbol_evolver_errors.json",
                r"D:\python\SymbolEvolver\output\MultiOff\MultiOff_solver_output2.json",
                "D:\python\SymbolEvolver\output\MultiOff\MultiOff_solver_output_2.json")
