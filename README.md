# 影评数据挖掘分析系统 - 使用说明

## 📖 项目简介

这是一个全面的观众影评数据挖掘分析系统，基于51万+条真实影评数据，提供情感分析、关键词挖掘、趋势分析等多维度洞察，并自动生成精美的可视化图表。

---

## 📊 系统功能

### 核心功能模块

1. **情感分析**
   - 基于星级的情感分类（正面/中性/负面）
   - 情感分布可视化
   - 评分与情感关联分析

2. **关键词挖掘**
   - 高频词汇TOP50统计
   - 正面/负面词云对比
   - TF-IDF关键主题提取

3. **电影分析**
   - 热门电影TOP10排行榜
   - 评分分布统计
   - 点赞数与互动分析

4. **时间趋势**
   - 历年评论数量趋势
   - 月度情感变化趋势
   - 评分时间序列分析

5. **相关性分析**
   - 特征相关性热力图
   - 散点图矩阵
   - 情感-星级交叉分析

6. **综合仪表板**
   - 多维度数据总览
   - 一键生成11+张可视化图表

---

## 🚀 快速开始

### 环境要求

- **操作系统**: Windows / Linux / macOS
- **Python版本**: Python 3.8 或更高版本
- **内存**: 建议4GB以上（数据量较大）

### 安装步骤

#### 方法一：使用虚拟环境（强烈推荐）✨

**Windows用户：**

1. **一键创建虚拟环境并安装依赖**
   ```bash
   双击运行 setup_venv.bat
   ```

2. **运行分析（自动激活虚拟环境）**
   ```bash
   双击运行 run_analysis_venv.bat
   ```

**手动激活虚拟环境：**
```bash
双击运行 activate_venv.bat
# 或者在命令行中执行
venv\Scripts\activate.bat
```

**Linux/macOS用户：**

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # Linux/macOS

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行分析
python film_review_analysis.py

# 5. 退出虚拟环境
deactivate
```

#### 方法二：全局安装

**Windows用户：**

1. **安装依赖**
   ```bash
   双击运行 install_dependencies.bat
   ```

2. **运行分析**
   ```bash
   双击运行 run_analysis.bat
   ```

**Linux/macOS 用户：**

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行分析**
   ```bash
   python film_review_analysis.py
   ```

---

## 📁 文件说明

```
项目目录/
│
├── data.xlsx                      # 原始影评数据（51万+条记录）
├── film_review_analysis.py        # 主分析脚本
├── requirements.txt               # Python依赖包列表
│
├── setup_venv.bat                 # 🌟 创建虚拟环境脚本（推荐）
├── activate_venv.bat              # 🌟 激活虚拟环境快捷脚本
├── run_analysis_venv.bat          # 🌟 虚拟环境下运行分析
│
├── install_dependencies.bat       # Windows依赖安装脚本（全局）
├── run_analysis.bat               # Windows运行脚本（全局）
├── README.md                      # 本说明文档
│
├── venv/                          # 虚拟环境目录（运行setup_venv.bat后生成）
│
└── analysis_results/              # 分析结果输出目录（自动生成）
    ├── 01_sentiment_distribution.png      # 情感与星级分布
    ├── 02_score_distribution.png          # 评分分布直方图
    ├── 03_top_keywords.png                # 高频关键词柱状图
    ├── 04_wordcloud.png                   # 词云图（3合1）
    ├── 05_top_movies.png                  # 热门电影排行榜
    ├── 06_likes_analysis.png              # 点赞数分析
    ├── 07_time_trend.png                  # 年度趋势分析
    ├── 08_monthly_trend.png               # 月度趋势分析
    ├── 09_correlation_heatmap.png         # 相关性热力图
    ├── 10_scatter_matrix.png              # 散点图矩阵
    ├── 11_comprehensive_dashboard.png     # 综合仪表板
    └── analysis_report.md                 # 数据分析报告
