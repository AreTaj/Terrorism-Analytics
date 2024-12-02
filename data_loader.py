import pandas as pd

def load_data():
    gtdb_df = pd.read_csv('globalterrorismdb.csv', encoding='ISO-8859-1', low_memory=False)
    return gtdb_df

if __name__ == '__main__':
    gtdb_df = load_data()
    
    
    
    
    
    


""" import kagglehub

def download_dataset():
    # Download latest version
    path = kagglehub.dataset_download("START-UMD/gtd")
    print("Path to dataset files:", path)
    # /Users/Aresh/.cache/kagglehub/datasets/START-UMD/gtd/versions/3
    return path

dataset_path = download_dataset() """
