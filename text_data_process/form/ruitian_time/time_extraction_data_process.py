import pandas as pd
import json
import re
import ast
import math
import argparse

def parse_time_cell(cell):
    """Parse a single cell like:
       '时间|近三年|['2020-07-11', '2023-07-11']'
       '截至时间|2023年10月|[ '2023-10-31']'
    """
    if cell is None or (isinstance(cell, float) and math.isnan(cell)):
        return None
    s = str(cell).strip()
    if not s:
        return None

    parts = s.split("|")
    if len(parts) < 3:
        return {"raw": s}

    tag = parts[0].strip()
    text = parts[1].strip()
    rng = "|".join(parts[2:]).strip()

    # Parse list-like string safely
    try:
        val = ast.literal_eval(rng)
    except Exception:
        rng2 = rng.replace("“", "'").replace("”", "'").replace("’", "'").replace("‘", "'")
        rng2 = re.sub(r"\bnull\b", "None", rng2, flags=re.I)
        try:
            val = ast.literal_eval(rng2)
        except Exception:
            val = None

    start = end = point = None
    if isinstance(val, list):
        if len(val) == 1:
            point = val[0] if val[0] != "" else None
        elif len(val) >= 2:
            start = val[0] if val[0] != "" else None
            end = val[1] if val[1] != "" else None
    elif isinstance(val, str):
        point = val if val != "" else None

    out = {"text": text, "tag": tag}
    if point is not None:
        out["type"] = "point"
        out["date"] = point
    else:
        out["type"] = "range"
        out["start"] = start
        out["end"] = end
    return out


INSTRUCTION = (
    "你是一个时间实体抽取与规范化助手。给定【当前日期】与【查询】文本，"
    "抽取查询中所有明确的时间表达（如“近三年”“截至2023年6月30日”“2021年上半年”“同期”等），"
    "并把每个时间表达规范化为 ISO 日期。输出必须是严格 JSON："
    "{\"time_entities\":[{\"text\":...,\"type\":\"range|point\",\"start\":...,\"end\":...}]}。"
    "type=point 时用字段 date；type=range 时用 start/end；未知起始用 null。"
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_csv", type=str, required=True)
    ap.add_argument("--output_jsonl", type=str, required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv)

    # Assume columns are: 0=query, 1=current_date, 2..=time entities
    col_query = df.columns[0]
    col_date = df.columns[1]
    entity_cols = list(df.columns[2:])

    with open(args.output_jsonl, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            query = str(row[col_query]).strip()
            cur_date = str(row[col_date]).strip()

            entities = []
            for c in entity_cols:
                ent = parse_time_cell(row[c])
                if ent:
                    entities.append(ent)

            output_obj = {"time_entities": entities}
            rec = {
                "instruction": INSTRUCTION,
                "input": f"当前日期: {cur_date}\n查询: {query}",
                "output": json.dumps(output_obj, ensure_ascii=False)
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Saved: {args.output_jsonl}  (records={len(df)})")

if __name__ == "__main__":
    main()