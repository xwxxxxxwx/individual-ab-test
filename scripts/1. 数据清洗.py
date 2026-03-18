"""
A/B Test 项目 - 第 1 步：数据清洗
清洗目标：
  1. 移除分组与页面不匹配的记录（control 看到 new_page，或 treatment 看到 old_page）
  2. 移除同一用户多次出现的重复记录（只保留首次）
  3. 输出清洗前后对比报告
"""

import pandas as pd
import numpy as np

# ── 加载数据 ───────────────────────────────────────────────────────────────
df = pd.read_csv('ab_data.csv')
print(f"清洗前总行数：{len(df):,}")
print()

# ── 1. 检查分组与页面不匹配的记录 ──────────────────────────────────────────
print("=" * 55)
print("【检查 1：分组与页面不匹配】")
print("=" * 55)

mismatch = df[
    ((df['group'] == 'control')   & (df['landing_page'] == 'new_page')) |
    ((df['group'] == 'treatment') & (df['landing_page'] == 'old_page'))
]
print(f"不匹配记录数：{len(mismatch):,}")
print(f"示例：")
print(mismatch.head(3))
print()

# ── 2. 检查重复用户 ────────────────────────────────────────────────────────
print("=" * 55)
print("【检查 2：重复用户】")
print("=" * 55)

dup_users = df[df.duplicated(subset='user_id', keep=False)]
print(f"重复出现的 user_id 记录数：{len(dup_users):,}")
print(f"涉及独立用户数：{dup_users['user_id'].nunique():,}")
print()

# ── 3. 执行清洗 ────────────────────────────────────────────────────────────
print("=" * 55)
print("【执行清洗】")
print("=" * 55)

# 步骤 1：移除分组与页面不匹配的记录
df_clean = df[
    ((df['group'] == 'control')   & (df['landing_page'] == 'old_page')) |
    ((df['group'] == 'treatment') & (df['landing_page'] == 'new_page'))
].copy()
print(f"移除不匹配记录后：{len(df_clean):,} 行（移除了 {len(df) - len(df_clean):,} 条）")

# 步骤 2：每个用户只保留时间最早的那条记录
df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
df_clean = df_clean.sort_values('timestamp').drop_duplicates(subset='user_id', keep='first')
print(f"移除重复用户后：  {len(df_clean):,} 行（再移除了 {len(df_clean) - len(df_clean):,} 条）")
print()

# ── 4. 清洗前后对比报告 ────────────────────────────────────────────────────
print("=" * 55)
print("【清洗前后对比报告】")
print("=" * 55)

control_before   = df[df['group'] == 'control']
treatment_before = df[df['group'] == 'treatment']
control_after    = df_clean[df_clean['group'] == 'control']
treatment_after  = df_clean[df_clean['group'] == 'treatment']

print(f"{'':20s} {'清洗前':>12s} {'清洗后':>12s}")
print("-" * 46)
print(f"{'总行数':20s} {len(df):>12,} {len(df_clean):>12,}")
print(f"{'对照组样本量':20s} {len(control_before):>12,} {len(control_after):>12,}")
print(f"{'实验组样本量':20s} {len(treatment_before):>12,} {len(treatment_after):>12,}")
print(f"{'对照组转化率':20s} {control_before['converted'].mean():>11.4f} {control_after['converted'].mean():>11.4f}")
print(f"{'实验组转化率':20s} {treatment_before['converted'].mean():>11.4f} {treatment_after['converted'].mean():>11.4f}")
print(f"{'转化率差值':20s} {(treatment_before['converted'].mean()-control_before['converted'].mean())*100:>10.4f}% {(treatment_after['converted'].mean()-control_after['converted'].mean())*100:>10.4f}%")
print()

# ── 5. 保存清洗后的数据 ────────────────────────────────────────────────────
df_clean.to_csv('ab_data_clean.csv', index=False)
print("✅ 清洗完成，已保存为 ab_data_clean.csv")
print(f"   最终数据：{len(df_clean):,} 行，{df_clean['user_id'].nunique():,} 个独立用户")