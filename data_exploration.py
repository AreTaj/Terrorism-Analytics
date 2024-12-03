import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_data():
    gtdb_df = pd.read_csv('globalterrorismdb.csv', encoding='ISO-8859-1', low_memory=False)
    return gtdb_df

def clean_data(df, threshold):
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

    cleaned_df = df.drop(columns_to_drop, axis=1)
    return cleaned_df

with open('exploratory_output.txt', 'w') as f:
    original_stdout = sys.stdout
    sys.stdout = f

    # Load original dataframe
    gtdb_df = load_data()

    df_cleaned = clean_data(gtdb_df, 0.9)  # Drop columns with >90% missing values

    # Print first five rows of df_cleaned
    print(df_cleaned.head(5), file=f)

    # Print dataframe shape
    print(df_cleaned.shape, file=f)

    """ Section: Explore Data """

    # Select numerical columns
    numerical_columns = df_cleaned.select_dtypes(include='number').columns

    # Create individual histograms for each numerical column of data
    fig, axes = plt.subplots(nrows=int(np.ceil(len(numerical_columns) / 4)), ncols=4, figsize=(20, 30))

    for i, column in enumerate(numerical_columns):
        row, col = i // 4, i % 4
        axes[row, col].hist(df_cleaned[column])  # Histograms
        axes[row, col].set_title(column)
        axes[row, col].set_xlabel(column)  # Add x-axis label for clarity
        axes[row, col].set_ylabel('Frequency')  # Add y-axis label

    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.8, wspace=0.5)  # Increase vertical and horizontal spacing

    # Save the plot to a file (replace 'my_plot.png' with desired filename)
    plt.savefig('histograms.png')
    print(f"Plot saved to: histograms.png\n", file=f)

sys.stdout = original_stdout