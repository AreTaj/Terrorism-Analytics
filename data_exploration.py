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
        * Generally speaking, anything that is more than 90% blank is probably not useful for this analysis

    Returns:
    The DataFrame with the columns dropped.
    """

    missing_values_per_column = df.isnull().sum() / len(df)
    columns_to_drop = missing_values_per_column[missing_values_per_column > threshold].index

    print(f"Dropping columns with more than {threshold * 100}% missing values:")
    for col in columns_to_drop:
        print(f"- {col}")

    df_dropped = df.drop(columns_to_drop, axis=1)

    """ 
    Drop any rows with blank values in nkill (number killed).
    Note that this does NOT drop rows with nkill = 0.
    """
    cleaned_df=df_dropped.dropna(subset=['nkill'])

    # Return a final cleaned dataframe
    return cleaned_df

""" Section: Load and Clean Data """
# Load original dataframe provided by globalterrorismdb.csv
gtdb_df = load_data()

# Clean data using function clean_data()
df_cleaned = clean_data(gtdb_df, 0.9)  # Drop columns with >90% missing values

""" Section: Data Exploration """
# Output all print statements to a file 'exploratory_output.txt'
with open('exploratory_output.txt', 'w') as f:
    original_stdout = sys.stdout
    sys.stdout = f

    # Print first five rows of df_cleaned
    print(df_cleaned.head(5), file=f)

    # Print dataframe shape
    print(df_cleaned.shape, file=f)

    """ Subsection: Multiple Numerical Histograms """

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

    """ Subsection: Examine nkill (death tolls) """
    print(df_cleaned['nkill'].describe())

    import seaborn as sns
    # Box plot
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=df_cleaned['nkill'])
    plt.title('Box Plot of Death Tolls')
    plt.xlabel('Deaths per Incident')
    plt.savefig('death_toll_boxplot.png')
    print(f"Plot saved to: death_toll_boxplot.png\n", file=f)

"""     import seaborn as sns
    # Visualize the distribution of obesity levels
    plt.figure(figsize=(18,6))
    sns.histplot(data=df_cleaned, x='nkill', kde=True, log_scale=True)
    plt.title('Distribution of Death Tolls')
    plt.xlabel('Deaths per Incident')
    plt.ylabel('Frequency')
    # Save the plot to a file (replace 'my_plot.png' with desired filename)
    plt.savefig('death_toll_histogram.png')
    print(f"Plot saved to: death_toll_histogram.png\n", file=f) """

sys.stdout = original_stdout