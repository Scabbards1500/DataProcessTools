import pandas as pd


def xlsx_to_json(xlsx_path, json_path, sheet_name=0):
    """
    将 Excel 文件转换为 JSON 文件

    参数:
    - xlsx_path: str，Excel 文件路径
    - json_path: str，输出的 JSON 文件路径
    - sheet_name: int 或 str，可选，指定工作表，默认为第一个工作表
    """
    # 读取 Excel 文件
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)

    # 转换为 JSON 并保存
    df.to_json(json_path, orient='records', force_ascii=False, indent=4)
    print(f"已成功将 {xlsx_path} 转换为 {json_path}")


# 示例用法
xlsx_to_json("example.xlsx", "output.json")
