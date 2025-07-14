import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Data for simulate_capacity
mu = 0.6
sigma = 0.1


def simulate_capacity(mu_SC = 0.6, sigma_SC = 0.1):
    """
    Simulates the capacity of a system using a Gaussian distribution.
    The function generates a random number from a Gaussian distribution with mean `mu` and standard deviation `sigma`.
    The generated number is constrained to be between 0 and 1 (exclusive).
    """
    random_number = 1
    while (random_number >= 1 or random_number <= 0):
        random_number = random.gauss(mu_SC, sigma_SC)
    return random_number

data_examples = [simulate_capacity(mu, sigma) for _ in range(100)]



# Set the style for the plots
plt.style.use('seaborn-v0_8-whitegrid')

# theoretical graphtheo
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
y = norm.pdf(x, mu, sigma) * 100 * 0.1

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(12, 7), dpi=100)

bins = np.arange(0.0, 1.1, 0.1)  # 创建0.0到1.0的区间，步长为0.1
n, bins, patches = ax.hist(data_examples, bins = bins, color='#1f77b4', alpha=0.8, 
                           edgecolor='white', linewidth=1.2, zorder=5)

# Plot the theoretical Gaussian distribution
for i in range(len(patches)):
    x_pos = patches[i].get_x() + patches[i].get_width() / 2
    y_pos = patches[i].get_height() + 0.5
    if n[i] > 0:
        ax.text(x_pos, y_pos, f'{int(n[i])}', ha='center', fontsize=10, 
                fontweight='bold', color='#2c3e50')
        
ax.plot(x, y, 'r-', linewidth=2.5, label='Theoretical curve')

# 添加均值和标准差标记
ax.axvline(mu, color='#e74c3c', linestyle='--', linewidth=2, 
           label=f'mean values ($\\mu$ = {mu})')
ax.axvline(mu + sigma, color='#3498db', linestyle=':', linewidth=1.8, 
           label=f'standard deviation ($\\sigma$ = {sigma})')

# 填充均值±标准差的区域
ax.fill_between(x, 0, y, where=(x >= mu-sigma) & (x <= mu+sigma), 
                color='#3498db', alpha=0.15)

# 添加说明文本
stats_text = (f'sample size: {len(data_examples)}\n'
              f'sample average: {np.mean(data_examples):.3f}\n'
              f'sample standard deviation: {np.std(data_examples):.3f}')

ax.text(0.02, 0.8, stats_text, transform=ax.transAxes, 
        fontsize=12, verticalalignment='top', 
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 设置图表标题和标签
ax.set_title('Capability Distribution Chart (μ=0.6, σ=0.1)', fontsize=16, pad=20)
ax.set_xlabel('Numeric range', fontsize=13)
ax.set_ylabel('frequency', fontsize=13)

# 设置坐标轴范围
ax.set_xlim(0.2, 1.0)
ax.set_ylim(0, max(n)*1.25)

# 添加网格和图例
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper left', fontsize=12)

# 添加底部信息
fig.text(0.5, 0.01, 'Capability Distribution Chart', 
         ha='center', fontsize=10, color='#7f8c8d')

# 使用紧凑布局
plt.tight_layout()
plt.subplots_adjust(bottom=0.1)

# 显示图表
plt.show()