import pandas as pd


def xlsx_to_json(xlsx_path, json_path, sheet_name=0, columns=None, rename_map=None):
    """
    将 Excel 文件转换为 JSON 文件

    参数:
    - xlsx_path: str，Excel 文件路径
    - json_path: str，输出的 JSON 文件路径
    - sheet_name: int 或 str，可选，指定工作表，默认为第一个工作表
    - columns: list[str]，可选，指定要导出的列名
    - rename_map: dict，可选，键为原始列名，值为新列名
    """
    # 读取 Excel 文件
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)

    # 如果指定了列，就筛选这些列
    if columns:
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"❌ 以下列在表中未找到: {missing_cols}")
        df = df[columns]

    # 如果提供了重命名映射
    if rename_map:
        df = df.rename(columns=rename_map)

    # 转换为 JSON 并保存
    df.to_json(json_path, orient='records', force_ascii=False, indent=4)
    print(f"✅ 已成功将 {xlsx_path} 转换为 {json_path}")


def json_to_xlsx(json_path, xlsx_path):
    """
    将 JSON 文件转换为 Excel 文件 (.xlsx)

    参数:
    - json_path: str，输入的 JSON 文件路径
    - xlsx_path: str，输出的 Excel 文件路径
    """
    # 读取 JSON 文件
    df = pd.read_json(json_path)

    # 写入 Excel 文件
    df.to_excel(xlsx_path, index=False)
    print(f"✅ 已成功将 {json_path} 转换为 {xlsx_path}")


# ✅ 示例用法
# 例如原始 Excel 中有“内容”和“段索引”列，导出为 JSON 时重命名为 content 和 chunk_index
xlsx_to_json(
    r"D:\python\DataProcessTools\text_data_process\gileadkb_document_graphrag_sorted.xlsx",
    r"D:\python\DataProcessTools\text_data_process\gileadkb_document_graphrag_final.json",
    columns=["content", "chunk_index","file_id"],
)

# json_to_xlsx(
#     r"D:\output.json",
#     r"D:\output.xlsx"
# )
