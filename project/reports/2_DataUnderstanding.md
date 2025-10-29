
---

# Phase: Data Understanding

## Task: Collect Initial Data

### Output: Initial Data Collection Report

The initial data has already been collected, and is stored in the `data` folder together with the *data dictionary* (i.e. descriptions or each column/feature in each dataset) in the `data/data_dictionary` folder.

The datasets are:
- `vg_charts.csv`
- `vg_developers.csv`
- `vg_publishers.csv`
- `vg_geo_cities.csv`
- `vg_geo_countries.csv`

## Task: Describe Data

### Output: Data Description Report

The following datasets have been acquired and analyzed for this project:

#### 1. VG_CHARTS Dataset (Main Dataset)
- **Format**: CSV file with comma-separated values
- **Size**: 64,016 records (rows) × 14 fields (columns)
- **Memory Usage**: 32.73 MB
- **Date Range**: 1971 to 2024
- **Fields**:
  - `img`: URL slug for box art images (56,177 unique values)
  - `title`: Game title (39,798 unique values)
  - `platform`: Gaming platform (81 unique values)
  - `genre`: Game genre (20 unique values)
  - `publisher`: Game publisher (3,383 unique values)
  - `developer`: Game developer (8,862 unique values)
  - `critic_score`: Metacritic critic score (89 unique values)
  - `total_sales`: Total worldwide sales in millions (482 unique values)
  - `na_sales`: North American sales in millions (320 unique values)
  - `jp_sales`: Japanese sales in millions (121 unique values)
  - `pal_sales`: PAL region sales in millions (256 unique values)
  - `other_sales`: Other regions sales in millions (133 unique values)
  - `release_date`: Game release date (7,922 unique values)
  - `last_update`: Last update timestamp (1,545 unique values)

#### 2. VG_DEVELOPERS Dataset
- **Format**: CSV file
- **Size**: 731 records × 3 fields
- **Fields**: developer, city, country
- **Missing Values**: 5 total

#### 3. VG_PUBLISHERS Dataset
- **Format**: CSV file
- **Size**: 889 records × 3 fields
- **Fields**: publisher, city, country
- **Missing Values**: 148 total

#### 4. VG_GEO_CITIES Dataset
- **Format**: CSV file
- **Size**: 23,412 records × 3 fields
- **Fields**: city, latitude, longitude
- **Missing Values**: 0

#### 5. VG_GEO_COUNTRIES Dataset
- **Format**: CSV file
- **Size**: 262 records × 5 fields
- **Fields**: Country, Alpha-2 code, Alpha-3 code, Latitude, Longitude
- **Missing Values**: 0

#### Data Sufficiency Assessment
The acquired data satisfies the project requirements as it contains:
- Comprehensive game information covering 53 years (1971-2024)
- Regional sales data for all major markets
- Platform, genre, and publisher information
- Geographic data for mapping visualizations
- Sufficient volume (64K+ games) for meaningful analysis

The data is adequate for answering all business questions outlined in the project objectives.

## Task: Explore Data

### Output: Data Exploration Report

#### Key Findings from Data Analysis

**1. Sales Distribution Analysis**
- **Total Sales Volume**: 6,601.41M units across all regions
- **Regional Distribution**:
  - North America: 3,345.52M (50.7%) - Largest market
  - PAL Region: 1,916.83M (29.0%) - Second largest
  - Japan: 687.94M (10.4%) - Third largest
  - Other Regions: 651.12M (9.9%) - Smallest market

**2. Platform Analysis**
- **Most Popular Platform by Volume**: PS2 with 1,027.76M total sales
- **Most Games Released**: PC with 12,617 games
- **Top Platforms by Game Count**: PC (12,617), PS2 (3,565), DS (3,288), PS4 (2,878)

**3. Genre Analysis**
- **Most Popular Genre by Sales**: Sports with 1,187.51M total sales
- **Most Games Released**: Misc (9,304), Action (8,557), Adventure (6,260)
- **Genre Diversity**: 20 distinct genres represented

**4. Publisher Analysis**
- **Top Publishers by Game Count**: Unknown (8,842), Sega (2,207), Ubisoft (1,663)
- **Major Publishers**: Electronic Arts, Activision, Nintendo, Sony Computer Entertainment
- **Publisher Diversity**: 3,383 unique publishers

**5. Temporal Analysis**
- **Peak Year**: 2008 with 538.11M sales
- **Recent Trend**: Declining sales in recent years (2020-2024 average: 0.69M)
- **Historical Coverage**: 53 years of data (1971-2024)

**6. Top Performing Games**
- **Best Selling Game**: Grand Theft Auto V (PS3) - 20.32M sales
- **Top 10 Games**: Dominated by Grand Theft Auto and Call of Duty franchises
- **Platform Distribution**: Multi-platform releases show strong performance

#### Business Questions Addressed

