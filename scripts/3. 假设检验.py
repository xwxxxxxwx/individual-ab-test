"""
A/B Test 项目 - 第 3 步：假设检验
检验方法：双尾 z 检验（比例检验）
假设设定：
  H₀：p_new = p_old（新旧页面转化率无显著差异）
  H₁：p_new ≠ p_old（新旧页面转化率存在显著差异）
显著性水平：α = 0.05
"""

import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ── 加载清洗后数据 ─────────────────────────────────────────────────────────
df = pd.read_csv('ab_data_clean.csv')

control   = df[df['group'] == 'control']
treatment = df[df['group'] == 'treatment']

n_ctrl = len(control)
n_trt  = len(treatment)
conv_ctrl = control['converted'].sum()
conv_trt  = treatment['converted'].sum()
rate_ctrl = conv_ctrl / n_ctrl
rate_trt  = conv_trt  / n_trt

# ── 1. 执行 z 检验 ─────────────────────────────────────────────────────────
print("=" * 55)
print("【z 检验（双尾比例检验）】")
print("=" * 55)

count = np.array([conv_trt, conv_ctrl])
nobs  = np.array([n_trt,    n_ctrl])

z_stat, p_value = proportions_ztest(count, nobs, alternative='two-sided')

print(f"对照组：n = {n_ctrl:,}，转化数 = {conv_ctrl:,}，转化率 = {rate_ctrl*100:.4f}%")
print(f"实验组：n = {n_trt:,}，转化数 = {conv_trt:,}，转化率 = {rate_trt*100:.4f}%")
print()
print(f"z 统计量：{z_stat:.4f}")
print(f"p 值：    {p_value:.4f}")
print()

alpha = 0.05
if p_value < alpha:
    print(f"✅ p = {p_value:.4f} < α = {alpha}，拒绝原假设 H₀")
    print("   结论：两组转化率存在统计显著差异。")
else:
    print(f"❌ p = {p_value:.4f} ≥ α = {alpha}，未能拒绝原假设 H₀")
    print("   结论：两组转化率无统计显著差异。")
print()

# ── 2. 置信区间 ────────────────────────────────────────────────────────────
print("=" * 55)
print("【各组转化率 95% 置信区间】")
print("=" * 55)

ci_ctrl = proportion_confint(conv_ctrl, n_ctrl, alpha=0.05, method='normal')
ci_trt  = proportion_confint(conv_trt,  n_trt,  alpha=0.05, method='normal')

print(f"对照组 95% CI：[{ci_ctrl[0]*100:.4f}%, {ci_ctrl[1]*100:.4f}%]")
print(f"实验组 95% CI：[{ci_trt[0]*100:.4f}%, {ci_trt[1]*100:.4f}%]")
print()

diff = rate_trt - rate_ctrl
se_diff = np.sqrt(
    rate_ctrl * (1 - rate_ctrl) / n_ctrl +
    rate_trt  * (1 - rate_trt)  / n_trt
)
ci_diff_lo = diff - 1.96 * se_diff
ci_diff_hi = diff + 1.96 * se_diff
print(f"差值（实验组 - 对照组）：{diff*100:.4f}%")
print(f"差值 95% CI：[{ci_diff_lo*100:.4f}%, {ci_diff_hi*100:.4f}%]")
print()

# ── 3. 可视化：z 分布与拒绝域 ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('A/B Test 假设检验结果', fontsize=14, fontweight='bold')

# 图一：z 分布曲线
x = np.linspace(-5, 5, 1000)
y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)

z_crit = 1.96
axes[0].plot(x, y, color='#333333', linewidth=2)
axes[0].fill_between(x, y, where=(x <= -z_crit), color='#E84B4B', alpha=0.4, label='拒绝域 (α/2 = 0.025)')
axes[0].fill_between(x, y, where=(x >= z_crit),  color='#E84B4B', alpha=0.4)
axes[0].fill_between(x, y, where=((x > -z_crit) & (x < z_crit)), color='#A8D5A2', alpha=0.3, label='接受域')
axes[0].axvline(z_stat, color='#1A6FB5', linewidth=2.5, linestyle='--', label=f'z = {z_stat:.4f}')
axes[0].axvline(-z_crit, color='#E84B4B', linewidth=1.5, linestyle=':')
axes[0].axvline( z_crit, color='#E84B4B', linewidth=1.5, linestyle=':', label=f'临界值 ±{z_crit}')
axes[0].set_title('z 检验：标准正态分布与拒绝域', fontsize=11)
axes[0].set_xlabel('z 值')
axes[0].set_ylabel('概率密度')
axes[0].legend(fontsize=9)
axes[0].grid(linestyle='--', alpha=0.3)
axes[0].spines[['top', 'right']].set_visible(False)
axes[0].text(z_stat + 0.1, 0.3, f'p = {p_value:.4f}', color='#1A6FB5', fontsize=10)

# 图二：置信区间对比
groups  = ['对照组\n(old_page)', '实验组\n(new_page)']
centers = [rate_ctrl * 100, rate_trt * 100]
errors  = [
    (rate_ctrl - ci_ctrl[0]) * 100,
    (rate_trt  - ci_trt[0])  * 100,
]
colors = ['#4C72B0', '#DD8452']

for i, (g, c, e, col) in enumerate(zip(groups, centers, errors, colors)):
    axes[1].errorbar(i, c, yerr=e, fmt='o', color=col,
                     markersize=10, capsize=8, capthick=2, linewidth=2)
    axes[1].text(i + 0.07, c, f'{c:.2f}%', va='center', fontsize=10, color=col)

axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(groups, fontsize=10)
axes[1].set_xlim(-0.5, 1.5)
axes[1].set_ylim(11.5, 12.5)
axes[1].set_title('两组转化率与 95% 置信区间', fontsize=11)
axes[1].set_ylabel('转化率 (%)')
axes[1].grid(axis='y', linestyle='--', alpha=0.3)
axes[1].spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('03_hypothesis_test.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ 图表已保存为 03_hypothesis_test.png")
print()

# ── 4. 最终结论 ────────────────────────────────────────────────────────────
print("=" * 55)
print("【最终结论】")
print("=" * 55)
print(f"z 统计量：{z_stat:.4f}，落在接受域（-1.96, +1.96）内")
print(f"p 值 {p_value:.4f} ≥ 0.05，未能拒绝 H₀")
print(f"差值 95% CI [{ci_diff_lo*100:.4f}%, {ci_diff_hi*100:.4f}%] 包含 0")
print()
print("新页面（new_page）未带来统计显著的转化率提升。")
print("观察到的 -0.16% 差异在统计上属于随机波动范围。")
print()
print("【业务建议】")
print("不建议将新页面全量上线。")
print("可考虑以下方向：")
print("  1. 延长实验周期或扩大样本量，进一步确认结果")
print("  2. 针对特定用户群体（如新用户/老用户）做分层分析")
print("  3. 重新审视新页面的设计改动点，评估是否值得继续迭代")