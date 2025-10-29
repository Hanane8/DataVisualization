#!/usr/bin/env python3
"""
Simple Data Exploration Script for Video Game Dataset Analysis
This script loads and explores all datasets for the CRISP-DM project.
"""

import os
import sys

# Add user site-packages to path
import site
sys.path.append(site.getusersitepackages())

# Try to import pandas, if not available, provide instructions
try:
    import pandas as pd
    import numpy as np
    print("✓ Pandas and NumPy are available")
except ImportError:
    print("❌ Pandas/NumPy not available. Please install with:")
    print("pip install --user pandas numpy")
    sys.exit(1)

def load_and_explore_datasets():
    """Load and explore all datasets."""
    print("=" * 80)
    print("VIDEO GAME DATASET EXPLORATION")
    print("=" * 80)
    
    # Check if data directory exists
    if not os.path.exists('data'):
        print("❌ Data directory not found!")
        return None
    
    datasets = {}
    
    # Load main datasets
    try:
        datasets['charts'] = pd.read_csv('data/vg_charts.csv')
        print(f"✓ Loaded vg_charts.csv: {datasets['charts'].shape}")
    except Exception as e:
        print(f"❌ Error loading vg_charts.csv: {e}")
        return None
    
    try:
        datasets['developers'] = pd.read_csv('data/vg_developers.csv')
        print(f"✓ Loaded vg_developers.csv: {datasets['developers'].shape}")
    except Exception as e:
        print(f"❌ Error loading vg_developers.csv: {e}")
    
    try:
        datasets['publishers'] = pd.read_csv('data/vg_publishers.csv')
        print(f"✓ Loaded vg_publishers.csv: {datasets['publishers'].shape}")
    except Exception as e:
        print(f"❌ Error loading vg_publishers.csv: {e}")
    
    try:
        datasets['geo_cities'] = pd.read_csv('data/vg_geo_cities.csv')
        print(f"✓ Loaded vg_geo_cities.csv: {datasets['geo_cities'].shape}")
    except Exception as e:
        print(f"❌ Error loading vg_geo_cities.csv: {e}")
    
    try:
        datasets['geo_countries'] = pd.read_csv('data/vg_geo_countries.csv')
        print(f"✓ Loaded vg_geo_countries.csv: {datasets['geo_countries'].shape}")
    except Exception as e:
        print(f"❌ Error loading vg_geo_countries.csv: {e}")
    
    return datasets

def analyze_charts_dataset(df):
    """Analyze the main charts dataset."""
    print("\n" + "=" * 60)
    print("VG_CHARTS DATASET ANALYSIS")
    print("=" * 60)
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\nColumns:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1:2d}. {col}")
    
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
    
    # Sales analysis
    sales_cols = ['na_sales', 'jp_sales', 'pal_sales', 'other_sales', 'total_sales']
    print(f"\nSales Statistics:")
    print(df[sales_cols].describe())
    
    # Top games by global sales
    print(f"\nTop 10 Games by Total Sales:")
    top_games = df.nlargest(10, 'total_sales')[['title', 'platform', 'genre', 'total_sales']]
    print(top_games)
    
    # Platform analysis
    print(f"\nTop 10 Platforms by Number of Games:")
    platform_counts = df['platform'].value_counts()
    print(platform_counts.head(10))
    
    # Genre analysis
    print(f"\nTop 10 Genres by Number of Games:")
    genre_counts = df['genre'].value_counts()
    print(genre_counts.head(10))
    
    # Publisher analysis
    print(f"\nTop 10 Publishers by Number of Games:")
    publisher_counts = df['publisher'].value_counts()
    print(publisher_counts.head(10))
    
    # Year analysis
    print(f"\nRelease Years Range:")
    # Extract year from release_date if it's a date string
    try:
        df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
        valid_years = df['year'].dropna()
        print(f"   {valid_years.min()} to {valid_years.max()}")
        print(f"\nGames per Year (Last 10 years):")
        year_counts = valid_years.value_counts().sort_index()
        print(year_counts.tail(10))
    except:
        print("Could not extract years from release_date")
    
    return {
        'shape': df.shape,
        'top_games': top_games,
        'platform_counts': platform_counts,
        'genre_counts': genre_counts,
        'publisher_counts': publisher_counts,
        'year_range': (valid_years.min(), valid_years.max()),
        'missing_values': missing_df
    }

