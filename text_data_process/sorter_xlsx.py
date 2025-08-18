import pandas as pd


def sort_excel_by_columns(xlsx_path: str, output_path: str, sort_columns: list[str], ascending: bool = True):
    """
    按指定列顺序对Excel文件进行排序

    参数:
    - xlsx_path: 输入的 Excel 文件路径
    - output_path: 排序后的输出文件路径
    - sort_columns: 要排序的列名列表，按优先级顺序排列
    - ascending: 是否升序排序（默认升序），可以传入 True 或 False
    """
    # 读取Excel文件
    df = pd.read_excel(xlsx_path)

    # 检查列是否存在
    missing = [col for col in sort_columns if col not in df.columns]
    if missing:
        raise ValueError(f"这些列在文件中未找到: {missing}")

    # 执行排序
    df_sorted = df.sort_values(by=sort_columns, ascending=ascending)

    # 保存为新文件
    df_sorted.to_excel(output_path, index=False)
    print(f"✅ 排序完成，保存到: {output_path}")


sort_columns = ["file_id", "chunk_index"]
sort_excel_by_columns(r"D:\python\DataProcessTools\text_data_process\gileadkb_document_graphrag.xlsx", r"D:\python\DataProcessTools\text_data_process\gileadkb_document_graphrag_sorted.xlsx", sort_columns)
