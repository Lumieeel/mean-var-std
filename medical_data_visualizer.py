import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def draw_cat_plot():
    # Load data
    df = pd.read_csv('medical_examination.csv')

    # Add 'overweight' column
    bmi = df['weight'] / ((df['height'] / 100) ** 2)
    df['overweight'] = (bmi > 25).astype(int)

    # Normalize data: 0 = good, 1 = bad
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # Create DataFrame for cat plot using `pd.melt`
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # Group and reformat the data to split it by `cardio`. Needed for the catplot
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # Draw the catplot with seaborn
    sns.set_style("whitegrid")
    fig = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar',
        height=5,
        aspect=1
    ).fig

    # Save figure
    fig.savefig('catplot.png')

    return fig

def draw_heat_map():
    # Load data
    df = pd.read_csv('medical_examination.csv')

    # Add 'overweight' column
    bmi = df['weight'] / ((df['height'] / 100) ** 2)
    df['overweight'] = (bmi > 25).astype(int)

    # Normalize data
    df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
    df['gluc'] = (df['gluc'] > 1).astype(int)

    # Clean the data
    df_clean = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ].copy()

    # Calculate the correlation matrix
    corr = df_clean.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw the heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        linewidths=.5,
        square=True,
        cbar_kws={"shrink": .5},
        ax=ax
    )

    # Save figure
    fig.savefig('heatmap.png')

    return fig

# If run as script, produce both plots
if __name__ == "__main__":
    draw_cat_plot()
    draw_heat_map()
    print("catplot.png and heatmap.png saved.")
