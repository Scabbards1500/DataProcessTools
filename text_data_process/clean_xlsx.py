import pandas as pd

# 读取 Excel 文件
input_path = r'D:\python\FastAPI_study\gilead_test\data\gilead_ori_data.xlsx'  # ← 替换成你的文件名
df = pd.read_excel(input_path)

# 删除 Input_data 列为空的行
df_cleaned = df.dropna(subset=['Input_question'])
# 删除 重复的行
df_unique = df_cleaned.drop_duplicates(subset=['Input_question'], keep='first')

# 保存为新的 Excel 文件
output_path = r'D:\python\FastAPI_study\gilead_test\data\gilead_final_data.xlsx'
df_unique.to_excel(output_path, index=False)

print(f"已删除 Input_data 为空的行，结果保存为 {output_path}")
