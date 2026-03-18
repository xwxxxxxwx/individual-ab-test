"""
A/B Test 项目 - 第 0 步：数据加载与初步了解
业务背景：电商平台新旧产品页面的转化率对比
数据集：ab_data.csv（与本文件放在同一目录下）
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# ── 1. 加载数据 ────────────────────────────────────────────────────────────
df = pd.read_csv('ab_data.csv')

# ── 2. 基本信息 ────────────────────────────────────────────────────────────
print("=" * 55)
print("【数据基本信息】")
print("=" * 55)
print(df.info())
print()

print("前 5 行数据：")
print(df.head())
print()

print(f"数据总行数：{len(df):,}")
print(f"字段列表：{list(df.columns)}")
print()

# ── 3. 各字段取值分布 ──────────────────────────────────────────────────────
print("=" * 55)
print("【各字段取值统计】")
print("=" * 55)
print("group 分组情况：")
print(df['group'].value_counts())
print()

print("landing_page 页面情况：")
print(df['landing_page'].value_counts())
print()

print("converted 转化情况（0=未转化，1=转化）：")
print(df['converted'].value_counts())
print()

# ── 4. 两组初步转化率 ──────────────────────────────────────────────────────
print("=" * 55)
print("【两组初步转化率（清洗前）】")
print("=" * 55)
control_rate   = df[df['group'] == 'control']['converted'].mean()
treatment_rate = df[df['group'] == 'treatment']['converted'].mean()

print(f"对照组（control）  转化率：{control_rate:.4f}  ({control_rate*100:.2f}%)")
print(f"实验组（treatment）转化率：{treatment_rate:.4f}  ({treatment_rate*100:.2f}%)")
print(f"差值：{(treatment_rate - control_rate)*100:.4f}%")
print()

# ── 5. 样本量评估（Power Analysis）────────────────────────────────────────
print("=" * 55)
print("【样本量评估 - Power Analysis】")
print("=" * 55)
# 使用对照组真实转化率作为基准，设定期望提升为 +2%（实际差异很小时的合理假设）
baseline_rate  = control_rate          # 基准转化率（对照组实测）
expected_lift  = 0.02                  # 期望检测到的最小提升幅度
new_rate       = baseline_rate + expected_lift

# 计算 effect size（Cohen's h）
effect_size = proportion_effectsize(new_rate, baseline_rate)

# 计算所需样本量（双尾，alpha=0.05，power=0.80）
analysis = NormalIndPower()
required_n = analysis.solve_power(
    effect_size=effect_size,
    alpha=0.05,
    power=0.80,
    alternative='two-sided'
)

print(f"基准转化率（对照组）：{baseline_rate:.4f} ({baseline_rate*100:.2f}%)")
print(f"期望检测的最小提升：+{expected_lift*100:.1f}%")
print(f"目标新页面转化率：   {new_rate:.4f} ({new_rate*100:.2f}%)")
print(f"Effect size（Cohen's h）：{effect_size:.4f}")
print()
print(f"每组所需最少样本量：{int(np.ceil(required_n)):,}")
print(f"两组合计所需样本量：{int(np.ceil(required_n)) * 2:,}")
print()

# 对比实际样本量
actual_control   = len(df[df['group'] == 'control'])
actual_treatment = len(df[df['group'] == 'treatment'])
print(f"实际对照组样本量：  {actual_control:,}")
print(f"实际实验组样本量：  {actual_treatment:,}")

if actual_control >= required_n and actual_treatment >= required_n:
    print("✅ 实际样本量充足，满足统计效能要求（Power ≥ 80%）")
else:
    print("⚠️  实际样本量不足，检验结果可信度存疑")