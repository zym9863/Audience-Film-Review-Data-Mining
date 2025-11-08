[中文](README.md) | [English](README-EN.md)

# Audience Film Review Data Mining System - User Guide

## Project Overview

This project provides a comprehensive data mining and analytics system for audience film reviews. It is built on top of more than 510,000 real reviews and delivers multi-dimensional insights such as sentiment analysis, keyword mining, trend analysis, and automatic generation of polished visualization charts.

---

## System Features

### Core Modules

1. **Sentiment Analysis**
   - Classifies review sentiment (positive/neutral/negative) based on star ratings
   - Visualizes the sentiment distribution
   - Explores the relationship between rating and sentiment

2. **Keyword Mining**
   - Collects the top 50 high-frequency words
   - Compares positive and negative word clouds
   - Extracts key topics with TF-IDF

3. **Movie Insights**
   - Lists the top 10 most discussed titles
   - Visualizes score distributions
   - Analyzes likes and engagement metrics

4. **Temporal Trends**
   - Displays annual review counts
   - Tracks monthly sentiment changes
   - Builds a score time series analysis

5. **Correlation Analysis**
   - Generates a feature correlation heatmap
   - Creates a scatter plot matrix
   - Cross-analyzes sentiment vs. star rating

6. **Comprehensive Dashboard**
   - Presents a multi-dimensional data overview
   - Exports more than 11 visualization charts with one click

---

## Getting Started

### Prerequisites

- **Operating System**: Windows, Linux, or macOS
- **Python**: 3.8 or newer
- **Memory**: At least 4 GB recommended (large dataset)

### Installation

#### Option 1: Virtual Environment (strongly recommended)

**Windows users:**

1. **Create the virtual environment and install dependencies**
   ```bash
   Double-click setup_venv.bat
   ```

2. **Run the analysis (activates the virtual environment automatically)**
   ```bash
   Double-click run_analysis_venv.bat
   ```

**Activate the virtual environment manually:**
```bash
Double-click activate_venv.bat
# Or run in Command Prompt
venv\Scripts\activate.bat
```

**Linux/macOS users:**

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate  # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the analysis
python film_review_analysis.py

# 5. Deactivate the virtual environment
deactivate
```

#### Option 2: Global Installation

**Windows users:**

1. **Install dependencies**
   ```bash
   Double-click install_dependencies.bat
   ```

2. **Run the analysis**
   ```bash
   Double-click run_analysis.bat
   ```

**Linux/macOS users:**

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the analysis**
   ```bash
   python film_review_analysis.py
   ```

---

## File Structure

```
project-root/
│
├── data.xlsx                      # Raw review dataset (510k+ records)
├── film_review_analysis.py        # Main analysis script
├── requirements.txt               # Python dependency list
│
├── setup_venv.bat                 # Recommended virtual environment setup script
├── activate_venv.bat              # Virtual environment activation helper
├── run_analysis_venv.bat          # Run analysis inside the virtual environment
│
├── install_dependencies.bat       # Windows dependency installer (global)
├── run_analysis.bat               # Windows runner (global)
├── README.md                      # Chinese documentation
│
├── venv/                          # Virtual environment directory (created by setup_venv.bat)
│
└── analysis_results/              # Generated outputs
    ├── 01_sentiment_distribution.png      # Sentiment and star distribution
    ├── 02_score_distribution.png          # Score histogram
    ├── 03_top_keywords.png                # High-frequency keywords
    ├── 04_wordcloud.png                   # All/positive/negative word clouds
    ├── 05_top_movies.png                  # Top 10 movies summary
    ├── 06_likes_analysis.png              # Likes analysis
    ├── 07_time_trend.png                  # Yearly trend
    ├── 08_monthly_trend.png               # Monthly trend
    ├── 09_correlation_heatmap.png         # Correlation heatmap
    ├── 10_scatter_matrix.png              # Scatter matrix
    ├── 11_comprehensive_dashboard.png     # Dashboard
    └── analysis_report.md                 # Analysis report
