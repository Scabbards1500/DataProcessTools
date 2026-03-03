import pandas as pd
import re

# --- 配置区 ---
input_csv = r"D:\python\DataProcessTools\text_data_process\form\raw_data_v22.csv"
output_csv = r"D:\python\DataProcessTools\text_data_process\form\raw_data_v23.csv"

# --- 读取实体列表 ---
def load_entities(file_path):
    entities = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                entities.append(line[2:])
    return entities

entities_dict = {
    "机构-公司": load_entities("机构-公司.txt"),
    "机构-政府": load_entities("机构-政府.txt"),
    "自然人": load_entities("自然人.txt"),
    "机构-其他": load_entities("机构-其他.txt"),
    "机构-代码": load_entities("机构-代码.txt")
}

# --- 读取 CSV ---
df = pd.read_csv(input_csv)

# 找到所有实体列
entity_cols = [col for col in df.columns if col.startswith("实体")]

# --- 遍历每行，插入缺失实体备注 ---
rows_to_insert = []

for idx, row in df.iterrows():
    # 收集这一行已经存在的实体（取 "|" 后面的部分）
    extracted_entities = []
    for col in entity_cols:
        val = row.get(col)
        if pd.notna(val):
            if "|" in str(val):
                extracted_entities.append(val.split("|")[1].strip())
            else:
                extracted_entities.append(str(val).strip())

    # 获取 query 文本
    query_text = str(row.get("Query", ""))

    # 检查每类缺失实体
    for ent_type, ent_list in entities_dict.items():
        missing_in_row = []

        for ent in ent_list:
            # 如果实体在 query 中出现最长匹配，则选择 query 中的实体
            pattern = re.escape(ent)
            matches = re.findall(pattern, query_text)
            if matches:
                match_entity = max(matches, key=len)  # 取最长匹配
                if match_entity not in extracted_entities and match_entity not in missing_in_row:
                    missing_in_row.append(match_entity)
            else:
                # 如果实体未在 query 中出现，但也不在已有实体里，则插入原实体
                if ent not in extracted_entities and ent not in missing_in_row:
                    missing_in_row.append(ent)

        if missing_in_row:
            # 构建备注行
            remark_row = {col: "" for col in df.columns}
            remark_text = f"【{ent_type}】({len(missing_in_row)})\n" + "\n".join(f" - {c}" for c in missing_in_row)
            remark_row["Query"] = remark_text
            rows_to_insert.append((idx, remark_row))

# --- 按行号插入备注 ---
for offset, (idx, remark_row) in enumerate(rows_to_insert):
    df_part1 = df.iloc[:idx + offset]
    df_part2 = df.iloc[idx + offset:]
    df = pd.concat([df_part1, pd.DataFrame([remark_row]), df_part2], ignore_index=True)

# --- 保存 ---
df.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"处理完成，输出保存到 {output_csv}")