def analyze_other_datasets(datasets):
    """Analyze other datasets."""
    print("\n" + "=" * 60)
    print("OTHER DATASETS ANALYSIS")
    print("=" * 60)
    
    for name, df in datasets.items():
        if name == 'charts':
            continue
            
        print(f"\n{name.upper()} Dataset:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Missing values: {df.isnull().sum().sum()}")
        print(f"  First few rows:")
        print(df.head(3))

def main():
    """Main function."""
    datasets = load_and_explore_datasets()
    
    if datasets is None:
        print("Failed to load datasets. Exiting.")
        return
    
    # Analyze charts dataset in detail
    charts_analysis = analyze_charts_dataset(datasets['charts'])
    
    # Analyze other datasets
    analyze_other_datasets(datasets)
    
    # Summary
    print("\n" + "=" * 60)
    print("EXPLORATION SUMMARY")
    print("=" * 60)
    print(f"Total datasets loaded: {len(datasets)}")
    print(f"Main dataset (charts) shape: {datasets['charts'].shape}")
    print(f"Total games in dataset: {len(datasets['charts'])}")
    # Extract year for date range
    charts_copy = datasets['charts'].copy()
    charts_copy['year'] = pd.to_datetime(charts_copy['release_date'], errors='coerce').dt.year
    valid_years = charts_copy['year'].dropna()
    print(f"Date range: {valid_years.min()} to {valid_years.max()}")
    print(f"Total platforms: {datasets['charts']['platform'].nunique()}")
    print(f"Total genres: {datasets['charts']['genre'].nunique()}")
    print(f"Total publishers: {datasets['charts']['publisher'].nunique()}")
    
    print("\n" + "=" * 60)
    print("BUSINESS QUESTIONS ANALYSIS")
    print("=" * 60)
    
    # Answer some business questions
    charts = datasets['charts']
    
    print("\n1. Most popular platform:")
    platform_sales = charts.groupby('platform')['total_sales'].sum().sort_values(ascending=False)
    print(f"   {platform_sales.index[0]} with {platform_sales.iloc[0]:.2f}M total sales")
    
    print("\n2. Most popular genre:")
    genre_sales = charts.groupby('genre')['total_sales'].sum().sort_values(ascending=False)
    print(f"   {genre_sales.index[0]} with {genre_sales.iloc[0]:.2f}M total sales")
    
    print("\n3. Regional sales distribution:")
    regional_totals = charts[['na_sales', 'jp_sales', 'pal_sales', 'other_sales']].sum()
    for region, total in regional_totals.items():
        print(f"   {region}: {total:.2f}M ({total/regional_totals.sum()*100:.1f}%)")
    
    print("\n4. Top selling game:")
    top_game = charts.loc[charts['total_sales'].idxmax()]
    print(f"   {top_game['title']} ({top_game['platform']}) - {top_game['total_sales']:.2f}M sales")
    
    print("\n5. Industry growth over time:")
    # Extract year from release_date
    charts['year'] = pd.to_datetime(charts['release_date'], errors='coerce').dt.year
    yearly_sales = charts.groupby('year')['total_sales'].sum().sort_index()
    print(f"   Peak year: {yearly_sales.idxmax()} with {yearly_sales.max():.2f}M sales")
    print(f"   Recent trend: {yearly_sales.tail(5).mean():.2f}M average (last 5 years)")

if __name__ == "__main__":
    main()
