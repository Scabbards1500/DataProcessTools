import pandas as pd

# === 配置 ===
input_file = 'gileadkb_document_graphrag.xlsx'           # 原始 Excel 文件路径
output_file = 'filtered_gileadkb_document_graphrag.xlsx'          # 结果保存路径
target_column = 'file_id'                        # 要筛选的列名（请替换）
keyword = '1375a4d8dd454428a89abfd1cb21b15a'                            # 要匹配的关键字（模糊匹配）

# === 读取 Excel 文件 ===
df = pd.read_excel(input_file)

# === 筛选包含关键字的行（不区分大小写）===
filtered_df = df[df[target_column].astype(str).str.contains(keyword, case=False, na=False)]

# === 保存结果为新的 Excel 文件 ===
filtered_df.to_excel(output_file, index=False)

print(f"已成功将包含“{keyword}”的行保存到文件：{output_file}")
