import pandas as pd
import re
# 去除不存在实体
# ======================
# 1. 配置
# ======================

CSV_PATH = r"D:\python\DataProcessTools\text_data_process\form\raw_data_v2.csv"
OUTPUT_PATH = r"D:\python\DataProcessTools\text_data_process\form\raw_data_v21.csv"

FIXED_COLS = ["序号", "Query", "当前日期"]

# ======================
# 2. 工具函数
# ======================

def parse_entity(cell):
    """
    解析实体单元格
    return (entity_type, entity_text)
    """
    if pd.isna(cell):
        return None, None

    parts = str(cell).split("|")
    if len(parts) < 2:
        return None, None

    return parts[0].strip(), parts[1].strip()


def entity_in_query(entity_text, query):
    """
    判断实体内容是否真的出现在 query 中
    使用 re.escape 防止正则误伤
    """
    pattern = re.escape(entity_text)
    return re.search(pattern, query) is not None


# ======================
# 3. 主逻辑
# ======================

df = pd.read_csv(CSV_PATH)

entity_cols = [c for c in df.columns if c not in FIXED_COLS]

not_exist_col = []

for _, row in df.iterrows():
    query = str(row["Query"])
    not_exist_entities = []

    for col in entity_cols:
        etype, etext = parse_entity(row[col])
        if not etype or not etext:
            continue

        if not entity_in_query(etext, query):
            not_exist_entities.append(f"{etype}: {etext}")

    # 多个用分号分隔
    not_exist_col.append("；".join(not_exist_entities))

# ======================
# 4. 写回 CSV
# ======================

df.insert(0, "实体不存在", not_exist_col)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")


