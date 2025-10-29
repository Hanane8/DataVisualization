#!/usr/bin/env python3
"""
Data Exploration Script for Video Game Dataset Analysis
This script loads and explores all datasets for the CRISP-DM project.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set pandas display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def load_datasets():
    """Load all datasets and return them as a dictionary."""
    datasets = {}
    
    # Load main datasets
    datasets['charts'] = pd.read_csv('data/vg_charts.csv')
    datasets['developers'] = pd.read_csv('data/vg_developers.csv')
    datasets['publishers'] = pd.read_csv('data/vg_publishers.csv')
    datasets['geo_cities'] = pd.read_csv('data/vg_geo_cities.csv')
    datasets['geo_countries'] = pd.read_csv('data/vg_geo_countries.csv')
    
    # Load data dictionaries
    datasets['charts_dict'] = pd.read_csv('data/data_dictionary/vg_charts.csv')
    datasets['developers_dict'] = pd.read_csv('data/data_dictionary/vg_developers.csv')
    datasets['publishers_dict'] = pd.read_csv('data/data_dictionary/vg_publishers.csv')
    datasets['geo_cities_dict'] = pd.read_csv('data/data_dictionary/vg_geo_cities.csv')
    datasets['geo_countries_dict'] = pd.read_csv('data/data_dictionary/vg_geo_countries.csv')
    
    return datasets

def analyze_dataset(df, name):
    """Analyze a single dataset and print comprehensive information."""
    print(f"\n{'='*60}")
    print(f"DATASET: {name.upper()}")
    print(f"{'='*60}")
    
    print(f"\nShape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\nData Types:")
    print(df.dtypes)
    
    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct
    })
    print(missing_df[missing_df['Missing Count'] > 0])
    
    print(f"\nUnique Values per Column:")
    unique_counts = df.nunique()
    print(unique_counts)
    
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    print(f"\nBasic Statistics for Numeric Columns:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())
    
    return {
        'shape': df.shape,
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,
        'missing_values': missing_df,
        'unique_counts': unique_counts,
        'numeric_columns': numeric_cols.tolist()
    }

def explore_charts_data(df):
    """Specific exploration for the main charts dataset."""
    print(f"\n{'='*60}")
    print("DETAILED ANALYSIS: VG_CHARTS")
    print(f"{'='*60}")
    
    # Sales analysis
    sales_cols = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales', 'global_sales']
    print(f"\nSales Statistics:")
    print(df[sales_cols].describe())
    
    # Top games by global sales
    print(f"\nTop 10 Games by Global Sales:")
    top_games = df.nlargest(10, 'global_sales')[['name', 'platform', 'genre', 'global_sales']]
    print(top_games)
    
    # Platform analysis
    print(f"\nPlatform Distribution:")
    platform_counts = df['platform'].value_counts()
    print(platform_counts.head(10))
    
    # Genre analysis
    print(f"\nGenre Distribution:")
    genre_counts = df['genre'].value_counts()
    print(genre_counts.head(10))
    
    # Publisher analysis
    print(f"\nTop Publishers by Number of Games:")
    publisher_counts = df['publisher'].value_counts()
    print(publisher_counts.head(10))
    
    # Year analysis
    print(f"\nRelease Years Range:")
    print(f"From {df['year'].min()} to {df['year'].max()}")
    print(f"Games per year (top 10):")
    year_counts = df['year'].value_counts().sort_index()
    print(year_counts.tail(10))
    
    return {
        'top_games': top_games,
        'platform_counts': platform_counts,
        'genre_counts': genre_counts,
        'publisher_counts': publisher_counts,
        'year_range': (df['year'].min(), df['year'].max()),
        'year_counts': year_counts
    }

def create_exploratory_visualizations(df_charts):
    """Create exploratory visualizations for the charts dataset."""
    print(f"\n{'='*60}")
    print("CREATING EXPLORATORY VISUALIZATIONS")
    print(f"{'='*60}")
    
    # 1. Sales distribution by region
    fig1 = px.box(df_charts, 
                  y=['na_sales', 'eu_sales', 'jp_sales', 'other_sales'],
                  title="Sales Distribution by Region",
                  labels={'value': 'Sales (millions)', 'variable': 'Region'})
    fig1.show()
    
    # 2. Top platforms by number of games
    platform_counts = df_charts['platform'].value_counts().head(15)
    fig2 = px.bar(x=platform_counts.index, y=platform_counts.values,
                 title="Top 15 Platforms by Number of Games",
                 labels={'x': 'Platform', 'y': 'Number of Games'})
    fig2.show()
    
    # 3. Genre popularity over time
    genre_year = df_charts.groupby(['year', 'genre']).size().reset_index(name='count')
    top_genres = df_charts['genre'].value_counts().head(5).index
    genre_year_top = genre_year[genre_year['genre'].isin(top_genres)]
    
    fig3 = px.line(genre_year_top, x='year', y='count', color='genre',
                   title="Top 5 Genres Popularity Over Time",
                   labels={'count': 'Number of Games', 'year': 'Release Year'})
    fig3.show()
    
    # 4. Global sales vs critic score
    fig4 = px.scatter(df_charts.dropna(subset=['critic_score']), 
                      x='critic_score', y='global_sales',
                      title="Global Sales vs Critic Score",
                      labels={'critic_score': 'Critic Score', 'global_sales': 'Global Sales (millions)'},
                      opacity=0.6)
    fig4.show()
    
    # 5. Regional sales comparison
    regional_sales = df_charts[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum()
    fig5 = px.pie(values=regional_sales.values, names=regional_sales.index,
                  title="Total Sales Distribution by Region")
    fig5.show()
    
    return fig1, fig2, fig3, fig4, fig5

def main():
    """Main function to run the data exploration."""
    print("Starting Data Exploration for Video Game Dataset Analysis")
    print("=" * 80)
    
    # Load datasets
    datasets = load_datasets()
    
    # Analyze each dataset
    analysis_results = {}
    for name, df in datasets.items():
        if not name.endswith('_dict'):  # Skip data dictionaries for now
            analysis_results[name] = analyze_dataset(df, name)
    
    # Detailed analysis of charts data
    charts_analysis = explore_charts_data(datasets['charts'])
    
    # Create visualizations
    print("\nCreating exploratory visualizations...")
    try:
        create_exploratory_visualizations(datasets['charts'])
        print("Visualizations created successfully!")
    except Exception as e:
        print(f"Error creating visualizations: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("EXPLORATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total datasets loaded: {len([k for k in datasets.keys() if not k.endswith('_dict')])}")
    print(f"Main dataset (charts) shape: {datasets['charts'].shape}")
    print(f"Total games in dataset: {len(datasets['charts'])}")
    print(f"Date range: {datasets['charts']['year'].min()}-{datasets['charts']['year'].max()}")
    print(f"Total platforms: {datasets['charts']['platform'].nunique()}")
    print(f"Total genres: {datasets['charts']['genre'].nunique()}")
    print(f"Total publishers: {datasets['charts']['publisher'].nunique()}")
    
    return datasets, analysis_results, charts_analysis

if __name__ == "__main__":
    datasets, analysis_results, charts_analysis = main()
