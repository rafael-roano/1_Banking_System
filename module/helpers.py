import pandas as pd

def csv_to_df(path):
    '''
    Read csv file into dataframe

    Returns:
        dataframe
         
    '''
    df = pd.read_csv(path)
        
    return df


 
def df_to_csv(df, path):
    ''' Save modifications in csv file from dataframe'''
        
    df.to_csv(path, index=False)