import pandas as pd
import re


def filter_by_keywords(
    input_path,
    keep_keywords,
    column_name=None,   # 默认 None = 所有列
    case_sensitive=False,
    output_prefix="output"
):
    """
    根据关键词筛选 Excel 中的行

    Args:
        input_path (str): 输入 Excel 文件路径
        keep_keywords (list[str]): 需要保留的字符串列表
        column_name (str or None): 指定列名；None 表示所有列
        case_sensitive (bool): 是否区分大小写
        output_prefix (str): 输出文件名前缀
    """

    df = pd.read_excel(input_path)

    flags = 0 if case_sensitive else re.IGNORECASE

    # 选择要筛选的列
    if column_name:
        if column_name not in df.columns:
            raise ValueError(f"列名 {column_name} 不存在")
        target_df = df[[column_name]].copy()
    else:
        target_df = df.copy()

    # 转成字符串并去除空值
    target_df = target_df.fillna("").astype(str)

    pattern_dict = {}

    for kw in keep_keywords:
        # 对每一列做 contains，然后按行做 any
        mask = target_df.apply(
            lambda col: col.str.contains(re.escape(kw), flags=flags, regex=True)
        ).any(axis=1)

        pattern_dict[kw] = mask

    selected_indices = set()

    # 每个关键词单独保存
    for kw, mask in pattern_dict.items():
        df_kw = df[mask]
        df_kw.to_csv(f"{output_prefix}_contains_time.csv", index=False)
        selected_indices.update(df_kw.index)
        print(f"包含 '{kw}' 的行: {len(df_kw)}")

    # # 同时包含所有关键词
    # if len(keep_keywords) > 1:
    #     combined_mask = pd.Series(True, index=df.index)
    #     for mask in pattern_dict.values():
    #         combined_mask &= mask
    #
    #     df_all = df[combined_mask]
    #     df_all.to_excel(f"{output_prefix}_contains_all.xlsx", index=False)
    #     print(f"同时包含所有关键词的行: {len(df_all)}")


    print("处理完成！")

import pandas as pd
import re
from pathlib import Path


import pandas as pd
import re
from pathlib import Path


def keep_keywords_only(
    input_path,
    keep_column_indices,
    keywords,
    case_sensitive=False,
    delete_blank=True,
    output_path=None
):
    """
    保留指定列 + 其他列中包含关键词的单元格，其余清空
    可选：删除空单元格并整体左移

    Args:
        input_path (str): 输入 csv/xlsx 文件
        keep_column_indices (list[int]): 需要完整保留的列索引（从0开始）
        keywords (list[str]): 关键词列表
        case_sensitive (bool): 是否区分大小写
        delete_blank (bool): 是否删除空单元格并左移
        output_path (str): 输出文件路径
    """

    # 读取文件
    suffix = Path(input_path).suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(input_path)
    elif suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(input_path)
    else:
        raise ValueError("只支持 csv / xlsx 文件")

    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = "|".join(re.escape(k) for k in keywords)

    max_col = df.shape[1] - 1
    for idx in keep_column_indices:
        if idx > max_col:
            raise ValueError(f"列索引 {idx} 超出范围 (最大为 {max_col})")

    # 先做关键词过滤
    for col_idx in range(df.shape[1]):
        if col_idx in keep_column_indices:
            continue

        col = df.iloc[:, col_idx]
        mask = col.astype(str).str.contains(pattern, flags=flags, regex=True, na=False)
        df.iloc[~mask, col_idx] = ""

    # 如果需要删除空格并左移
    if delete_blank:
        def shift_left(row):
            non_empty = [x for x in row if str(x).strip() != "" and pd.notna(x)]
            return pd.Series(non_empty + [""] * (len(row) - len(non_empty)))

        df = df.apply(shift_left, axis=1)

    # 输出路径
    if not output_path:
        output_path = f"filtered_{Path(input_path).name}"

    if suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        df.to_excel(output_path, index=False)

    print(f"处理完成，已保存到: {output_path}")


filter_by_keywords(
    input_path=r"D:\python\DataProcessTools\text_data_process\form\ruitian_time\generated_time_queries.xlsx",
    keep_keywords=["时间|"],
    case_sensitive=True
)

keep_keywords_only(
    input_path=r"D:\python\DataProcessTools\text_data_process\form\output_contains_time.csv",
    keep_column_indices=[0,1],
    keywords=["时间|"]
)
