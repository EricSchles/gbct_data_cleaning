import pandas as pd
from valid_headers import column_names
        
def check_columns(df,filename):
    headers = column_names[filename]
    cur_headers = [str(key) for key in df.keys()]
    if headers != cur_headers:
        return False
    else:
        return True

def check_filename(filename):
    try:
        column_names[filename]
        return True
    except KeyError:
        return False
    
def validate(filename):
    #checks if extension type is valid
    if filename.endswith(".csv"):
        return pd.read_csv(filename)
    elif filename.endswith(".xls"):
        return pd.read_excel(filename)
    elif filename.endswith(".xlsx"):
        return pd.read_excel(filename)
    else:
        return "invalid file extension"

def perform_checks(filename,local_file):
    if not check_filename(filename):
        return "filename does not exist in our records"
    df = validate(local_file)
    if type(df) == type(str()):
        return "file does not have an extension this program can work with, please use .xlsx, .xls, or .csv"
    if not check_columns(df,filename):
        return "columns do not match our records for this file"
    else:
        return "no error"
