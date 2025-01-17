import pandas as pd

# 读取CSV文件
file_path = r"C:\Users\scaaa\Downloads\CPT_mismatched.csv"  # 替换为你的文件路径
df = pd.read_csv(file_path)

# 定义一个函数来提取F1分数

# extract = 'F1 score:'
# extract = 'Mismatch percentage: '
extract = 'Precision score:'


def extract_f1_score(text):
    if pd.isna(text) or extract not in text:
        return None
    # 提取F1分数部分
    f1_line = [line for line in text.split('\n') if extract in line]
    if f1_line:
        # return float(f1_line[0].split(':')[1].strip())
        return (f1_line[0].split(':')[1].strip())
    return None

# 只保留F1分数数据
f1_data = df.copy()

# 提取每个列中的F1分数
for column in ['Zero-shot', 'One-shot', 'Few-shot', 'Dynamic']:
    f1_data[column] = df[column].apply(extract_f1_score)

# 打印结果
print(f1_data)
output_path = 'F1_2.csv'  # 你可以在这里指定保存路径和文件名
f1_data.to_csv(output_path, index=False)
