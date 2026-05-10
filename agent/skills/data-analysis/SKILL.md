---
name: data-analysis
description: Statistical analysis, data processing, and visualization for structured and semi-structured data
triggers: Analyze data, process dataset, generate statistics, visualize data, data transformation
version: 1.0
---

# Data Analysis Skill

Perform systematic data analysis from ingestion through insight generation with statistical validation.

## Core Workflow

### Phase 1: Data Ingestion & Profiling
1. **Format Detection**: Identify data format (CSV, JSON, TSV, log files, markdown tables)
2. **Structure Analysis**:
   - Row/column counts
   - Data types per column
   - Missing value percentages
   - Unique value counts
3. **Quality Assessment**:
   - Duplicate detection
   - Outlier identification (IQR method: Q1-1.5*IQR, Q3+1.5*IQR)
   - Inconsistency flags (mixed formats, typos)

### Phase 2: Statistical Analysis
1. **Descriptive Statistics**:
   - Mean, median, mode for numerical data
   - Frequency distributions for categorical data
   - Standard deviation, variance, range
   - Percentile rankings (25th, 50th, 75th, 90th, 95th)
2. **Correlation Analysis**:
   - Pearson correlation for linear relationships
   - Spearman rank correlation for monotonic relationships
   - Identify multicollinearity (r > 0.8)
3. **Trend Detection**:
   - Moving averages (7-day, 30-day)
   - Growth rates (MoM, YoY)
   - Seasonality patterns

### Phase 3: Data Transformation
1. **Cleaning Operations**:
   - Handle missing values (drop/fill with mean/median/mode)
   - Normalize/standardize numerical columns
   - Encode categorical variables
   - Parse datetime fields
2. **Feature Engineering**:
   - Create derived columns (ratios, differences, aggregations)
   - Bin numerical data into categories
   - Extract time-based features (day_of_week, month, quarter)
3. **Aggregation**:
   - GroupBy operations with multiple aggregations
   - Pivot tables for multi-dimensional analysis
   - Rolling windows for time series

### Phase 4: Insight Generation
1. **Key Findings**:
   - Top/bottom N items by metric
   - Significant changes (>2σ from mean)
   - Emerging patterns or trends
2. **Segmentation**:
   - Natural groupings in data
   - Cohort analysis
   - Comparative analysis (before/after, A/B groups)
3. **Anomaly Detection**:
   - Statistical outliers (>3σ)
   - Unexpected zero/negative values
   - Sudden spikes or drops

### Phase 5: Visualization Recommendations
Generate ASCII/text-based visualizations or descriptions for:
- Distribution histograms
- Time series line charts
- Correlation heatmaps (text matrix)
- Bar charts for categorical comparisons
- Box plots for outlier detection

## Output Format

```
## Data Analysis Report: <dataset_name>

### Dataset Profile
- Records: <count>
- Columns: <count> (<numerical>, <categorical>, <datetime>)
- Missing Values: <percentage>%
- Duplicates: <count>

### Key Statistics
<table of descriptive stats>

### Top Findings
1. <Finding with supporting numbers>
2. <Finding with supporting numbers>
3. <Finding with supporting numbers>

### Correlations
<strongest positive relationship>
<strongest negative relationship>

### Anomalies
<list of statistical outliers with context>

### Recommendations
- <actionable insight based on data>
- <further analysis suggestion>
```

## Tools Used
- `list_files.sh` for dataset discovery
- `read_file` for data inspection
- `get_date.sh` for timestamp generation
- Shell utilities: `awk`, `sort`, `uniq`, `wc`, `cut`, `grep`
- Python one-liners for statistical operations (if available)

## Processing Rules
- ALWAYS show sample data before analysis
- NEVER assume data quality -- validate first
- HANDLE missing data explicitly (don't silently drop)
- FLAG statistical significance vs practical significance
- PRESERVE original data (work on copies/transforms)
- EXPLAIN statistical concepts in plain language
