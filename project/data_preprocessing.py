#!/usr/bin/env python3
"""
Data Preprocessing Script for Video Game Dataset Analysis
This script cleans and preprocesses all datasets for the CRISP-DM project.
"""

import os
import sys

# Add user site-packages to path
import site
sys.path.append(site.getusersitepackages())

import pandas as pd
import numpy as np
import pickle

def load_datasets():
    """Load all raw datasets."""
    print("Loading datasets...")
    datasets = {}
    
    datasets['charts'] = pd.read_csv('data/vg_charts.csv')
    datasets['developers'] = pd.read_csv('data/vg_developers.csv')
    datasets['publishers'] = pd.read_csv('data/vg_publishers.csv')
    datasets['geo_cities'] = pd.read_csv('data/vg_geo_cities.csv')
    datasets['geo_countries'] = pd.read_csv('data/vg_geo_countries.csv')
    
    print(f"✓ Loaded {len(datasets)} datasets")
    return datasets

def clean_charts_data(df):
    """Clean and preprocess the main charts dataset."""
    print("\nCleaning VG_CHARTS dataset...")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # 1. Handle release_date - extract year
    print("  - Processing release dates...")
    df_clean['release_date_clean'] = pd.to_datetime(df_clean['release_date'], errors='coerce')
    df_clean['year'] = df_clean['release_date_clean'].dt.year
    
    # 2. Handle missing sales data
    print("  - Processing sales data...")
    # Fill missing sales with 0 (assuming no sales if missing)
    sales_cols = ['na_sales', 'jp_sales', 'pal_sales', 'other_sales', 'total_sales']
    df_clean[sales_cols] = df_clean[sales_cols].fillna(0)
    
    # 3. Handle missing critic scores
    print("  - Processing critic scores...")
    df_clean['critic_score'] = df_clean['critic_score'].fillna(0)
    
    # 4. Clean text fields
    print("  - Cleaning text fields...")
    text_cols = ['title', 'platform', 'genre', 'publisher', 'developer']
    for col in text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace('nan', 'Unknown')
    
    # 5. Create derived features
    print("  - Creating derived features...")
    
    # Total sales verification (should match sum of regional sales)
    df_clean['calculated_total'] = (df_clean['na_sales'] + 
                                   df_clean['jp_sales'] + 
                                   df_clean['pal_sales'] + 
                                   df_clean['other_sales'])
    
    # Sales completeness indicator
    df_clean['has_complete_sales'] = (
        df_clean['na_sales'].notna() & 
        df_clean['jp_sales'].notna() & 
        df_clean['pal_sales'].notna() & 
        df_clean['other_sales'].notna()
    )
    
    # Decade classification
    df_clean['decade'] = (df_clean['year'] // 10) * 10
    
    # Platform generation
    platform_generations = {
        'PS': '5th Gen', 'PS2': '6th Gen', 'PS3': '7th Gen', 'PS4': '8th Gen', 'PS5': '9th Gen',
        'XBOX': '6th Gen', 'X360': '7th Gen', 'XOne': '8th Gen', 'XS': '9th Gen',
        'N64': '5th Gen', 'GC': '6th Gen', 'Wii': '7th Gen', 'WiiU': '8th Gen', 'NS': '8th Gen',
        'GB': '4th Gen', 'GBA': '6th Gen', 'DS': '7th Gen', '3DS': '8th Gen',
        'PC': 'PC', 'MAC': 'PC', 'LIN': 'PC'
    }
    df_clean['platform_generation'] = df_clean['platform'].map(platform_generations).fillna('Other')
    
    print(f"  ✓ Cleaned dataset: {df_clean.shape}")
    return df_clean

def clean_other_datasets(datasets):
    """Clean other datasets."""
    print("\nCleaning other datasets...")
    
    cleaned = {}
    
    # Clean developers dataset
    if 'developers' in datasets:
        print("  - Cleaning developers dataset...")
        df_dev = datasets['developers'].copy()
        df_dev['developer'] = df_dev['developer'].astype(str).str.strip()
        df_dev['city'] = df_dev['city'].fillna('Unknown')
        df_dev['country'] = df_dev['country'].fillna('Unknown')
        cleaned['developers'] = df_dev
    
    # Clean publishers dataset
    if 'publishers' in datasets:
        print("  - Cleaning publishers dataset...")
        df_pub = datasets['publishers'].copy()
        df_pub['publisher'] = df_pub['publisher'].astype(str).str.strip()
        df_pub['city'] = df_pub['city'].fillna('Unknown')
        df_pub['country'] = df_pub['country'].fillna('Unknown')
        cleaned['publishers'] = df_pub
    
    # Geo datasets are already clean
    cleaned['geo_cities'] = datasets['geo_cities']
    cleaned['geo_countries'] = datasets['geo_countries']
    
    return cleaned

def merge_datasets(charts_clean, other_datasets):
    """Merge datasets for enhanced analysis."""
    print("\nMerging datasets...")
    
    # Merge with developers
    charts_merged = charts_clean.copy()
    if 'developers' in other_datasets:
        charts_merged = charts_merged.merge(
            other_datasets['developers'], 
            on='developer', 
            how='left',
            suffixes=('', '_dev')
        )
        print("  ✓ Merged with developers data")
    
    # Merge with publishers
    if 'publishers' in other_datasets:
        charts_merged = charts_merged.merge(
            other_datasets['publishers'], 
            on='publisher', 
            how='left',
            suffixes=('', '_pub')
        )
        print("  ✓ Merged with publishers data")
    
    # Merge with geo data for publishers
    if 'geo_countries' in other_datasets:
        geo_countries = other_datasets['geo_countries'].copy()
        # Clean country names for merging
        geo_countries['Country'] = geo_countries['Country'].str.strip().str.replace('"', '')
        charts_merged = charts_merged.merge(
            geo_countries, 
            left_on='country_pub', 
            right_on='Country', 
            how='left',
            suffixes=('', '_geo')
        )
        print("  ✓ Merged with geographic data")
    
    print(f"  ✓ Final merged dataset: {charts_merged.shape}")
    return charts_merged

def create_analysis_datasets(df_merged):
    """Create specialized datasets for different types of analysis."""
    print("\nCreating analysis datasets...")
    
    analysis_datasets = {}
    
    # 1. Complete sales data only
    complete_sales = df_merged[df_merged['has_complete_sales']].copy()
    analysis_datasets['complete_sales'] = complete_sales
    print(f"  ✓ Complete sales dataset: {complete_sales.shape}")
    
    # 2. Recent games (2010+)
    recent_games = df_merged[df_merged['year'] >= 2010].copy()
    analysis_datasets['recent_games'] = recent_games
    print(f"  ✓ Recent games dataset: {recent_games.shape}")
    
    # 3. Major publishers only
    major_publishers = ['Electronic Arts', 'Activision', 'Nintendo', 'Sony Computer Entertainment', 
                       'Microsoft', 'Ubisoft', 'Sega', 'Konami']
    major_pub_games = df_merged[df_merged['publisher'].isin(major_publishers)].copy()
    analysis_datasets['major_publishers'] = major_pub_games
    print(f"  ✓ Major publishers dataset: {major_pub_games.shape}")
    
    # 4. Top platforms only
    top_platforms = ['PC', 'PS2', 'PS3', 'PS4', 'X360', 'XOne', 'NS', 'DS', '3DS']
    top_platform_games = df_merged[df_merged['platform'].isin(top_platforms)].copy()
    analysis_datasets['top_platforms'] = top_platform_games
    print(f"  ✓ Top platforms dataset: {top_platform_games.shape}")
    
    return analysis_datasets

def save_processed_data(charts_clean, charts_merged, analysis_datasets, other_datasets):
    """Save all processed datasets."""
    print("\nSaving processed data...")
    
    # Create processed data directory
    os.makedirs('processed_data', exist_ok=True)
    
    # Save main datasets
    charts_clean.to_pickle('processed_data/charts_clean.pkl')
    charts_merged.to_pickle('processed_data/charts_merged.pkl')
    print("  ✓ Saved main processed datasets")
    
    # Save analysis datasets
    for name, df in analysis_datasets.items():
        df.to_pickle(f'processed_data/{name}.pkl')
    print("  ✓ Saved analysis datasets")
    
    # Save other datasets
    for name, df in other_datasets.items():
        df.to_pickle(f'processed_data/{name}_clean.pkl')
    print("  ✓ Saved other cleaned datasets")
    
    # Save summary statistics
    summary_stats = {
        'original_shape': charts_clean.shape,
        'merged_shape': charts_merged.shape,
        'complete_sales_count': len(analysis_datasets['complete_sales']),
        'recent_games_count': len(analysis_datasets['recent_games']),
        'major_publishers_count': len(analysis_datasets['major_publishers']),
        'top_platforms_count': len(analysis_datasets['top_platforms']),
        'year_range': (charts_clean['year'].min(), charts_clean['year'].max()),
        'platforms_count': charts_clean['platform'].nunique(),
        'genres_count': charts_clean['genre'].nunique(),
        'publishers_count': charts_clean['publisher'].nunique()
    }
    
    with open('processed_data/summary_stats.pkl', 'wb') as f:
        pickle.dump(summary_stats, f)
    print("  ✓ Saved summary statistics")

def main():
    """Main preprocessing function."""
    print("=" * 80)
    print("DATA PREPROCESSING FOR VIDEO GAME DATASET ANALYSIS")
    print("=" * 80)
    
    # Load raw datasets
    datasets = load_datasets()
    
    # Clean main charts dataset
    charts_clean = clean_charts_data(datasets['charts'])
    
    # Clean other datasets
    other_datasets_clean = clean_other_datasets(datasets)
    
    # Merge datasets
    charts_merged = merge_datasets(charts_clean, other_datasets_clean)
    
    # Create analysis datasets
    analysis_datasets = create_analysis_datasets(charts_merged)
    
    # Save all processed data
    save_processed_data(charts_clean, charts_merged, analysis_datasets, other_datasets_clean)
    
    # Print summary
    print("\n" + "=" * 60)
    print("PREPROCESSING SUMMARY")
    print("=" * 60)
    print(f"Original dataset: {datasets['charts'].shape}")
    print(f"Cleaned dataset: {charts_clean.shape}")
    print(f"Merged dataset: {charts_merged.shape}")
    print(f"Complete sales games: {len(analysis_datasets['complete_sales'])}")
    print(f"Recent games (2010+): {len(analysis_datasets['recent_games'])}")
    print(f"Major publisher games: {len(analysis_datasets['major_publishers'])}")
    print(f"Top platform games: {len(analysis_datasets['top_platforms'])}")
    print(f"Year range: {charts_clean['year'].min()} - {charts_clean['year'].max()}")
    print(f"Platforms: {charts_clean['platform'].nunique()}")
    print(f"Genres: {charts_clean['genre'].nunique()}")
    print(f"Publishers: {charts_clean['publisher'].nunique()}")
    
    print("\n✓ Data preprocessing completed successfully!")
    print("✓ All processed datasets saved to 'processed_data/' directory")

if __name__ == "__main__":
    main()
