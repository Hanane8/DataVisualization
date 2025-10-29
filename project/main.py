#!/usr/bin/env python3
"""
Video Game Data Visualization Dashboard
Interactive Dash application for analyzing video game industry data.
"""

import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pickle

# Add user site-packages to path
import site
sys.path.append(site.getusersitepackages())

# Load processed data
def load_data():
    """Load all processed datasets."""
    data = {}
    try:
        data['charts'] = pd.read_pickle('processed_data/charts_merged.pkl')
        data['recent'] = pd.read_pickle('processed_data/recent_games.pkl')
        data['major_publishers'] = pd.read_pickle('processed_data/major_publishers.pkl')
        data['top_platforms'] = pd.read_pickle('processed_data/top_platforms.pkl')
        print("✓ Data loaded successfully")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Video Game Industry Dashboard"

# Load data
data = load_data()
if data is None:
    print("Failed to load data. Please run data preprocessing first.")
    sys.exit(1)

# Define color schemes
colors = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Helper functions for creating visualizations
def create_sales_by_region_chart(df):
    """Create regional sales distribution chart."""
    regional_sales = df[['na_sales', 'jp_sales', 'pal_sales', 'other_sales']].sum()
    
    fig = px.pie(
        values=regional_sales.values,
        names=['North America', 'Japan', 'PAL Region', 'Other Regions'],
        title="Sales Distribution by Region",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        font_size=12,
        showlegend=True,
        height=400
    )
    
    return fig

def create_platform_sales_chart(df):
    """Create platform sales comparison chart."""
    platform_sales = df.groupby('platform')['total_sales'].sum().sort_values(ascending=False).head(15)
    
    fig = px.bar(
        x=platform_sales.values,
        y=platform_sales.index,
        orientation='h',
        title="Top 15 Platforms by Total Sales",
        labels={'x': 'Total Sales (Millions)', 'y': 'Platform'},
        color=platform_sales.values,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'},
        font_size=12
    )
    
    return fig

def create_genre_trend_chart(df):
    """Create genre popularity over time chart."""
    # Get top 5 genres by total sales
    top_genres = df.groupby('genre')['total_sales'].sum().sort_values(ascending=False).head(5).index
    
    # Filter data for top genres and recent years
    genre_data = df[df['genre'].isin(top_genres) & (df['year'] >= 2000)]
    yearly_genre_sales = genre_data.groupby(['year', 'genre'])['total_sales'].sum().reset_index()
    
    fig = px.line(
        yearly_genre_sales,
        x='year',
        y='total_sales',
        color='genre',
        title="Top 5 Genres Sales Trend (2000-2024)",
        labels={'total_sales': 'Total Sales (Millions)', 'year': 'Year'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_layout(
        height=400,
        font_size=12,
        hovermode='x unified'
    )
    
    return fig

def create_publisher_analysis_chart(df):
    """Create publisher success analysis chart."""
    publisher_stats = df.groupby('publisher').agg({
        'total_sales': ['sum', 'mean', 'count'],
        'critic_score': 'mean'
    }).round(2)
    
    publisher_stats.columns = ['total_sales_sum', 'avg_sales_per_game', 'game_count', 'avg_critic_score']
    publisher_stats = publisher_stats[publisher_stats['game_count'] >= 10]  # Publishers with at least 10 games
    publisher_stats = publisher_stats.sort_values('total_sales_sum', ascending=False).head(15)
    
    fig = px.scatter(
        publisher_stats,
        x='game_count',
        y='avg_sales_per_game',
        size='total_sales_sum',
        color='avg_critic_score',
        hover_data=['total_sales_sum'],
        title="Publisher Success Analysis<br><sub>Size = Total Sales, Color = Avg Critic Score</sub>",
        labels={
            'game_count': 'Number of Games',
            'avg_sales_per_game': 'Average Sales per Game (Millions)',
            'avg_critic_score': 'Average Critic Score'
        },
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        height=500,
        font_size=12
    )
    
    return fig

def create_yearly_sales_chart(df):
    """Create yearly sales trend chart."""
    yearly_sales = df.groupby('year')['total_sales'].sum().reset_index()
    yearly_sales = yearly_sales[yearly_sales['year'] >= 1980]  # Focus on modern era
    
    fig = px.line(
        yearly_sales,
        x='year',
        y='total_sales',
        title="Video Game Industry Sales Trend (1980-2024)",
        labels={'total_sales': 'Total Sales (Millions)', 'year': 'Year'},
        color_discrete_sequence=[colors['primary']]
    )
    
    fig.update_layout(
        height=400,
        font_size=12,
        hovermode='x unified'
    )
    
    # Add trend line
    fig.add_scatter(
        x=yearly_sales['year'],
        y=yearly_sales['total_sales'],
        mode='lines',
        line=dict(dash='dash', color=colors['secondary']),
        name='Trend'
    )
    
    return fig

def create_top_games_table(df, n=20):
    """Create top games data table."""
    top_games = df.nlargest(n, 'total_sales')[['title', 'platform', 'genre', 'publisher', 'total_sales', 'critic_score']]
    
    return dash_table.DataTable(
        data=top_games.to_dict('records'),
        columns=[
            {"name": "Title", "id": "title"},
            {"name": "Platform", "id": "platform"},
            {"name": "Genre", "id": "genre"},
            {"name": "Publisher", "id": "publisher"},
            {"name": "Total Sales (M)", "id": "total_sales", "type": "numeric", "format": {"specifier": ".2f"}},
            {"name": "Critic Score", "id": "critic_score", "type": "numeric", "format": {"specifier": ".0f"}}
        ],
        style_cell={'textAlign': 'left', 'fontSize': 12},
        style_header={'backgroundColor': colors['primary'], 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        page_size=10,
        sort_action="native"
    )

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🎮 Video Game Industry Dashboard", className="text-center mb-4"),
            html.P("Interactive analysis of video game sales, platforms, genres, and market trends", 
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filters"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Platform:"),
                            dcc.Dropdown(
                                id='platform-filter',
                                options=[{'label': 'All Platforms', 'value': 'all'}] + 
                                       [{'label': p, 'value': p} for p in sorted(data['charts']['platform'].unique())],
                                value='all',
                                clearable=False
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Genre:"),
                            dcc.Dropdown(
                                id='genre-filter',
                                options=[{'label': 'All Genres', 'value': 'all'}] + 
                                       [{'label': g, 'value': g} for g in sorted(data['charts']['genre'].unique())],
                                value='all',
                                clearable=False
                            )
                        ], width=6)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Year Range:"),
                            dcc.RangeSlider(
                                id='year-range-slider',
                                min=int(data['charts']['year'].min()),
                                max=int(data['charts']['year'].max()),
                                value=[int(data['charts']['year'].min()), int(data['charts']['year'].max())],
                                marks={str(year): str(year) for year in range(int(data['charts']['year'].min()), int(data['charts']['year'].max())+1, 10)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ])
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Key Metrics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-games", className="card-title"),
                    html.P("Total Games", className="card-text")
                ])
            ], color="primary", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-sales", className="card-title"),
                    html.P("Total Sales (M)", className="card-text")
                ])
            ], color="success", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="avg-sales", className="card-title"),
                    html.P("Avg Sales per Game", className="card-text")
                ])
            ], color="info", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="platforms-count", className="card-title"),
                    html.P("Platforms", className="card-text")
                ])
            ], color="warning", outline=True)
        ], width=3)
    ], className="mb-4"),
    
    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='regional-sales-chart')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='platform-sales-chart')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='genre-trend-chart')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='yearly-sales-chart')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Publisher Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='publisher-analysis-chart')
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Top Games Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top Selling Games"),
                dbc.CardBody([
                    html.Div(id='top-games-table')
                ])
            ])
        ], width=12)
    ])
    
], fluid=True)

