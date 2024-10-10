import re
import matplotlib.pyplot as plt

# 读取文件内容
with open('output.txt', 'r') as file:
    data = file.read()

# 正则表达式匹配模式
pattern = re.compile(r'Epoch (\d+) / Iteration (\d+), before phase two:\s+'
            r'AUC: ([0-9.eE+-]+), EER: ([0-9.eE+-]+), EER_thr: ([0-9.eE+-]+), F1_score: ([0-9.eE+-]+)\s+'
            r'After phase two:\s+'
            r'AUC: ([0-9.eE+-]+), EER: ([0-9.eE+-]+), EER_thr: ([0-9.eE+-]+), F1_score: ([0-9.eE+-]+)')
# 解析数据
results = {}
for match in pattern.findall(data):
    epoch, iteration = int(match[0]), int(match[1])
    before_values = list(map(float, match[2:6]))
    after_values = list(map(float, match[6:10]))

    if epoch not in results:
        results[epoch] = {'iterations': [], 'before': [], 'after': []}

    results[epoch]['iterations'].append(iteration)
    results[epoch]['before'].append(before_values)
    results[epoch]['after'].append(after_values)

# 绘制每个 epoch 的 2×2 图表
metrics = ['AUC', 'EER', 'EER_thr', 'F1_score']
colors = ['b', 'g']

for epoch, epoch_data in results.items():
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
    fig.suptitle(f'Epoch {epoch} - Metrics per Iteration')

    for i, metric in enumerate(metrics):
        ax = axes[i // 2, i % 2]
        ax.set_title(metric)
        ax.set_xlabel('Iteration')
        ax.set_ylabel(metric)

        iterations = epoch_data['iterations']
        before_values = [values[i] for values in epoch_data['before']]
        after_values = [values[i] for values in epoch_data['after']]
    
        ax.plot(iterations, before_values, label='Before Phase Two', color=colors[0])
        ax.plot(iterations, after_values, label='After Phase Two', color=colors[1])

        ax.legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f'Epoch_{epoch}_metrics.png')
    plt.close()
    #plt.show()

# 计算并绘制每个 epoch 的平均 metrics
avg_metrics = {metric: {'before': [], 'after': []} for metric in metrics}

for epoch, epoch_data in results.items():
    # 计算平均值
    before_avg = [sum(values) / len(values) for values in zip(*epoch_data['before'])]
    after_avg = [sum(values) / len(values) for values in zip(*epoch_data['after'])]

    for j, metric in enumerate(metrics):
        avg_metrics[metric]['before'].append(before_avg[j])
        avg_metrics[metric]['after'].append(after_avg[j])

# 绘制每个 epoch 的平均值
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
fig.suptitle('Average Metrics per Epoch')

x = list(results.keys())
for i, metric in enumerate(metrics):
    ax = axes[i // 2, i % 2]
    ax.set_title(metric)
    ax.set_xlabel('Epoch')
    ax.set_ylabel(metric)

    ax.plot(x, avg_metrics[metric]['before'], label='Before Phase Two', marker='o')
    ax.plot(x, avg_metrics[metric]['after'], label='After Phase Two', marker='x')

    ax.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Average_Metrics_per_Epoch.png')
#plt.show()
plt.close()