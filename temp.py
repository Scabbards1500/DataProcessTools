import json

import json

def filter_related_imgs(input_file, output_file, keep_n):
    # 读取原始 JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 如果是单个对象，包装成列表方便统一处理
    if isinstance(data, dict):
        data = [data]

    for item in data:
        premise = item.get("Translated Premise", {})
        related_imgs = {k: v for k, v in premise.items() if k.startswith("related_img")}

        # 按数字顺序排序
        sorted_related = dict(sorted(
            related_imgs.items(),
            key=lambda x: int(x[0].replace("related_img", ""))
        ))

        # 截取前 keep_n 个
        filtered_related = dict(list(sorted_related.items())[:keep_n])

        # 删除原来的 related_img
        for key in list(premise.keys()):
            if key.startswith("related_img"):
                premise.pop(key)

        # 添加回去
        premise.update(filtered_related)

    # 写出新的 JSON
    with open(output_file, "w", encoding="utf-8") as f:
        # 如果原来是单个对象，就只保存第一个
        if len(data) == 1:
            json.dump(data[0], f, ensure_ascii=False, indent=4)
        else:
            json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"生成完成，新文件保存到 {output_file}")



if __name__ == "__main__":
    # 输入文件路径
    input_path = r"D:\tempdataset\Memes\result\ablation_study\num of imgs\HarM_planner_output10.json"
    # 输出文件路径
    output_path = r"D:\tempdataset\Memes\result\ablation_study\num of imgs\HarM_planner_output9.json"
    # 保留的 related_img 数量
    keep_number = 9

    filter_related_imgs(input_path, output_path, keep_number)
