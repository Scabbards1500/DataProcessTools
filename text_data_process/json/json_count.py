import json

def count_json_objects(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        count = len(data)  # 如果最外层是数组，计算元素个数
    elif isinstance(data, dict):
        count = 1  # 如果最外层是对象，只算 1 个
    else:
        raise ValueError("JSON 格式不符合预期，只支持最外层为 list 或 dict")

    print(f"{json_path} 中 JSON object 的数量为: {count}")
    return count


if __name__ == "__main__":
    count_json_objects("D:\python\SymbolEvolver\output\HarM\HarM_parsered.json")
