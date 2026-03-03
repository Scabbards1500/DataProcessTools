import json
import argparse
from typing import List, Dict, Any


def chunks_to_markdown(chunks: List[Dict[str, Any]], output_file: str = None) -> str:
    """
    将 JSON chunks 还原为 Markdown 文本

    参数:
        chunks: list of dict, chunk 列表
        output_file: str, 可选，输出 Markdown 文件路径

    返回:
        markdown_text: str, Markdown 文本
    """
    if not chunks:
        return ""

    # 构建完整的层级路径（包含当前标题）
    def get_full_path(chunk: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取包含当前标题的完整路径"""
        full_path = []
        # 添加父级路径
        if chunk.get("section_path"):
            full_path.extend(chunk["section_path"])
        # 添加当前标题
        section_title = chunk.get("section_title", "")
        section_number = chunk.get("section_number", "")
        # 从 section_number 推断 level（通过点的数量）
        # 如果 section_number 为 "0"，则 level 为 0（表示无标题的开头内容）
        if section_number == "0":
            level = 0
        else:
            level = section_number.count(".") + 1 if section_number else 1
        
        # 只有 level > 0 的 chunk 才添加到路径中（level=0 表示无标题）
        if level > 0:
            full_path.append({
                "title": section_title,
                "number": section_number,
                "level": level
            })
        return full_path

    # 为每个 chunk 添加完整路径和 level 信息
    processed_chunks = []
    for chunk in chunks:
        full_path = get_full_path(chunk)
        # 获取当前 chunk 的 level
        section_number = chunk.get("section_number", "")
        if section_number == "0":
            current_level = 0
        else:
            current_level = full_path[-1]["level"] if full_path else 1
        processed_chunks.append({
            **chunk,
            "full_path": full_path,
            "level": current_level
        })

    # 按 section_number 排序（确保正确的顺序）
    def sort_key(chunk: Dict[str, Any]) -> tuple:
        """排序键：根据 section_number 的各个部分转换为整数元组"""
        number = chunk.get("section_number", "0")
        try:
            # 将 "0.1.2" 转换为 (0, 1, 2)
            parts = [int(x) for x in number.split(".") if x]
            # 填充到相同长度以便比较
            return tuple(parts)
        except (ValueError, AttributeError):
            return (0,)

    processed_chunks.sort(key=sort_key)

    # 生成 Markdown
    markdown_lines = []
    last_title = None  # 记录上一个 chunk 的标题

    for chunk in processed_chunks:
        content = chunk.get("content", "")
        current_level = chunk.get("level", 1)
        section_title = chunk.get("section_title", "")

        # 处理 level=0 的 chunk（文档开头无标题的内容）
        if current_level == 0:
            # level=0 的 chunk 不输出标题，直接输出内容
            actual_content = content.strip()
            if actual_content:
                markdown_lines.append(actual_content)
                markdown_lines.append("")  # 添加空行分隔
            # level=0 的 chunk 不影响 last_title
            continue

        # 只输出当前 chunk 的标题，不输出 section_path 中的父级标题
        # 检查是否需要输出标题（如果标题与上一个不同）
        if section_title and section_title != last_title:
            # 输出当前 chunk 的标题
            hashes = "#" * current_level
            markdown_lines.append(f"{hashes} {section_title}")

        # 处理内容
        # 去掉内容中的标题前缀（如果存在）
        title_prefix = f"{section_title}: "
        if content.startswith(title_prefix):
            actual_content = content[len(title_prefix):]
            # 只去掉开头的空白，保留其他格式（包括换行、特殊字符等）
            actual_content = actual_content.lstrip()
        else:
            actual_content = content

        # 如果内容不为空，添加到 Markdown（保留原始格式，包括换行和特殊字符）
        if actual_content.strip():
            # 直接添加内容，保留所有换行和特殊字符（如美元符号等）
            markdown_lines.append(actual_content)
            markdown_lines.append("")  # 添加空行分隔

        # 更新 last_title
        last_title = section_title

    # 合并为 Markdown 文本
    markdown_text = "\n".join(markdown_lines)

    # 输出到文件
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_text)
        print(f"Markdown 文件已保存到: {output_file}")

    return markdown_text


# ------------------------------
# 主函数
# ------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将 JSON chunks 还原为 Markdown")
    parser.add_argument("json_file", help="JSON 文件路径")
    parser.add_argument("--output", "-o", default=None, help="输出 Markdown 文件路径")
    args = parser.parse_args()

    # 读取 JSON 文件
    with open(args.json_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # 转换为 Markdown
    markdown_text = chunks_to_markdown(chunks, output_file=args.output)

    # 如果没有指定输出文件，打印到标准输出
    if not args.output:
        print(markdown_text)
