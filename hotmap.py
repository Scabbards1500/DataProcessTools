import matplotlib.pyplot as plt
import numpy as np

# 模型名称
models = [
    'ChatGLM4-9B', 'Gemma-1.1-7B', 'Gemma-2-9B', 'Internlm2-7B',
    'Internlm2.5-7B', 'Llama-3-8B', 'MiniCPM-2B', 'Mistral-7B',
    'Phi3-small', 'Qwen1.5-14B', 'Qwen1.5-32B', 'Qwen2-7B',
    'Yi-1.5-9B', 'Yi-1.5-34B'
]

# 误导状态: 0=误导, 1=未误导
without_anti = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
with_anti = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# 设置柱状图宽度和位置
x = np.arange(len(models))
width = 0.35

# 创建图表
fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width/2, without_anti, width, label='Without Anti-misdirection')
rects2 = ax.bar(x + width/2, with_anti, width, label='With Anti-misdirection')

# 添加标签和标题
ax.set_ylabel('Misleading Status (0 = Mislead, 1 = Not Mislead)')
ax.set_title('Model Performance with and without Anti-misdirection Prompts')
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=45, ha="right")
ax.legend()

# 添加数值标签
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

plt.tight_layout()
plt.show()
