import pandas as pd
from collections import defaultdict
# 实体统计
# ======================
# 1. 读取数据
# ======================

df = pd.read_csv(r"D:\python\DataProcessTools\text_data_process\form\raw_data_v22.csv")

FIXED_COLS = ["序号", "Query", "当前日期"]

entity_cols = [c for c in df.columns if c not in FIXED_COLS]

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


# ======================
# 3. 统计实体词表（排除时间）
# ======================

entity_dict = defaultdict(set)

for _, row in df.iterrows():
    for col in entity_cols:
        etype, etext = parse_entity(row[col])
        if not etype or not etext:
            continue

        if etype == "时间":
            continue

        entity_dict[etype].add(etext)

# 转成 list（方便展示 / JSON 化）
entity_dict = {k: sorted(list(v)) for k, v in entity_dict.items()}

# ======================
# 4. 展示结果
# ======================

for etype, entities in entity_dict.items():
    print(f"\n【{etype}】({len(entities)})")
    for e in entities:
        print(" -", e)
