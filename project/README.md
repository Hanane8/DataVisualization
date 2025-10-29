# Video Game Industry Data Visualization Dashboard

## Project Overview

This project creates an interactive data visualization dashboard for analyzing the video game industry using the CRISP-DM methodology. The dashboard provides comprehensive insights into game sales, platform preferences, genre trends, and market dynamics across different regions and time periods.

## Business Context

**Company**: Mythic Realm Studios (Fictitious Gaming Company)  
**Objective**: Provide senior leadership with interactive tools to explore gaming industry trends and make data-driven decisions about game development and market strategies.

## Key Business Questions Addressed

1. Which regions prefer which platforms for playing video games?
2. What is the most popular platform for playing video games?
3. How do video game sales vary per release year in each region?
4. Which platforms have been most popular each release year?
5. Which regions prefer which genres the most?
6. What are the top three genres per region?
7. Which genres have been more or less popular over time?
8. Which publishers have consistent success vs. hit-or-miss performance?
9. Which region purchases the most video games?
10. Which titles sold the most worldwide?
11. Which release year had the highest sales, and is the industry growing?
12. Do any platforms specialize in particular genres?
13. What titles are popular in one region but flop in another?

## Dataset Information

### Main Dataset: VG_CHARTS
- **Size**: 64,016 games
- **Time Period**: 1971-2024
- **Key Attributes**: Game title, platform, genre, publisher, developer, sales data, critic scores
- **Regional Sales**: North America, Japan, PAL Region, Other Regions

### Supporting Datasets
- **VG_DEVELOPERS**: 731 developers with geographic information
- **VG_PUBLISHERS**: 889 publishers with geographic information  
- **VG_GEO_CITIES**: 23,412 cities with coordinates
- **VG_GEO_COUNTRIES**: 262 countries with coordinates and codes

## Project Structure

