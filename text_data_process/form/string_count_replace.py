import pandas as pd

# 读取 CSV（统一转成字符串，避免 NaN/数字问题）
df = pd.read_csv(r"D:\python\DataProcessTools\text_data_process\form\filtered_output_contains_time.csv", dtype=str)

# 统计包含 "***" 的单元格数量
count = df.applymap(lambda x: "			" in x if isinstance(x, str) else False).sum().sum()

print(f'包含 "			" 的单元格数量: {count}')

# 替换 "***" 为 "%%%"
df = df.applymap(lambda x: x.replace("			", "") if isinstance(x, str) else x)

# 保存新文件
df.to_csv(r"D:\python\DataProcessTools\text_data_process\form\filtered_output_contains_time2.csv", index=False)