```

---

## 📈 输出结果

### 可视化图表（共11张）

| 序号 | 图表文件 | 说明 |
|------|----------|------|
| 1 | `01_sentiment_distribution.png` | 用户星级评分分布 + 情感倾向分布（饼图） |
| 2 | `02_score_distribution.png` | 电影评分分布直方图（含均值、中位数线） |
| 3 | `03_top_keywords.png` | TOP 30 高频关键词柱状图 |
| 4 | `04_wordcloud.png` | 三合一词云图（全部/正面/负面评论） |
| 5 | `05_top_movies.png` | TOP 10 电影排行（按评论数和评分） |
| 6 | `06_likes_analysis.png` | 点赞数分布箱线图 + 对数分布图 |
| 7 | `07_time_trend.png` | 历年评论数量 + 评分/星级趋势 |
| 8 | `08_monthly_trend.png` | 月度评论量 + 正面评论率趋势 |
| 9 | `09_correlation_heatmap.png` | 特征相关性 + 情感-星级热力图 |
| 10 | `10_scatter_matrix.png` | 4x4 特征散点图矩阵 |
| 11 | `11_comprehensive_dashboard.png` | 综合分析仪表板 |

### 分析报告

- **文件名**: `analysis_report.md`
- **格式**: Markdown格式，可用任何文本编辑器打开
- **内容**:
  - 数据概览
  - 情感分布统计
  - TOP 20 高频关键词
  - 热门电影TOP 10详情
  - 时间趋势分析
  - 相关性分析结果
  - 关键发现总结

---

## 🔧 技术栈

| 类别 | 技术/库 | 用途 |
|------|---------|------|
| 数据处理 | pandas, numpy | 数据加载、清洗、统计 |
| 中文分词 | jieba | 评论文本分词、关键词提取 |
| 可视化 | matplotlib, seaborn | 各类图表绘制 |
| 词云 | wordcloud | 生成词云图 |
| 机器学习 | scikit-learn | TF-IDF、主题模型 |
| 文件读取 | openpyxl | Excel文件处理 |

---

## ⚙️ 自定义配置

### 修改输出目录

编辑 `film_review_analysis.py` 第40行：

```python
self.output_dir = "analysis_results"  # 改为你想要的目录名
```

### 调整图表样式

编辑第18-22行的绘图配置：

```python
plt.rcParams['font.sans-serif'] = ['SimHei']  # 修改字体
sns.set_style("whitegrid")  # 修改风格：whitegrid/darkgrid/white/dark
sns.set_palette("husl")     # 修改配色方案
```

### 自定义停用词

编辑 `_load_stopwords()` 方法（第616-632行），添加或删除停用词。

---

## 💡 使用技巧

### 1. 处理大数据集

如果数据量非常大（>100万条），建议：
- 增加内存分配
- 使用采样分析：在代码中添加 `self.df = self.df.sample(100000)`

### 2. 自定义分析范围

在 `run()` 方法中注释掉不需要的分析模块：

```python
# self.correlation_analysis()  # 跳过相关性分析
```

### 3. 修改词云字体

如果词云显示乱码，修改第391行的字体路径：

```python
font_path='C:/Windows/Fonts/simhei.ttf',  # Windows
# font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # Linux
```

---

## 🐛 常见问题

### 问题1：安装依赖失败

**解决方案**：
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题2：词云显示乱码

**解决方案**：
- Windows：确保系统已安装黑体（SimHei）字体
- Linux：安装中文字体 `sudo apt-get install fonts-wqy-zenhei`
- macOS：下载并安装中文字体

### 问题3：内存不足

**解决方案**：
- 使用采样分析减少数据量
- 关闭其他占用内存的程序
- 分批处理数据

### 问题4：图表不清晰

**解决方案**：
修改 `savefig()` 的 `dpi` 参数（默认300）：
```python
plt.savefig('xxx.png', dpi=600)  # 提高到600
```

---

## 📚 数据字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| ID | int | 记录唯一标识符 |
| Movie_Name | str | 电影名称 |
| Score | float | 电影豆瓣评分 (0-10) |
| Review_People | int | 评论总人数 |
| Star_Distribution | str | 星级分布比例 |
| Craw_Date | datetime | 数据爬取日期 |
| Username | str | 评论用户名 |
| Date | datetime | 评论发表日期 |
| Star | int | 用户给出的星级 (1-5) |
| Comment | str | 影评文本内容 |
| Comment_Distribution | str | 评论分布 |
| Like | int | 评论获得的点赞数 |

---

## 📊 示例输出

运行完成后，控制台会显示如下信息：

```
============================================================
🎬 影评数据挖掘分析系统启动
============================================================

📂 正在加载数据...
✅ 数据加载成功！共 515315 条记录，12 个字段

📊 数据概览:
   - 电影数量: 871 部
   - 评论数量: 515315 条
   - 用户数量: 172763 人
   - 时间范围: 2005-06-12 至 2019-10-15

🧹 开始数据预处理...
   - 处理缺失值...
   - 提取评论长度特征...
   - 添加情感分类...
   - 提取时间特征...
✅ 数据预处理完成！

😊 开始情感分析...
   - 生成星级分布饼图...
   ✅ 保存: 01_sentiment_distribution.png
   - 生成评分分布直方图...
   ✅ 保存: 02_score_distribution.png
✅ 情感分析完成！

... (更多输出)

============================================================
🎉 所有分析任务完成！
============================================================

📁 分析结果保存在目录: analysis_results/
📊 共生成 11 张可视化图表
📄 分析报告: analysis_results/analysis_report.md

感谢使用影评数据挖掘分析系统！
```

---

## 🤝 贡献与反馈

如有问题或建议，欢迎反馈！

---

## 📄 许可证

本项目仅供学习和研究使用。

---

**祝您使用愉快！🎉**
