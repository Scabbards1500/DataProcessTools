import pandas as pd
# 筛选字符串

# 读取 Excel 文件
input_path = 'final_data_rewrite.xlsx'  # ← 替换为你的文件名
df = pd.read_excel(input_path)

# 删除 'rewritten_query' 为空的行，并清洗字符串
df = df[df['rewritten_query'].notna()]
df['rewritten_query'] = df['rewritten_query'].astype(str).str.strip()

# 条件筛选
mask_star = df['rewritten_query'].str.contains(r'\*\*', regex=True)
mask_answer = df['rewritten_query'].str.contains(r'\banswer\b', case=False, regex=True)

# 分别筛选
df_star = df[mask_star]
df_answer = df[mask_answer]

# 同时包含 "**" 和 "answer"
df_both = df[mask_star & mask_answer]

# 合并这两种条件（去重）
combined_indices = list(set(df_star.index).union(set(df_answer.index)))
df_special = df.loc[combined_indices]

# 普通数据（不包含 '**' 和 'answer' 的）
df_normal = df.drop(index=combined_indices)

# 保存文件
df_star.to_excel('contains_star.xlsx', index=False)
df_answer.to_excel('contains_answer.xlsx', index=False)
df_both.to_excel('contains_both.xlsx', index=False)
df_normal.to_excel('right.xlsx', index=False)

# 打印结果
print("处理完成：")
print(f"包含 '**' 的行保存为 contains_star.xlsx（共 {len(df_star)} 行）")
print(f"包含 'answer' 的行保存为 contains_answer.xlsx（共 {len(df_answer)} 行）")
print(f"同时包含 '**' 和 'answer' 的行保存为 contains_both.xlsx（共 {len(df_both)} 行）")
print(f"剩下的其他行保存为 right.xlsx（共 {len(df_normal)} 行）")