**Q1: Which regions prefer which platform?**
- North America: Strong preference for PlayStation platforms (PS2, PS4)
- Japan: Strong preference for Nintendo platforms (DS, NS)
- PAL Region: Balanced distribution across platforms

**Q2: What is the most popular platform?**
- By sales volume: PS2 (1,027.76M sales)
- By game count: PC (12,617 games)

**Q3: How do sales vary by release year?**
- Peak in 2008 (538.11M sales)
- General decline since 2008
- Recent years show significant drop-off

**Q4: Which genres are most popular?**
- By sales: Sports (1,187.51M)
- By game count: Misc, Action, Adventure

**Q5: Which publishers have consistent success?**
- Major publishers: Electronic Arts, Activision, Nintendo
- Many games have "Unknown" publisher (data quality issue)

#### Data Quality Observations
- High percentage of missing sales data (70-89% missing)
- Significant number of games with "Unknown" publisher
- Some missing developer information
- Date format inconsistencies in release_date field

#### Impact on Project
These findings will inform:
1. **Data Cleaning Strategy**: Focus on handling missing sales data
2. **Visualization Design**: Prioritize platforms and genres with sufficient data
3. **Business Insights**: North American market dominance, platform preferences
4. **App Functionality**: Filter capabilities for platforms, genres, and time periods

## Task: Verify Data Quality

### Output: Data Quality Report

#### Data Completeness Assessment

**VG_CHARTS Dataset (Main Dataset)**
- **Total Records**: 64,016 games
- **Missing Values Analysis**:
  - `critic_score`: 57,338 missing (89.57%) - Very high missing rate
  - `total_sales`: 45,094 missing (70.44%) - High missing rate
  - `na_sales`: 51,379 missing (80.26%) - Very high missing rate
  - `jp_sales`: 57,290 missing (89.49%) - Very high missing rate
  - `pal_sales`: 51,192 missing (79.97%) - Very high missing rate
  - `other_sales`: 48,888 missing (76.37%) - High missing rate
  - `release_date`: 7,051 missing (11.01%) - Moderate missing rate
  - `last_update`: 46,137 missing (72.07%) - High missing rate
  - `developer`: 17 missing (0.03%) - Very low missing rate

**Other Datasets**
- **VG_DEVELOPERS**: 5 missing values total (0.68%)
- **VG_PUBLISHERS**: 148 missing values total (16.6%)
- **VG_GEO_CITIES**: 0 missing values (100% complete)
- **VG_GEO_COUNTRIES**: 0 missing values (100% complete)

#### Data Correctness Assessment

**Identified Issues**:
1. **Publisher Data**: 8,842 games (13.8%) have "Unknown" publisher - indicates data collection issues
2. **Sales Data**: High missing rates suggest incomplete sales tracking
3. **Date Format**: `release_date` field contains mixed formats and some invalid dates
4. **Duplicate Games**: Same game titles appear multiple times (likely different platforms/versions)

#### Data Quality Problems and Solutions

**Problem 1: High Missing Sales Data**
- **Impact**: Limits analysis capabilities for regional sales trends
- **Solution**: 
  - Focus analysis on games with complete sales data
  - Use imputation for games with partial sales data
  - Create separate visualizations for games with complete vs. incomplete data

**Problem 2: Unknown Publishers**
- **Impact**: Reduces publisher analysis accuracy
- **Solution**:
  - Filter out "Unknown" publishers for publisher-specific analysis
  - Create separate category for unknown publishers
  - Focus on major known publishers for detailed analysis

**Problem 3: Date Format Inconsistencies**
- **Impact**: Temporal analysis challenges
- **Solution**:
  - Standardize date formats during data preparation
  - Extract year information for temporal analysis
  - Handle invalid dates appropriately

**Problem 4: Duplicate Game Entries**
- **Impact**: Potential double-counting in analysis
- **Solution**:
  - Identify and handle duplicate entries
  - Consider aggregating sales across platforms for same game
  - Create platform-specific vs. game-specific views

#### Data Sufficiency for Business Objectives

**Adequate Data Areas**:
- Platform analysis (81 platforms, good distribution)
- Genre analysis (20 genres, comprehensive coverage)
- Temporal analysis (53 years of data)
- Geographic analysis (complete country/city data)

**Limited Data Areas**:
- Regional sales analysis (high missing rates)
- Publisher analysis (many unknown publishers)
- Critic score analysis (89% missing)

#### Recommendations for Data Preparation

1. **Data Cleaning Priority**:
   - Handle missing sales data (imputation or filtering)
   - Standardize date formats
   - Address unknown publishers

2. **Data Transformation**:
   - Create year column from release_date
   - Aggregate sales data appropriately
   - Handle duplicate game entries

3. **Analysis Strategy**:
   - Focus on games with complete sales data for regional analysis
   - Use platform/genre analysis as primary focus
   - Create multiple views for different data completeness levels

The data quality issues are manageable and will not prevent successful completion of the project objectives, but require careful handling during the data preparation phase.