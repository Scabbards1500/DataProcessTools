import pandas as pd

# === 设置文件路径 ===
input_file = "filtered_gileadkb_document_graphrag2.xlsx"        # 替换为你的 Excel 文件路径
output_file = "filtered_gileadkb_document_graphrag2.txt"           # 输出的 TXT 文件名

# === 读取 Excel 文件 ===
try:
    df = pd.read_excel(input_file)
    print(f"✅ 成功读取文件：{input_file}")
except Exception as e:
    print(f"❌ 读取 Excel 失败：{e}")
    exit(1)

# === 写入 TXT 文件 ===
try:
    # 使用 UTF-8-SIG 编码防止中文乱码，列用 tab 分隔，不保留索引
    df.to_csv(output_file, sep='\t', index=False, encoding='utf-8-sig')
    print(f"✅ 成功转换为 TXT 文件：{output_file}")
except Exception as e:
    print(f"❌ 写入 TXT 文件失败：{e}")