```

---

## Output Overview

### Visualization Charts (11 total)

| No. | File | Description |
|-----|------|-------------|
| 1 | `01_sentiment_distribution.png` | Distribution of user ratings and sentiment (pie chart) |
| 2 | `02_score_distribution.png` | Rating histogram with mean and median lines |
| 3 | `03_top_keywords.png` | Top 30 keyword bar chart |
| 4 | `04_wordcloud.png` | Combined word clouds (all/positive/negative) |
| 5 | `05_top_movies.png` | Top 10 movie ranking by review count and rating |
| 6 | `06_likes_analysis.png` | Likes box plot and log-scale distribution |
| 7 | `07_time_trend.png` | Yearly review count and rating/star trends |
| 8 | `08_monthly_trend.png` | Monthly review volume and positive rate trend |
| 9 | `09_correlation_heatmap.png` | Feature correlation and sentiment-star heatmap |
| 10 | `10_scatter_matrix.png` | 4x4 feature scatter matrix |
| 11 | `11_comprehensive_dashboard.png` | Comprehensive analytics dashboard |

### Analysis Report

- **Filename**: `analysis_report.md`
- **Format**: Markdown, viewable in any text editor
- **Contents**:
  - Data overview
  - Sentiment distribution statistics
  - Top 20 keywords
  - Top 10 movies details
  - Trend analysis
  - Correlation analysis
  - Key findings summary

---

## Tech Stack

| Category | Libraries | Purpose |
|----------|-----------|---------|
| Data processing | pandas, numpy | Data loading, cleaning, and statistics |
| Chinese tokenization | jieba | Segmentation and keyword extraction |
| Visualization | matplotlib, seaborn | Chart generation |
| Word cloud | wordcloud | Word cloud rendering |
| Machine learning | scikit-learn | TF-IDF and topic extraction |
| File handling | openpyxl | Excel I/O |

---

## Customization

### Change the Output Directory

Edit line 40 in `film_review_analysis.py`:

```python
self.output_dir = "analysis_results"  # Override with your preferred directory
```

### Adjust Chart Styles

Modify the plotting configuration around lines 18-22:

```python
plt.rcParams['font.sans-serif'] = ['SimHei']  # Update the font family
sns.set_style("whitegrid")  # Options: whitegrid, darkgrid, white, dark
sns.set_palette("husl")     # Update the color palette
```

### Customize Stop Words

Update the `_load_stopwords()` method (lines 616-632) to add or remove stop words.

---

## Tips and Tricks

### 1. Large Datasets

For datasets exceeding one million rows:
- Increase available memory
- Sample the data: `self.df = self.df.sample(100000)`

### 2. Custom Analysis Scope

Comment out unneeded modules inside `run()`:

```python
# self.correlation_analysis()  # Skip correlation analysis when not required
```

### 3. Fix Word Cloud Fonts

Update the font path around line 391 if characters render incorrectly:

```python
font_path='C:/Windows/Fonts/simhei.ttf',  # Windows
# font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # Linux
```

---

## Frequently Asked Questions

### Issue 1: Dependency Installation Fails

**Fix**:
```bash
# Use a mirror in mainland China
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Issue 2: Word Cloud Shows Garbled Text

**Fix**:
- Windows: ensure the SimHei font is installed
- Linux: install `sudo apt-get install fonts-wqy-zenhei`
- macOS: install a Chinese font manually

### Issue 3: Insufficient Memory

**Fix**:
- Use sampling to reduce the dataset size
- Close other memory-intensive applications
- Process the data in batches

### Issue 4: Blurry Charts

**Fix**:
Increase the `dpi` in `savefig()` (default is 300):
```python
plt.savefig('xxx.png', dpi=600)  # Raise to 600 for clarity
```

---

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| ID | int | Unique identifier |
| Movie_Name | str | Movie title |
| Score | float | Douban rating (0-10) |
| Review_People | int | Total number of reviews |
| Star_Distribution | str | Star rating distribution |
| Craw_Date | datetime | Data crawl date |
| Username | str | Reviewer username |
| Date | datetime | Review publish date |
| Star | int | User star rating (1-5) |
| Comment | str | Review content |
| Comment_Distribution | str | Comment distribution |
| Like | int | Like count |

---

## Sample Console Output

```
============================================================
Audience Film Review Data Mining System Started
============================================================

Loading data...
Data loaded: 515315 records, 12 columns

Data overview:
  - Movies: 871
  - Reviews: 515315
  - Users: 172763
  - Time span: 2005-06-12 to 2019-10-15

Running preprocessing...
  - Handling missing values...
  - Calculating review length...
  - Assigning sentiment labels...
  - Extracting time features...
Preprocessing completed

Running sentiment analysis...
  - Saving 01_sentiment_distribution.png
  - Saving 02_score_distribution.png
Sentiment analysis completed

... (additional output)

============================================================
All analysis tasks completed
============================================================

Results are located in: analysis_results/
Generated charts: 11
Report: analysis_results/analysis_report.md
```

---

## Contributing and Feedback

Issues and suggestions are always welcome.

---

## License

For learning and research use only.

---

Enjoy exploring the data!