```
project/
├── data/                          # Raw datasets
│   ├── vg_charts.csv
│   ├── vg_developers.csv
│   ├── vg_publishers.csv
│   ├── vg_geo_cities.csv
│   ├── vg_geo_countries.csv
│   └── data_dictionary/           # Column descriptions
├── processed_data/                # Cleaned and processed datasets
│   ├── charts_merged.pkl         # Main analysis dataset
│   ├── recent_games.pkl          # Games from 2010+
│   ├── major_publishers.pkl      # Top publishers only
│   ├── top_platforms.pkl         # Major platforms only
│   └── summary_stats.pkl         # Dataset statistics
├── reports/                       # CRISP-DM documentation
│   ├── 1_BusinessUnderstanding.md
│   ├── 2_DataUnderstanding.md
│   ├── 3_DataPreparation.md
│   ├── 4_VisualizationAndAppDevelopment.md
│   ├── 5_Evaluation.md
│   └── 6_Deployment.md
├── main.py                       # Main Dash application
├── data_exploration.py           # Data exploration script
├── data_preprocessing.py         # Data cleaning and preparation
├── simple_exploration.py         # Simple data analysis
└── README.md                     # This file
```

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/paga-hb/C1VI1B_2025.git
cd C1VI1B_2025/project
```

### Step 2: Install Required Packages
```bash
pip install --user numpy pandas matplotlib seaborn plotly dash dash-bootstrap-components openpyxl lxml pycountry kaleido
```

### Step 3: Run Data Preprocessing
```bash
python data_preprocessing.py
```

### Step 4: Launch the Dashboard
```bash
python main.py
```

The dashboard will be available at: http://127.0.0.1:8050

## Dashboard Features

### Interactive Visualizations

1. **Regional Sales Distribution**
   - Pie chart showing sales distribution across North America, Japan, PAL Region, and Other Regions
   - Interactive hover information with exact values and percentages

2. **Platform Sales Analysis**
   - Horizontal bar chart of top 15 platforms by total sales
   - Color-coded by sales volume for easy comparison

3. **Genre Trends Over Time**
   - Line chart showing sales trends for top 5 genres from 2000-2024
   - Interactive legend to show/hide specific genres

4. **Yearly Sales Trend**
   - Line chart showing industry growth from 1980-2024
   - Includes trend line for pattern analysis

5. **Publisher Success Analysis**
   - Scatter plot analyzing publisher performance
   - X-axis: Number of games published
   - Y-axis: Average sales per game
   - Size: Total sales volume
   - Color: Average critic score

6. **Top Selling Games Table**
   - Sortable data table with top 20 games
   - Columns: Title, Platform, Genre, Publisher, Total Sales, Critic Score
   - Pagination for easy navigation

### Interactive Filters

- **Platform Filter**: Dropdown to filter by specific gaming platforms
- **Genre Filter**: Dropdown to filter by game genres
- **Year Range Slider**: Select specific time periods for analysis

### Key Metrics Cards

- **Total Games**: Number of games in filtered dataset
- **Total Sales**: Sum of all sales in millions
- **Average Sales per Game**: Mean sales across all games
- **Platforms**: Number of unique platforms

## Technical Implementation

### Data Processing Pipeline

1. **Data Loading**: Load raw CSV files from data directory
2. **Data Cleaning**: Handle missing values, standardize formats
3. **Data Merging**: Combine game data with geographic information
4. **Feature Engineering**: Create derived attributes (year, decade, platform generation)
5. **Data Validation**: Verify data consistency and completeness

### Dashboard Architecture

- **Frontend**: Dash with Bootstrap components for responsive design
- **Backend**: Python with Plotly for interactive visualizations
- **Data Storage**: Pickle files for fast loading and processing
- **State Management**: Dash callbacks for real-time updates

### Performance Optimizations

- Pre-processed datasets for fast loading
- Efficient data filtering and aggregation
- Responsive design for various screen sizes
- Optimized chart rendering with Plotly

## Usage Instructions

### Basic Navigation

1. **Open the Dashboard**: Navigate to http://127.0.0.1:8050
2. **Apply Filters**: Use the filter panel to narrow down your analysis
3. **Explore Visualizations**: Click and hover on charts for detailed information
4. **Sort Tables**: Click column headers in the top games table to sort
5. **Reset Filters**: Select "All" options to reset filters

### Analysis Workflows

**Regional Analysis**:
1. Use the regional sales pie chart to understand market distribution
2. Apply platform/genre filters to see regional preferences
3. Use year range slider to analyze trends over time

**Platform Analysis**:
1. Review the platform sales bar chart for overall performance
2. Filter by specific platforms to see detailed breakdowns
3. Use the publisher analysis to understand platform success factors

**Genre Analysis**:
1. Examine the genre trends chart for popularity over time
2. Filter by specific genres to see platform preferences
3. Use the top games table to identify successful genre examples

**Publisher Analysis**:
1. Use the publisher scatter plot to identify successful publishers
2. Filter by publisher to see their game portfolio
3. Analyze the relationship between critic scores and sales

## Key Findings

### Market Insights

- **North America** dominates with 50.7% of total sales
- **PS2** is the most successful platform by sales volume (1,027.76M)
- **PC** has the most games released (12,617)
- **Sports** genre leads in total sales (1,187.51M)
- **2008** was the peak year for industry sales (538.11M)

### Business Recommendations

1. **Focus on North American Market**: Highest sales potential
2. **Multi-Platform Strategy**: Games on multiple platforms show strong performance
3. **Genre Diversification**: Action and Sports genres show consistent success
4. **Quality Matters**: Higher critic scores correlate with better sales
5. **Recent Trends**: Industry has declined since 2008 peak

## Data Quality Notes

- **Missing Sales Data**: 70-89% of games have missing regional sales data
- **Unknown Publishers**: 13.8% of games have unknown publisher information
- **Data Completeness**: Geographic and temporal data is highly complete
- **Validation**: Sales data has been validated for consistency

## Troubleshooting

### Common Issues

1. **Module Not Found Error**:
   - Ensure all packages are installed: `pip install --user [package_name]`
   - Check Python path includes user site-packages

2. **Data Loading Error**:
   - Run data preprocessing first: `python data_preprocessing.py`
   - Ensure processed_data directory exists

3. **Dashboard Not Loading**:
   - Check if port 8050 is available
   - Try different port: modify `app.run_server(port=8051)`

4. **Performance Issues**:
   - Close other applications to free memory
   - Use filters to reduce dataset size

### Getting Help

- Check the console output for error messages
- Verify all dependencies are installed correctly
- Ensure data preprocessing completed successfully
- Review the CRISP-DM reports for detailed analysis

## Project Deliverables

### Code Files
- `main.py`: Complete Dash application
- `data_preprocessing.py`: Data cleaning and preparation
- `data_exploration.py`: Comprehensive data analysis
- `simple_exploration.py`: Basic data exploration

### Documentation
- `README.md`: This comprehensive guide
- `reports/`: Complete CRISP-DM documentation
- Data dictionaries for all datasets

### Processed Data
- Cleaned and merged datasets in pickle format
- Specialized datasets for different analysis types
- Summary statistics and metadata

## Future Enhancements

### Potential Improvements
1. **Real-time Data Updates**: Connect to live data sources
2. **Advanced Filtering**: More granular filter options
3. **Export Functionality**: Download charts and data
4. **User Authentication**: Multi-user support
5. **Mobile Optimization**: Enhanced mobile experience
6. **Machine Learning**: Predictive analytics for sales forecasting

### Additional Visualizations
1. **Geographic Maps**: Publisher/developer location maps
2. **Correlation Matrix**: Feature relationship analysis
3. **Box Plots**: Sales distribution analysis
4. **Heatmaps**: Platform-genre performance matrices
5. **Network Graphs**: Publisher-developer relationships

## License

This project is part of the Data Visualization course (C1VI1B) at Borås University.

## Contact

For questions about this project, please refer to the course documentation or contact the project team.

---

**Note**: This dashboard is designed for educational purposes and demonstrates the application of CRISP-DM methodology to real-world data visualization challenges in the gaming industry.
