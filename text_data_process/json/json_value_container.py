import json

# 输入文件
txt_file = r"D:\python\SymbolEvolver\utils\removed_ids.txt"       # 你存放 img/...png 的txt
json_file = "D:\python\SymbolEvolver\output\FHM\FHM_translator_output.json"     # 原始大json
out_file = "D:\python\SymbolEvolver\output\FHM\FHM_translator_output2.json"  # 输出筛选后的结果

# 读取txt里的所有文件名
with open(txt_file, "r", encoding="utf-8") as f:
    keep_imgs = set(line.strip() for line in f if line.strip())

# 读取json（假设是一个list，每个元素是dict）
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 筛选
filtered = [obj for obj in data if obj.get("img") in keep_imgs]

# 保存
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(f"筛选完成！共 {len(filtered)} 条，已保存到 {out_file}")
