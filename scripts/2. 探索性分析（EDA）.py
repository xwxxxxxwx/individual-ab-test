"""
A/B Test 项目 - 第 2 步：探索性分析（EDA）
分析目标：
  1. 对比两组转化率及置信区间
  2. 可视化两组转化率差异
  3. 分析转化率随时间的变化趋势
  4. 输出 EDA 小结
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ── 加载清洗后数据 ─────────────────────────────────────────────────────────
df = pd.read_csv('ab_data_clean.csv', parse_dates=['timestamp'])

control   = df[df['group'] == 'control']
treatment = df[df['group'] == 'treatment']

# ── 1. 基础统计：转化率 + 95% 置信区间 ────────────────────────────────────
print("=" * 55)
print("【两组转化率统计（含 95% 置信区间）】")
print("=" * 55)

def conv_stats(group_df, label):
    n    = len(group_df)
    conv = group_df['converted'].sum()
    rate = conv / n
    se   = np.sqrt(rate * (1 - rate) / n)
    ci_lo, ci_hi = rate - 1.96 * se, rate + 1.96 * se
    print(f"{label}")
    print(f"  样本量：{n:,}")
    print(f"  转化数：{conv:,}")
    print(f"  转化率：{rate:.4f} ({rate*100:.2f}%)")
    print(f"  95% CI：[{ci_lo*100:.4f}%, {ci_hi*100:.4f}%]")
    print()
    return rate, se

rate_ctrl, se_ctrl = conv_stats(control,   "对照组（control / old_page）")
rate_trt,  se_trt  = conv_stats(treatment, "实验组（treatment / new_page）")

diff = rate_trt - rate_ctrl
se_diff = np.sqrt(se_ctrl**2 + se_trt**2)
ci_diff_lo = diff - 1.96 * se_diff
ci_diff_hi = diff + 1.96 * se_diff
print(f"转化率差值（实验组 - 对照组）：{diff*100:.4f}%")
print(f"差值 95% CI：[{ci_diff_lo*100:.4f}%, {ci_diff_hi*100:.4f}%]")
print()

# ── 2. 图表一：两组转化率对比柱状图 ───────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('A/B Test 探索性分析', fontsize=14, fontweight='bold', y=1.02)

labels = ['对照组\n(old_page)', '实验组\n(new_page)']
rates  = [rate_ctrl, rate_trt]
errors = [1.96 * se_ctrl, 1.96 * se_trt]
colors = ['#4C72B0', '#DD8452']

bars = axes[0].bar(labels, [r * 100 for r in rates], color=colors,
                   width=0.45, yerr=[e * 100 for e in errors],
                   capsize=6, error_kw={'linewidth': 1.5})
axes[0].set_title('两组转化率对比（含 95% CI）', fontsize=12)
axes[0].set_ylabel('转化率 (%)')
axes[0].set_ylim(0, max([r * 100 for r in rates]) * 1.3)
for bar, rate in zip(bars, rates):
    axes[0].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.15,
                 f'{rate*100:.2f}%', ha='center', va='bottom', fontsize=11)
axes[0].grid(axis='y', linestyle='--', alpha=0.4)
axes[0].spines[['top', 'right']].set_visible(False)

# ── 3. 图表二：转化率随时间变化趋势 ───────────────────────────────────────
df['date'] = df['timestamp'].dt.date

daily = df.groupby(['date', 'group']).agg(
    n=('converted', 'count'),
    conv=('converted', 'sum')
).reset_index()
daily['rate'] = daily['conv'] / daily['n']
daily['date'] = pd.to_datetime(daily['date'])

for grp, color, label in [
    ('control',   '#4C72B0', '对照组（old_page）'),
    ('treatment', '#DD8452', '实验组（new_page）'),
]:
    d = daily[daily['group'] == grp].sort_values('date')
    axes[1].plot(d['date'], d['rate'] * 100, color=color, label=label,
                 linewidth=1.8, marker='o', markersize=3)

axes[1].set_title('每日转化率趋势', fontsize=12)
axes[1].set_ylabel('转化率 (%)')
axes[1].set_xlabel('日期')
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes[1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=30, ha='right')
axes[1].legend(fontsize=10)
axes[1].grid(linestyle='--', alpha=0.4)
axes[1].spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('02_eda_charts.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ 图表已保存为 02_eda_charts.png")
print()

# ── 4. EDA 小结 ────────────────────────────────────────────────────────────
print("=" * 55)
print("【EDA 小结】")
print("=" * 55)
ci_contains_zero = ci_diff_lo < 0 < ci_diff_hi
print(f"对照组转化率：{rate_ctrl*100:.2f}%")
print(f"实验组转化率：{rate_trt*100:.2f}%")
print(f"差值：{diff*100:.4f}%，差值 95% CI 包含 0：{ci_contains_zero}")
if ci_contains_zero:
    print("→ 差值置信区间包含 0，初步判断两组差异可能不显著。")
    print("   将在第三步假设检验中正式验证。")
else:
    print("→ 差值置信区间不包含 0，初步判断两组存在显著差异。")
    print("   将在第三步假设检验中正式验证。")