# Callbacks
@app.callback(
    [Output('total-games', 'children'),
     Output('total-sales', 'children'),
     Output('avg-sales', 'children'),
     Output('platforms-count', 'children'),
     Output('regional-sales-chart', 'figure'),
     Output('platform-sales-chart', 'figure'),
     Output('genre-trend-chart', 'figure'),
     Output('yearly-sales-chart', 'figure'),
     Output('publisher-analysis-chart', 'figure'),
     Output('top-games-table', 'children')],
    [Input('platform-filter', 'value'),
     Input('genre-filter', 'value'),
     Input('year-range-slider', 'value')]
)
def update_dashboard(platform_filter, genre_filter, year_range):
    """Update all dashboard components based on filters."""
    
    # Filter data
    filtered_data = data['charts'].copy()
    
    # Apply platform filter
    if platform_filter != 'all':
        filtered_data = filtered_data[filtered_data['platform'] == platform_filter]
    
    # Apply genre filter
    if genre_filter != 'all':
        filtered_data = filtered_data[filtered_data['genre'] == genre_filter]
    
    # Apply year range filter
    filtered_data = filtered_data[
        (filtered_data['year'] >= year_range[0]) & 
        (filtered_data['year'] <= year_range[1])
    ]
    
    # Calculate metrics
    total_games = len(filtered_data)
    total_sales = f"{filtered_data['total_sales'].sum():.1f}"
    avg_sales = f"{filtered_data['total_sales'].mean():.2f}"
    platforms_count = filtered_data['platform'].nunique()
    
    # Create visualizations
    regional_chart = create_sales_by_region_chart(filtered_data)
    platform_chart = create_platform_sales_chart(filtered_data)
    genre_chart = create_genre_trend_chart(filtered_data)
    yearly_chart = create_yearly_sales_chart(filtered_data)
    publisher_chart = create_publisher_analysis_chart(filtered_data)
    top_games_table = create_top_games_table(filtered_data)
    
    return (total_games, total_sales, avg_sales, platforms_count,
            regional_chart, platform_chart, genre_chart, yearly_chart,
            publisher_chart, top_games_table)

if __name__ == '__main__':
    print("Starting Video Game Industry Dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
