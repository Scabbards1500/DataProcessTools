import json
import uuid
import re
import argparse

def markdown_to_chunks(markdown_text, doc_id="doc", max_level=6, output_file=None):
    """
    将 Markdown 文本拆分成 hierarchical chunk JSON

    参数:
        markdown_text: str, Markdown 文本
        doc_id: str, 文档ID
        max_level: int, 最大拆分标题级别，超过该级别的标题不会生成新的chunk，会合并到上级
        output_file: str, 可选，输出 JSON 文件路径

    返回:
        chunks: list of dict
    """
    lines = markdown_text.split("\n")
    chunks = []
    section_stack = []  # 当前标题栈 [{"title":..., "number":...}]
    counters = {}  # 每个级别计数
    current_content = []

    def flush_chunk():
        # 处理文档开头没有标题的文本（section_stack 为空）
        if not section_stack:
            # 只有有内容时才创建 chunk
            if not current_content:
                return
            chunk_id = str(uuid.uuid4())
            # 保留原始格式，用换行符连接
            content_text = "\n".join(current_content).strip()
            chunk = {
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "section_path": [],
                "section_title": "",  # 空标题
                "section_number": "0",  # 编号为 0
                "content": content_text,
                "level": 0  # level 为 0 表示没有标题
            }
            chunks.append(chunk)
            return
        
        # 即使 current_content 为空，只要有 section_stack，也要创建 chunk
        # 这样可以处理两个标题连在一起的情况
        # 注意：超过 max_level 的标题已经在主循环中作为内容处理，不会到达这里
        
        section_number = section_stack[-1]["number"]
        section_title = section_stack[-1]["title"]
        # section_path 不包含当前 chunk，只包含父级路径
        section_path = section_stack[:-1]
        chunk_level = section_stack[-1]["level"]

        chunk_id = str(uuid.uuid4())
        # 保留原始格式，用换行符连接，而不是空格
        # 即使 current_content 为空，也要创建 chunk（标题本身作为内容）
        if current_content:
            content_text = f"{section_title}: " + "\n".join(current_content).strip()
        else:
            # 如果内容为空，只保留标题（用于处理两个标题连在一起的情况）
            content_text = f"{section_title}: "
        
        chunk = {
            "chunk_id": chunk_id,
            "doc_id": doc_id,
            "section_path": section_path,
            "section_title": section_title,
            "section_number": section_number,
            "content": content_text,
            "level": chunk_level  # 添加 level 用于去重判断
        }
        chunks.append(chunk)

    heading_pattern = re.compile(r"^(#{1,6})\s+(.*)")

    for line in lines:
        # 保留原始行（包括空行和空白），用于匹配标题
        stripped_line = line.strip()
        
        # 空行也要保留，用于分隔段落
        if not stripped_line:
            current_content.append("")
            continue

        match = heading_pattern.match(stripped_line)
        if match:
            hashes, title = match.groups()
            level = len(hashes)

            # 如果标题级别超过 max_level，将其作为内容添加到当前 chunk，而不是创建新 chunk
            if level > max_level:
                # 将标题作为内容添加到当前 chunk（保留原始格式）
                current_content.append(line)
                # 更新 counters（用于可能的编号生成，但不创建新 chunk）
                counters[level] = counters.get(level, 0) + 1
                for l in range(level + 1, 7):
                    counters[l] = 0
                # 注意：超过 max_level 的标题不更新 section_stack，因为不会用于创建 chunk
            else:
                # 标题级别 <= max_level，正常处理：flush previous chunk 并创建新 chunk
                flush_chunk()
                current_content = []

                # 更新 counters
                counters[level] = counters.get(level, 0) + 1
                # 重置低级别计数
                for l in range(level + 1, 7):
                    counters[l] = 0

                # 生成编号（确保所有级别都有计数器，缺失的默认为0）
                number = ".".join(str(counters.get(l, 0)) for l in range(1, level + 1))

                # 更新 section_stack
                section_stack = section_stack[:level - 1]
                section_stack.append({"title": title, "number": number, "level": level})

        else:
            # 普通段落 / 列表 / 表格行（保留原始格式，包括空白和特殊字符）
            current_content.append(line)

    # flush last chunk
    flush_chunk()

    # 去重：合并相邻的同层级、同标题的 chunk，并清理 section_path 中的重复项
    if chunks:
        deduplicated_chunks = []
        i = 0
        while i < len(chunks):
            current_chunk = chunks[i]
            
            # 清理 section_path 中的重复项：每个层级只保留最后一个条目
            if current_chunk.get("section_path"):
                cleaned_path = []
                level_to_item = {}  # {level: item} 记录每个层级的最新条目
                for path_item in current_chunk["section_path"]:
                    path_level = path_item.get("level", 0)
                    # 每个层级只保留最后一个条目（覆盖之前的）
                    level_to_item[path_level] = path_item
                # 按 level 顺序重新构建 path
                if level_to_item:
                    max_level = max(level_to_item.keys())
                    cleaned_path = [level_to_item.get(l) for l in range(1, max_level + 1) if l in level_to_item]
                current_chunk["section_path"] = cleaned_path
            
            # 检查后续相邻的 chunk 是否需要合并到当前 chunk
            j = i + 1
            while j < len(chunks):
                next_chunk = chunks[j]
                
                # 判断是否需要合并：同层级、同标题
                if (current_chunk["level"] == next_chunk["level"] and
                    current_chunk["section_title"] == next_chunk["section_title"]):
                    # 合并内容：将下一个 chunk 的内容追加到当前 chunk
                    current_content = current_chunk["content"]
                    next_content = next_chunk["content"]
                    
                    # 对于 level=0 的 chunk（无标题），直接使用内容，不需要处理标题前缀
                    if current_chunk["level"] == 0:
                        next_actual_content = next_content.strip()
                    else:
                        # 去掉下一个 chunk 的标题前缀（如果存在）
                        next_title_prefix = f"{next_chunk['section_title']}: "
                        if next_content.startswith(next_title_prefix):
                            next_actual_content = next_content[len(next_title_prefix):].strip()
                        else:
                            next_actual_content = next_content.strip()
                    
                    # 如果下一个 chunk 有实际内容，追加到当前 chunk（用换行符连接，保留格式）
                    if next_actual_content:
                        current_chunk["content"] = current_content + "\n" + next_actual_content
                    
                    # 跳过下一个 chunk，继续检查
                    j += 1
                else:
                    # 不需要合并，跳出循环
                    break
            
            # 添加合并后的 chunk
            deduplicated_chunks.append(current_chunk)
            i = j
        
        chunks = deduplicated_chunks
        # 移除临时添加的 level 字段
        for chunk in chunks:
            chunk.pop("level", None)

    # 输出 JSON 文件
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

    return chunks


# ------------------------------
# 主函数，支持文件输入和自定义拆分级别
# ------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Markdown 拆分 chunk 并输出 JSON")
    parser.add_argument("md_file", help="Markdown 文件路径")
    parser.add_argument("--doc_id", default="doc", help="文档ID")
    parser.add_argument("--max_level", type=int, default=6, help="最大拆分标题级别")
    parser.add_argument("--output", default=None, help="输出 JSON 文件路径")
    args = parser.parse_args()

    with open(args.md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    chunks = markdown_to_chunks(md_text, doc_id=args.doc_id, max_level=args.max_level, output_file=args.output)

    if not args.output:
        print(json.dumps(chunks, indent=2, ensure_ascii=False))
