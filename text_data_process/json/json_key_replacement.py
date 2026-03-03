import json
import os

def replace_key(obj, old_key, new_key):
    """
    递归地替换字典或列表中指定的key
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if k == old_key:
                k = new_key
            new_dict[k] = replace_key(v, old_key, new_key)
        return new_dict
    elif isinstance(obj, list):
        return [replace_key(item, old_key, new_key) for item in obj]
    else:
        return obj

def process_json_file(file_path, old_key="Premise", new_key="Translated Premise"):
    # 读取JSON文件
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 替换key
    updated_data = replace_key(data, old_key, new_key)

    # 保存回原文件（或写入新的文件）
    new_file_path = file_path.replace(".json", "_updated.json")
    with open(new_file_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)

    print(f"处理完成: {file_path} -> {new_file_path}")

if __name__ == "__main__":
    # 在这里输入你的 JSON 文件路径
    json_file_path = r"C:\Users\scaaa\Downloads\HarM_planner_output_updated_with_translator_imgs_updated.json"
    process_json_file(json_file_path)
