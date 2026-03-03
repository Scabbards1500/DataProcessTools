import re
import argparse
from collections import defaultdict

class SectionNode:
    def __init__(self, title, level):
        self.title = title
        self.level = level
        self.content_words = 0  # 该标题下自身正文字数
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def total_words(self):
        """递归计算自身 + 所有子节点的字数"""
        total = self.content_words
        for c in self.children:
            total += c.total_words()
        return total

    def collect_by_level(self, level_dict):
        """把每级标题的总字数累积到 level_dict"""
        if self.level not in level_dict:
            level_dict[self.level] = []
        level_dict[self.level].append(self.total_words())
        for c in self.children:
            c.collect_by_level(level_dict)


def parse_markdown_to_tree(md_text):
    lines = md_text.split("\n")
    heading_pattern = re.compile(r"^(#{1,6})\s+(.*)")

    root = SectionNode("root", 0)
    stack = [root]  # 栈维护当前层级节点
    current_content = []

    def flush_content_to_node(node, content_lines):
        text = " ".join(content_lines).strip()
        word_count = len(text.split())
        node.content_words += word_count

    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = heading_pattern.match(line)
        if match:
            # flush current content
            flush_content_to_node(stack[-1], current_content)
            current_content = []

            hashes, title = match.groups()
            level = len(hashes)

            # 弹出比当前 level >= 的节点
            while stack and stack[-1].level >= level:
                stack.pop()

            node = SectionNode(title, level)
            stack[-1].add_child(node)
            stack.append(node)
        else:
            current_content.append(line)

    # flush最后一段
    flush_content_to_node(stack[-1], current_content)
    return root

def compute_avg_words_by_level(md_text):
    root = parse_markdown_to_tree(md_text)
    level_dict = {}
    root.collect_by_level(level_dict)

    avg_words_per_level = {}
    for level, counts in level_dict.items():
        avg_words_per_level[level] = sum(counts) / len(counts) if counts else 0
    return avg_words_per_level


# ------------------------------
# 主函数
# ------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="统计 Markdown 每级标题累计平均字数（包含子节点）")
    parser.add_argument("md_file", help="Markdown 文件路径")
    args = parser.parse_args()

    with open(args.md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    avg_words = compute_avg_words_by_level(md_text)
    print("每级标题平均字数（包含子节点）统计结果：")
    for level in sorted(avg_words.keys()):
        print(f"Level {level} average words: {avg_words[level]:.1f}")
