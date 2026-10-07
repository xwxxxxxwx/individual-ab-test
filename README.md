# A/B Test 数据分析

> 个人项目 | Python | 统计分析 | A/B 测试

## 项目简介

电商转化率 A/B 测试分析项目，通过假设检验和统计分析方法，评估产品改动对用户转化率的影响。

项目解决的核心问题：如何科学地判断 A/B 两组的转化率差异是真实的效果提升，还是随机波动导致的。通过统计显著性检验给出量化结论。

## 技术栈

- 编程语言：Python 3
- 数据处理：Pandas, NumPy
- 统计分析：SciPy（Z检验、假设检验）
- 可视化：Matplotlib, Seaborn
- 开发环境：Jupyter Notebook

## 分析内容

### 数据清洗
- 原始数据探索性分析（EDA）
- 异常值处理
- 缺失值处理
- 数据格式转换

### 统计分析
- A/B 两组转化率对比
- 统计显著性检验（Z 检验 / 比例检验）
- 置信区间计算
- P 值解读
- 用户分群效果差异分析
- 样本量和统计功效评估

### 可视化
- 转化率对比柱状图
- 置信区间可视化
- 分布对比图
- 分群效果对比图

## 代码结构

```
.
├── AB_Test_Analysis.ipynb    # 主分析 Notebook
├── ab_data.csv               # 原始 A/B 测试数据
├── ab_data_clean.csv         # 清洗后的数据
├── scripts/                  # Python 脚本工具
│   ├── 0. 数据加载与初步了解.py
│   ├── 1. 数据清洗.py
│   ├── 2. 探索性分析（EDA）.py
│   └── 3. 假设检验.py
├── notes/                    # 分析笔记
│   ├── 0.假设与实验设定.txt
│   ├── 1. 数据清洗结果说明.txt
│   ├── 2. 探索性分析结果说明.txt
│   └── 3. 假设检验结果说明
├── images/                   # 分析图表输出
│   ├── 2_eda_charts.png
│   └── 3_hypothesis_test.png
└── README.md
```

## 快速开始

### 克隆项目

```bash
git clone https://github.com/xwxxxxxwx/individual-ab-test.git
cd individual-ab-test
```

### 环境配置

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

# 安装依赖
pip install pandas numpy scipy matplotlib seaborn jupyter
```

### 运行分析

```bash
jupyter notebook
# 在浏览器中打开 AB_Test_Analysis.ipynb
```

### 关于数据文件

本项目包含示例数据文件（ab_data.csv），文件体积较小，已提交至仓库。
如使用自有数据，请替换文件并保持列名格式一致。

## 项目说明

- 项目类型：个人数据分析练习项目
- 应用场景：电商产品 A/B 测试效果评估
