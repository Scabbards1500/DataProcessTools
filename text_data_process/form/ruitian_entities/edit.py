import pandas as pd

df = pd.read_csv("replaced_new.csv")

# 第一列减 11
df.iloc[:, 0] = df.iloc[:, 0] - 11

# 老 pandas 用 lineterminator
csv_str = df.to_csv(index=False, lineterminator="\n")

with open("output_with_empty_lines.csv", "w", encoding="utf-8", newline="") as f:
    f.write("\n" * 8287)
    f.write(csv_str)
