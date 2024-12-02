import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from data_loader import load_data

def column_dropper(df, threshold):
    """
    Drops columns from a DataFrame that have more than the specified threshold of missing values.

    Args:
    df: The DataFrame to process.
    threshold: The maximum allowed percentage of missing values (0-1).

    Returns:
    The DataFrame with the columns dropped.
    """

    missing_values_per_column = df.isnull().sum() / len(df)
    columns_to_drop = missing_values_per_column[missing_values_per_column > threshold].index

    print(f"Dropping columns with more than {threshold * 100}% missing values:")
    for col in columns_to_drop:
        print(f"- {col}")

    return df.drop(columns_to_drop, axis=1)

with open('output.txt', 'w') as f:
    original_stdout = sys.stdout
    sys.stdout = f

    # Load original dataframe created in data_loader.py
    gtdb_df = load_data()

    df_cleaned = column_dropper(gtdb_df, 0.9)  # Drop columns with >90% missing values

    # Print first five rows of df_cleaned
    print(df_cleaned.head(5), file=f)

    # Print dataframe shape
    print(df_cleaned.shape, file=f)

    """ Section: Explore Data """

    # Select numerical columns
    numerical_columns = df_cleaned.select_dtypes(include='number').columns

    # Create individual box plots for each numerical column of data
    fig, axes = plt.subplots(nrows=int(np.ceil(len(numerical_columns) / 4)), ncols=4, figsize=(12, 8))

    for i, column in enumerate(numerical_columns):
        row, col = i // 4, i % 4
        axes[row, col].boxplot(df_cleaned[column])
        axes[row, col].set_title(column)

    plt.tight_layout()

    # Save the plot to a file (replace 'my_plot.png' with desired filename)
    plt.savefig('my_plot.png')
    print(f"Plot saved to: my_plot.png\n", file=f)

sys.stdout = original_stdout