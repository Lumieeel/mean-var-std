import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

DATAFILE = "fcc-forum-pageviews.csv"  # cambia si tu CSV tiene otro nombre

def draw_line_plot():
    # Load data
    df = pd.read_csv(DATAFILE, parse_dates=['date'], index_col='date')

    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Load data
    df = pd.read_csv(DATAFILE, parse_dates=['date'], index_col='date')

    # Prepare data for monthly bar plot: average page views per month grouped by year
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Group by year and month and compute mean
    grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Rename columns to month names ordered Jan..Dec
    month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
    grouped.columns = month_names

    # Plot grouped bar chart
    fig = grouped.plot(kind='bar', figsize=(15,7)).figure
    plt.xlabel('Year')
    plt.ylabel('Average Page Views')
    plt.legend(title='Month')
    plt.tight_layout()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Load data
    df = pd.read_csv(DATAFILE, parse_dates=['date'], index_col='date')

    # Clean the data: remove extreme outliers outside 2.5th-97.5th percentiles
    low = df['value'].quantile(0.025)
    high = df['value'].quantile(0.975)
    df_clean = df[(df['value'] >= low) & (df['value'] <= high)].copy()

    # Prepare data for box plots
    df_clean.reset_index(inplace=True)
    df_clean['year'] = df_clean['date'].dt.year
    df_clean['month'] = df_clean['date'].dt.strftime('%b')  # abbreviated month name
    df_clean['month_num'] = df_clean['date'].dt.month

    # Sort by month number so month order is Jan..Dec
    df_clean = df_clean.sort_values('month_num')

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16,6))

    sns.boxplot(ax=axes[0], x='year', y='value', data=df_clean)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(ax=axes[1], x='month', y='value', data=df_clean,
                order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()
    fig.savefig('box_plot.png')
    return fig

# If run directly, produce all three plots
if __name__ == "__main__":
    print("Generando gráficos...")
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()
    print("Se guardaron line_plot.png, bar_plot.png y box_plot.png")
