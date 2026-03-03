import json

def filter_mismatched(json1_path, json2_path, output_path):
    # 读取 json1 和 json2
    with open(json1_path, "r", encoding="utf-8") as f:
        data1 = json.load(f)
    with open(json2_path, "r", encoding="utf-8") as f:
        data2 = json.load(f)

    # 保证两边都转成列表
    if isinstance(data1, dict):
        data1 = [data1]
    if isinstance(data2, dict):
        data2 = [data2]

    # 建立 json2 的 id → label 映射
    label_map = {item["id"]: item["label"] for item in data2 if "id" in item and "label" in item}

    # 筛选出 ground_truth != label 的对象
    mismatched = []
    for item in data1:
        meme_id = item.get("meme_id")
        gt = item.get("ground_truth")
        if meme_id in label_map and gt != label_map[meme_id]:
            mismatched.append(item)

    # 保存结果
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(mismatched, f, ensure_ascii=False, indent=4)

    print(f"筛选完成，共找到 {len(mismatched)} 条不一致数据，已保存到 {output_path}")


if __name__ == "__main__":
    filter_mismatched(r"C:\Users\scaaa\Downloads\MultiOff_visualized_gpt\MultiOff_visualized\all_symbol_evolver_errors.json", r"D:\python\SymbolEvolver\output\MultiOff\MultiOff_solver_output.json", r"C:\Users\scaaa\Downloads\MultiOff_visualized_gpt\MultiOff_visualized\all_symbol_evolver_errors3.json")
