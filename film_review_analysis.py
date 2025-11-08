"""
观众影评数据挖掘分析系统
作者：Claude Code
日期：2025-11-08
功能：对电影评论数据进行全面的数据挖掘和可视化分析
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
import jieba.analyse
from collections import Counter
from wordcloud import WordCloud
import warnings
from datetime import datetime
import re
from matplotlib import font_manager

warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 设置绘图风格
sns.set_style("whitegrid")
sns.set_palette("husl")


def _configure_chinese_font():
    """配置 Matplotlib 字体，确保中文正常显示并返回可用字体信息。"""
    candidate_fonts = [
        ("SimHei", ["simhei.ttf"]),
        ("Microsoft YaHei", ["msyh.ttc", "msyh.ttf"]),
        ("SimSun", ["simsun.ttc", "simsun.ttf"]),
        ("PingFang SC", ["PingFang.ttc", "PingFang Regular.ttf"]),
        ("Noto Sans CJK SC", ["NotoSansCJK-Regular.ttc", "NotoSansCJKsc-Regular.otf"]),
        ("Source Han Sans CN", ["SourceHanSansCN-Regular.otf", "SourceHanSansSC-Regular.otf"]),
    ]

    fm = font_manager.fontManager
    available_by_name = {f.name.lower(): f.fname for f in fm.ttflist}

    def _set_rc(font_name_to_use):
        plt.rcParams['font.sans-serif'] = [font_name_to_use]
        plt.rcParams['font.family'] = 'sans-serif'

    search_dirs = [
        os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts"),
        "/System/Library/Fonts",
        "/Library/Fonts",
        os.path.expanduser("~/Library/Fonts"),
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        os.path.expanduser("~/.local/share/fonts"),
    ]

    for font_name, file_names in candidate_fonts:
        try:
            found_path = font_manager.findfont(font_name, fallback_to_default=False)
            if found_path and os.path.exists(found_path):
                actual_name = font_manager.FontProperties(fname=found_path).get_name()
                _set_rc(actual_name)
                return actual_name, found_path
        except Exception:
            pass

        lower_name = font_name.lower()
        if lower_name in available_by_name:
            font_path = available_by_name[lower_name]
            actual_name = font_manager.FontProperties(fname=font_path).get_name() if os.path.exists(font_path) else font_name
            _set_rc(actual_name)
            return actual_name, font_path

        for file_name in file_names:
            for directory in search_dirs:
                candidate_path = os.path.join(directory, file_name)
                if os.path.exists(candidate_path):
                    try:
                        fm.addfont(candidate_path)
                        actual_name = font_manager.FontProperties(fname=candidate_path).get_name()
                        _set_rc(actual_name)
                        return actual_name, candidate_path
                    except Exception:
                        continue

    return None, None


CHINESE_FONT_NAME, CHINESE_FONT_PATH = _configure_chinese_font()


class FilmReviewAnalyzer:
    """
    影评数据分析器
    """

    def __init__(self, data_path):
        """
        初始化分析器

        参数:
            data_path: Excel数据文件路径
        """
        print("=" * 60)
        print("🎬 影评数据挖掘分析系统启动")
        print("=" * 60)

        self.data_path = data_path
        self.df = None
        self.output_dir = "analysis_results"
        self.report = []
        self.wordcloud_font_path = CHINESE_FONT_PATH

        if CHINESE_FONT_NAME:
            print(f"✅ 检测到中文字体: {CHINESE_FONT_NAME}")
        else:
            print("⚠️ 未检测到中文字体，图表中的中文可能无法正常显示。")

        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✅ 创建输出目录: {self.output_dir}")

    def load_data(self):
        """
        加载并初步检查数据
        """
        print("\n📂 正在加载数据...")
        self.df = pd.read_excel(self.data_path)
        print(f"✅ 数据加载成功！共 {len(self.df)} 条记录，{len(self.df.columns)} 个字段")

        # 基本信息
        print(f"\n📊 数据概览:")
        print(f"   - 电影数量: {self.df['Movie_Name'].nunique()} 部")
        print(f"   - 评论数量: {len(self.df)} 条")
        print(f"   - 用户数量: {self.df['Username'].nunique()} 人")
        print(f"   - 时间范围: {self.df['Date'].min()} 至 {self.df['Date'].max()}")

        self.report.append("# 影评数据挖掘分析报告\n")
        self.report.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.report.append(f"**数据规模**: {len(self.df)} 条记录\n")
        self.report.append(f"**电影数量**: {self.df['Movie_Name'].nunique()} 部\n\n")

    def preprocess_data(self):
        """
        数据预处理和清洗
        """
        print("\n🧹 开始数据预处理...")

        # 1. 处理缺失值
        print("   - 处理缺失值...")
        missing_before = self.df.isnull().sum().sum()
        self.df['Comment'].fillna('', inplace=True)
        self.df['Username'].fillna('匿名用户', inplace=True)
        missing_after = self.df.isnull().sum().sum()
        print(f"     处理前缺失值: {missing_before}, 处理后: {missing_after}")

        # 2. 添加评论长度特征
        print("   - 提取评论长度特征...")
        self.df['comment_length'] = self.df['Comment'].apply(lambda x: len(str(x)))

        # 3. 添加情感分类（基于星级）
        print("   - 添加情感分类...")
        def classify_sentiment(star):
            if star <= 2:
                return '负面'
            elif star == 3:
                return '中性'
            else:
                return '正面'

        self.df['sentiment'] = self.df['Star'].apply(classify_sentiment)

        # 4. 时间特征提取
        print("   - 提取时间特征...")
        self.df['year'] = pd.to_datetime(self.df['Date']).dt.year
        self.df['month'] = pd.to_datetime(self.df['Date']).dt.month
        self.df['year_month'] = pd.to_datetime(self.df['Date']).dt.to_period('M')

        print("✅ 数据预处理完成！")

        # 统计信息
        sentiment_dist = self.df['sentiment'].value_counts()
        self.report.append("## 一、情感分布\n")
        for sent, count in sentiment_dist.items():
            pct = count / len(self.df) * 100
            self.report.append(f"- **{sent}**: {count} 条 ({pct:.2f}%)\n")
        self.report.append("\n")

    def sentiment_analysis(self):
        """
        情感分析
        """
        print("\n😊 开始情感分析...")

        # 1. 星级分布饼图
        print("   - 生成星级分布饼图...")
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        star_counts = self.df['Star'].value_counts().sort_index()
        colors = ['#ff6b6b', '#f06595', '#ffa500', '#74c0fc', '#51cf66']
        axes[0].pie(
            star_counts.values,
            labels=[f'{i}星' for i in star_counts.index],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        axes[0].set_title('用户星级评分分布', fontsize=14, fontweight='bold')

        sentiment_counts = self.df['sentiment'].value_counts()
        sentiment_colors = {'正面': '#51cf66', '中性': '#ffa500', '负面': '#ff6b6b'}
        axes[1].pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            colors=[sentiment_colors[s] for s in sentiment_counts.index],
            startangle=90
        )
        axes[1].set_title('情感倾向分布', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/01_sentiment_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 01_sentiment_distribution.png")

        # 2. 评分分布直方图
        print("   - 生成评分分布直方图...")
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.hist(self.df['Score'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax.axvline(self.df['Score'].mean(), color='red', linestyle='--',
                  linewidth=2, label=f'平均分: {self.df["Score"].mean():.2f}')
        ax.axvline(self.df['Score'].median(), color='green', linestyle='--',
                  linewidth=2, label=f'中位数: {self.df["Score"].median():.2f}')

        ax.set_xlabel('电影评分', fontsize=12)
        ax.set_ylabel('电影数量', fontsize=12)
        ax.set_title('电影评分分布直方图', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/02_score_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 02_score_distribution.png")

        print("✅ 情感分析完成！")

    def keyword_analysis(self):
        """
        关键词分析和词云生成
        """
        print("\n🔤 开始关键词分析...")

        # 加载停用词
        print("   - 加载停用词表...")
        stopwords = self._load_stopwords()

        # 分词
        print("   - 对评论文本进行分词...")
        all_words = []
        positive_words = []
        negative_words = []

        for idx, row in self.df.iterrows():
            if idx % 50000 == 0:
                print(f"     处理进度: {idx}/{len(self.df)}")

            comment = str(row['Comment'])
            if len(comment) < 2:
                continue

            words = jieba.lcut(comment)
            words = [w for w in words if len(w) > 1 and w not in stopwords]

            all_words.extend(words)

            if row['sentiment'] == '正面':
                positive_words.extend(words)
            elif row['sentiment'] == '负面':
                negative_words.extend(words)

        print(f"     ✅ 分词完成！共提取 {len(all_words)} 个词")

        # 1. 词频统计
        print("   - 统计词频...")
        word_freq = Counter(all_words)
        top_words = word_freq.most_common(50)

        # 保存TOP词汇
        self.report.append("## 二、关键词分析\n")
        self.report.append("### TOP 20 高频词汇\n")
        for i, (word, freq) in enumerate(top_words[:20], 1):
            self.report.append(f"{i}. **{word}**: {freq} 次\n")
        self.report.append("\n")

        # 2. 绘制词频柱状图
        print("   - 生成词频柱状图...")
        fig, ax = plt.subplots(figsize=(14, 8))

        words, freqs = zip(*top_words[:30])
        bars = ax.barh(range(len(words)), freqs, color=plt.cm.viridis(np.linspace(0, 1, len(words))))
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words)
        ax.invert_yaxis()
        ax.set_xlabel('词频', fontsize=12)
        ax.set_title('TOP 30 高频关键词', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        # 添加数值标签
        for i, (bar, freq) in enumerate(zip(bars, freqs)):
            ax.text(freq + max(freqs)*0.01, i, f'{freq}',
                   va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/03_top_keywords.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 03_top_keywords.png")

        # 3. 生成词云
        print("   - 生成词云图...")

        if not self.wordcloud_font_path:
            print("⚠️ 未找到可用的中文字体文件，已跳过词云图生成。")
            self.report.append("⚠️ 由于系统缺少中文字体，词云图未生成。\n\n")
            print("✅ 关键词分析完成！")
            return word_freq

        font_path = self.wordcloud_font_path

        # 整体词云
        wordcloud = WordCloud(
            font_path=font_path,
            width=1600,
            height=800,
            background_color='white',
            max_words=200,
            colormap='viridis'
        ).generate(' '.join(all_words))

        fig, axes = plt.subplots(1, 3, figsize=(24, 8))

        # 全部评论词云
        axes[0].imshow(wordcloud, interpolation='bilinear')
        axes[0].axis('off')
        axes[0].set_title('全部评论词云', fontsize=14, fontweight='bold', pad=20)

        # 正面评论词云
        if positive_words:
            positive_wc = WordCloud(
                font_path=font_path,
                width=1600,
                height=800,
                background_color='white',
                max_words=150,
                colormap='Greens'
            ).generate(' '.join(positive_words))

            axes[1].imshow(positive_wc, interpolation='bilinear')
            axes[1].axis('off')
            axes[1].set_title('正面评论词云', fontsize=14, fontweight='bold', pad=20)

        # 负面评论词云
        if negative_words:
            negative_wc = WordCloud(
                font_path=font_path,
                width=1600,
                height=800,
                background_color='white',
                max_words=150,
                colormap='Reds'
            ).generate(' '.join(negative_words))

            axes[2].imshow(negative_wc, interpolation='bilinear')
            axes[2].axis('off')
            axes[2].set_title('负面评论词云', fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/04_wordcloud.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 04_wordcloud.png")

        print("✅ 关键词分析完成！")

        return word_freq

    def movie_analysis(self):
        """
        电影评分和互动分析
        """
        print("\n🎥 开始电影分析...")

        # 1. 热门电影TOP10
        print("   - 分析热门电影TOP10...")
        movie_stats = self.df.groupby('Movie_Name').agg({
            'Score': 'first',
            'ID': 'count',
            'Like': 'sum',
            'Star': 'mean'
        }).rename(columns={'ID': 'review_count', 'Like': 'total_likes', 'Star': 'avg_star'})

        top_movies = movie_stats.nlargest(10, 'review_count')

        self.report.append("## 三、热门电影 TOP 10\n")
        for i, (movie, row) in enumerate(top_movies.iterrows(), 1):
            self.report.append(f"{i}. **{movie}**\n")
            self.report.append(f"   - 评分: {row['Score']:.1f}\n")
            self.report.append(f"   - 评论数: {int(row['review_count'])} 条\n")
            self.report.append(f"   - 平均星级: {row['avg_star']:.2f}\n")
            self.report.append(f"   - 总点赞数: {int(row['total_likes'])}\n\n")

        # 绘制TOP10电影柱状图
        fig, axes = plt.subplots(2, 1, figsize=(14, 12))

        # 评论数TOP10
        ax1 = axes[0]
        movies = [m[:15]+'...' if len(m) > 15 else m for m in top_movies.index]
        bars1 = ax1.barh(range(len(movies)), top_movies['review_count'],
                        color=plt.cm.Spectral(np.linspace(0, 1, len(movies))))
        ax1.set_yticks(range(len(movies)))
        ax1.set_yticklabels(movies)
        ax1.invert_yaxis()
        ax1.set_xlabel('评论数', fontsize=12)
        ax1.set_title('TOP 10 评论最多的电影', fontsize=14, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)

        for i, (bar, count) in enumerate(zip(bars1, top_movies['review_count'])):
            ax1.text(count + max(top_movies['review_count'])*0.01, i,
                    f"{int(count)}", va='center', fontsize=9)

        # 评分最高TOP10
        top_rated = movie_stats.nlargest(10, 'Score')
        movies2 = [m[:15]+'...' if len(m) > 15 else m for m in top_rated.index]
        bars2 = axes[1].barh(range(len(movies2)), top_rated['Score'],
                            color=plt.cm.RdYlGn(np.linspace(0.3, 1, len(movies2))))
        axes[1].set_yticks(range(len(movies2)))
        axes[1].set_yticklabels(movies2)
        axes[1].invert_yaxis()
        axes[1].set_xlabel('评分', fontsize=12)
        axes[1].set_title('TOP 10 评分最高的电影', fontsize=14, fontweight='bold')
        axes[1].grid(axis='x', alpha=0.3)
        axes[1].set_xlim(0, 10)

        for i, (bar, score) in enumerate(zip(bars2, top_rated['Score'])):
            axes[1].text(score + 0.1, i, f'{score:.1f}', va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/05_top_movies.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 05_top_movies.png")

        # 2. 点赞数分析
        print("   - 分析点赞数分布...")
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # 点赞数箱线图（按星级）
        self.df.boxplot(column='Like', by='Star', ax=axes[0])
        axes[0].set_xlabel('星级', fontsize=12)
        axes[0].set_ylabel('点赞数', fontsize=12)
        axes[0].set_title('不同星级评论的点赞数分布', fontsize=13, fontweight='bold')
        axes[0].get_figure().suptitle('')

        # 点赞数分布（对数尺度）
        like_data = self.df[self.df['Like'] > 0]['Like']
        axes[1].hist(np.log10(like_data + 1), bins=50, color='coral', edgecolor='black', alpha=0.7)
        axes[1].set_xlabel('log10(点赞数+1)', fontsize=12)
        axes[1].set_ylabel('评论数量', fontsize=12)
        axes[1].set_title('点赞数分布 (对数尺度)', fontsize=13, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/06_likes_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 06_likes_analysis.png")

        print("✅ 电影分析完成！")

    def time_trend_analysis(self):
        """
        时间趋势分析
        """
        print("\n📅 开始时间趋势分析...")

        # 1. 按年统计
        print("   - 分析评论时间趋势...")
        yearly_stats = self.df.groupby('year').agg({
            'ID': 'count',
            'Score': 'mean',
            'Star': 'mean'
        }).rename(columns={'ID': 'count', 'Score': 'avg_score', 'Star': 'avg_star'})

        fig, axes = plt.subplots(2, 1, figsize=(14, 10))

        # 评论数量趋势
        ax1 = axes[0]
        ax1.plot(yearly_stats.index, yearly_stats['count'],
                marker='o', linewidth=2, markersize=8, color='steelblue')
        ax1.fill_between(yearly_stats.index, yearly_stats['count'], alpha=0.3, color='steelblue')
        ax1.set_xlabel('年份', fontsize=12)
        ax1.set_ylabel('评论数量', fontsize=12)
        ax1.set_title('历年评论数量趋势', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # 添加数据标签
        for x, y in zip(yearly_stats.index, yearly_stats['count']):
            ax1.text(x, y, f'{int(y)}', ha='center', va='bottom', fontsize=9)

        # 评分和星级趋势
        ax2 = axes[1]
        ax2_twin = ax2.twinx()

        line1 = ax2.plot(yearly_stats.index, yearly_stats['avg_score'],
                        marker='s', linewidth=2, markersize=8, color='green', label='平均电影评分')
        line2 = ax2_twin.plot(yearly_stats.index, yearly_stats['avg_star'],
                             marker='^', linewidth=2, markersize=8, color='orange', label='平均用户星级')

        ax2.set_xlabel('年份', fontsize=12)
        ax2.set_ylabel('平均电影评分', fontsize=12, color='green')
        ax2_twin.set_ylabel('平均用户星级', fontsize=12, color='orange')
        ax2.tick_params(axis='y', labelcolor='green')
        ax2_twin.tick_params(axis='y', labelcolor='orange')
        ax2.set_title('历年评分和星级趋势', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # 合并图例
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax2.legend(lines, labels, loc='best', fontsize=10)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/07_time_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 07_time_trend.png")

        # 2. 按月统计（仅统计数据量较大的年份）
        print("   - 分析月度趋势...")
        monthly_stats = self.df.groupby('year_month').agg({
            'ID': 'count',
            'sentiment': lambda x: (x == '正面').sum() / len(x) * 100
        }).rename(columns={'ID': 'count', 'sentiment': 'positive_rate'})

        fig, axes = plt.subplots(2, 1, figsize=(16, 10))

        # 月度评论量
        axes[0].plot(range(len(monthly_stats)), monthly_stats['count'],
                    linewidth=1.5, color='steelblue', alpha=0.8)
        axes[0].fill_between(range(len(monthly_stats)), monthly_stats['count'],
                            alpha=0.3, color='steelblue')
        axes[0].set_xlabel('时间', fontsize=12)
        axes[0].set_ylabel('评论数量', fontsize=12)
        axes[0].set_title('月度评论数量趋势', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)

        # 月度正面评论率
        axes[1].plot(range(len(monthly_stats)), monthly_stats['positive_rate'],
                    linewidth=1.5, color='green', alpha=0.8)
        axes[1].fill_between(range(len(monthly_stats)), monthly_stats['positive_rate'],
                            alpha=0.3, color='green')
        axes[1].set_xlabel('时间', fontsize=12)
        axes[1].set_ylabel('正面评论占比 (%)', fontsize=12)
        axes[1].set_title('月度正面评论率趋势', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(monthly_stats['positive_rate'].mean(),
                       color='red', linestyle='--', linewidth=2,
                       label=f'平均值: {monthly_stats["positive_rate"].mean():.1f}%')
        axes[1].legend(fontsize=10)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/08_monthly_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 08_monthly_trend.png")

        # 添加到报告
        self.report.append("## 四、时间趋势分析\n")
        self.report.append(f"- **时间跨度**: {self.df['year'].min()} - {self.df['year'].max()} 年\n")
        self.report.append(f"- **评论高峰年份**: {yearly_stats['count'].idxmax()} 年 ({int(yearly_stats['count'].max())} 条)\n")
        self.report.append(f"- **平均正面评论率**: {monthly_stats['positive_rate'].mean():.2f}%\n\n")

        print("✅ 时间趋势分析完成！")

    def correlation_analysis(self):
        """
        相关性分析
        """
        print("\n🔗 开始相关性分析...")

        # 准备数值数据
        numeric_cols = ['Score', 'Star', 'Like', 'comment_length']
        corr_matrix = self.df[numeric_cols].corr()

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # 相关性热力图
        sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=axes[0])
        axes[0].set_title('特征相关性热力图', fontsize=14, fontweight='bold', pad=15)

        # 情感-星级交叉表
        sentiment_star = pd.crosstab(self.df['sentiment'], self.df['Star'], normalize='columns') * 100
        sns.heatmap(sentiment_star, annot=True, fmt='.1f', cmap='YlGnBu',
                   square=False, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=axes[1])
        axes[1].set_title('情感-星级分布热力图 (%)', fontsize=14, fontweight='bold', pad=15)
        axes[1].set_xlabel('星级', fontsize=12)
        axes[1].set_ylabel('情感', fontsize=12)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/09_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 09_correlation_heatmap.png")

        # 散点图矩阵
        print("   - 生成散点图矩阵...")
        sample_df = self.df.sample(min(5000, len(self.df)), random_state=42)

        fig = plt.figure(figsize=(14, 14))

        for i, col1 in enumerate(numeric_cols):
            for j, col2 in enumerate(numeric_cols):
                ax = plt.subplot(4, 4, i*4 + j + 1)

                if i == j:
                    ax.hist(sample_df[col1], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
                    ax.set_ylabel('频数', fontsize=9)
                else:
                    ax.scatter(sample_df[col2], sample_df[col1],
                             alpha=0.3, s=10, color='steelblue')

                if i == 3:
                    ax.set_xlabel(col2, fontsize=9)
                if j == 0:
                    ax.set_ylabel(col1, fontsize=9)

                ax.grid(True, alpha=0.3)

        plt.suptitle('特征散点图矩阵', fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/10_scatter_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 10_scatter_matrix.png")

        # 添加到报告
        self.report.append("## 五、相关性分析\n")
        self.report.append("### 关键发现\n")
        self.report.append(f"- **评分与星级相关性**: {corr_matrix.loc['Score', 'Star']:.3f}\n")
        self.report.append(f"- **点赞与星级相关性**: {corr_matrix.loc['Like', 'Star']:.3f}\n")
        self.report.append(f"- **评论长度与星级相关性**: {corr_matrix.loc['comment_length', 'Star']:.3f}\n\n")

        print("✅ 相关性分析完成！")

    def comprehensive_dashboard(self):
        """
        生成综合仪表板
        """
        print("\n📊 生成综合分析仪表板...")

        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # 1. 评分分布
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(self.df['Score'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax1.set_title('评分分布', fontweight='bold')
        ax1.set_xlabel('评分')
        ax1.set_ylabel('电影数')

        # 2. 星级饼图
        ax2 = fig.add_subplot(gs[0, 1])
        star_counts = self.df['Star'].value_counts().sort_index()
        colors = ['#ff6b6b', '#f06595', '#ffa500', '#74c0fc', '#51cf66']
        ax2.pie(star_counts.values, labels=[f'{i}星' for i in star_counts.index],
               autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('星级分布', fontweight='bold')

        # 3. 情感饼图
        ax3 = fig.add_subplot(gs[0, 2])
        sentiment_counts = self.df['sentiment'].value_counts()
        sentiment_colors = {'正面': '#51cf66', '中性': '#ffa500', '负面': '#ff6b6b'}
        ax3.pie(sentiment_counts.values, labels=sentiment_counts.index,
               autopct='%1.1f%%', colors=[sentiment_colors[s] for s in sentiment_counts.index],
               startangle=90)
        ax3.set_title('情感分布', fontweight='bold')

        # 4. 年度趋势
        ax4 = fig.add_subplot(gs[1, :])
        yearly_stats = self.df.groupby('year').size()
        ax4.plot(yearly_stats.index, yearly_stats.values, marker='o', linewidth=2, markersize=8)
        ax4.fill_between(yearly_stats.index, yearly_stats.values, alpha=0.3)
        ax4.set_title('历年评论数量趋势', fontweight='bold')
        ax4.set_xlabel('年份')
        ax4.set_ylabel('评论数')
        ax4.grid(True, alpha=0.3)

        # 5. TOP10电影
        ax5 = fig.add_subplot(gs[2, :])
        movie_counts = self.df['Movie_Name'].value_counts().head(10)
        movies = [m[:20]+'...' if len(m) > 20 else m for m in movie_counts.index]
        bars = ax5.barh(range(len(movies)), movie_counts.values,
                       color=plt.cm.Spectral(np.linspace(0, 1, len(movies))))
        ax5.set_yticks(range(len(movies)))
        ax5.set_yticklabels(movies)
        ax5.invert_yaxis()
        ax5.set_title('TOP 10 评论最多的电影', fontweight='bold')
        ax5.set_xlabel('评论数')
        ax5.grid(axis='x', alpha=0.3)

        plt.suptitle('影评数据分析综合仪表板', fontsize=18, fontweight='bold', y=0.995)
        plt.savefig(f'{self.output_dir}/11_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"     ✅ 保存: 11_comprehensive_dashboard.png")

        print("✅ 综合仪表板生成完成！")

    def generate_report(self):
        """
        生成分析报告
        """
        print("\n📝 生成分析报告...")

        # 添加总结
        self.report.append("## 六、分析总结\n")
        self.report.append("### 主要发现\n")
        self.report.append(f"1. **数据规模**: 共分析了 {len(self.df)} 条影评，涵盖 {self.df['Movie_Name'].nunique()} 部电影\n")
        self.report.append(f"2. **情感倾向**: 正面评论占比最高，达到 {(self.df['sentiment']=='正面').sum()/len(self.df)*100:.1f}%\n")
        self.report.append(f"3. **评分分布**: 平均评分 {self.df['Score'].mean():.2f}，中位数 {self.df['Score'].median():.2f}\n")
        self.report.append(f"4. **用户参与**: 平均每部电影获得 {len(self.df)/self.df['Movie_Name'].nunique():.0f} 条评论\n")
        self.report.append(f"5. **互动情况**: {(self.df['Like']>0).sum()} 条评论获得点赞，占比 {(self.df['Like']>0).sum()/len(self.df)*100:.1f}%\n\n")

        self.report.append("### 可视化图表清单\n")
        self.report.append("1. `01_sentiment_distribution.png` - 情感与星级分布\n")
        self.report.append("2. `02_score_distribution.png` - 评分分布直方图\n")
        self.report.append("3. `03_top_keywords.png` - 高频关键词柱状图\n")
        self.report.append("4. `04_wordcloud.png` - 词云图（全部/正面/负面）\n")
        self.report.append("5. `05_top_movies.png` - 热门电影排行榜\n")
        self.report.append("6. `06_likes_analysis.png` - 点赞数分析\n")
        self.report.append("7. `07_time_trend.png` - 年度趋势分析\n")
        self.report.append("8. `08_monthly_trend.png` - 月度趋势分析\n")
        self.report.append("9. `09_correlation_heatmap.png` - 相关性热力图\n")
        self.report.append("10. `10_scatter_matrix.png` - 散点图矩阵\n")
        self.report.append("11. `11_comprehensive_dashboard.png` - 综合仪表板\n\n")

        self.report.append("---\n")
        self.report.append("*本报告由影评数据挖掘系统自动生成*\n")

        # 保存报告
        report_path = f'{self.output_dir}/analysis_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.writelines(self.report)

        print(f"✅ 分析报告已保存: {report_path}")

    def _load_stopwords(self):
        """
        加载中文停用词表
        """
        # 常用中文停用词
        stopwords = set([
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
            '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
            '没有', '看', '好', '自己', '这', '那', '么', '为', '这个', '来',
            '个', '中', '大', '里', '可', '能', '但', '而', '与', '给', '对',
            '被', '从', '还', '让', '把', '又', '更', '吗', '时', '地', '得',
            '啊', '吧', '呢', '哦', '哈', '嗯', '呀', '啦', '嘛', '吗',
            '电影', '影片', '部', '片', '这部', '一部', '觉得', '感觉', '真的',
            '太', '挺', '特别', '非常', '十分', '比较', '还是', '已经', '就是',
            '可以', '所以', '如果', '虽然', '因为', '但是', '然后', '最后',
            '　', ' ', '\n', '\t', '\r'
        ])

        return stopwords

    def run(self):
        """
        运行完整分析流程
        """
        try:
            # 加载数据
            self.load_data()

            # 数据预处理
            self.preprocess_data()

            # 情感分析
            self.sentiment_analysis()

            # 关键词分析
            self.keyword_analysis()

            # 电影分析
            self.movie_analysis()

            # 时间趋势分析
            self.time_trend_analysis()

            # 相关性分析
            self.correlation_analysis()

            # 综合仪表板
            self.comprehensive_dashboard()

            # 生成报告
            self.generate_report()

            print("\n" + "=" * 60)
            print("🎉 所有分析任务完成！")
            print("=" * 60)
            print(f"\n📁 分析结果保存在目录: {self.output_dir}/")
            print(f"📊 共生成 11 张可视化图表")
            print(f"📄 分析报告: {self.output_dir}/analysis_report.md")
            print("\n感谢使用影评数据挖掘分析系统！")

        except Exception as e:
            print(f"\n❌ 分析过程中出现错误: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    # 数据文件路径
    data_path = 'data.xlsx'

    # 创建分析器实例
    analyzer = FilmReviewAnalyzer(data_path)

    # 运行分析
    analyzer.run()
