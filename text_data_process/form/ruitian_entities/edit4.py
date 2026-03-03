# 去除不需要实体
import re
import pandas as pd

# 你的 CSV 文件
csv_file = "raw_data_v21.csv"
df = pd.read_csv(csv_file)

# 列出所有不要的公司关键字（之前整理好的内容）
remove_keywords = [
    r"\（沃尔玛公司",
    r"\）有哪些董事会成员曾在国际知名咨询公司",
    r"\）有哪些董事会成员曾经在国际知名咨询公司",
    r"2023年1月至2023年12月31日期间公告股份",
    r"2024年11月至12月31日期间埃克森美孚公司",
    r"2024年股份",
    r"A股上市公司",
    r"A股厨房小电器公司",
    r"Company（美国工商五金公司",
    r"Corporation（英伟达公司",
    r"Corporation）截至2021年6月30日累计公司",
    r"International（沃尔玛公司",
    r"\['Thermo Fisher Scientific'\]企业",
    r"全A股上市公司",
    r"全市场公司",
    r"以及自该公告发布后6个月内岱美股份",
    r"以及这些独立董事在除公司",
    r"以反映公司",
    r"是否发布过变更股份",
    r"截止九阳股份有限公司",
    r"截止北京光环新网科技股份有限公司",
    r"所有上市公司",
    r"该公告发布后三个月内公司",
    r"请说明这些高管所持股份",
    r"用于分析公司",
    r"商业金属公司",
    r"简历及其除本公司",
    r"曾经有哪些除了公司",
    r"曾经有哪些除了物产中大集团股份有限公司",
    r"包括公司",
    r"包括其除本公司",
    r"除在公司",
    r"Limited（富途控股有限公司",
    r"Ltd（航天控股公司",
    r"N）是否有追加股份",
    "2023年1月1日至2023年12月31日期间公告股份",
    "2024年11月1日至12月31日期间埃克森美孚公司",
    "输出公司",
    "增发计划发布后一周内公司",
    "以反映公司",
    "其在除本公司",
    "收到全资子公司",
    "历年公司",
    "监事和高级管理人员名单及其在除本公司",
    "美股及其他海外上市公司",
    "美股等海外上市公司",
    "上述公司"
]

# 拼接正则模式
pattern = "|".join(remove_keywords)

# 对“实体”列进行清理
def clean_entities(value):
    if pd.isna(value):
        return value
    # 如果匹配到不需要的实体就清空
    if re.search(pattern, value):
        return ""
    return value

# 假设你的“实体”列名是 '实体' 或多个实体列
entity_cols = [col for col in df.columns if "实体" in col]

for col in entity_cols:
    df[col] = df[col].apply(clean_entities)

# 保存清理后的 CSV
df.to_csv("raw_data_v22.csv", index=False)
