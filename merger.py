import pandas as pd
from os import listdir, getcwd
import sqlite3, sys

#input path to the csvs and gets the current working directory
path_to_files = input("Path to files: ")
cwd = getcwd()

#search in the directory for all .csv files, returns a list
def find_csv(path=path_to_files, suffix=".csv"):
    files = listdir(path)
    return[file for file in files if file.endswith(suffix)]

#confirmation
def ask_merge():
    print(f"Found {len(files)} CSV files, ready to be merged\n")
    ask = input("Do you want to continue? [y/n]")
    if ask.lower() == "y": return
    else: exit()

#appends every file in a dataframe
def merge_files(files):
    dataframe = []
    for file in files:
        df = pd.read_csv(f"{path_to_files}/{file}", sep=";", low_memory=False)
        dataframe.append(df)
    return(pd.concat(dataframe, ignore_index=True))

files = find_csv(path_to_files)

ask_merge()

dataframe = merge_files(files)
print(f"\nDataframe preview:\n{dataframe}")

#creating a sqlite3 connection and cursor
conn = sqlite3.connect("Machine data")
c = conn.cursor()

#assigns the column names of the dataframe to a string, to create a SQL command
headers = dataframe.columns
headers_string = ", ".join(headers)

c.execute(f"CREATE TABLE IF NOT EXISTS Machine_data ({headers_string})")
conn.commit()

#inserts the pandas dataframe to the SQL database
dataframe.to_sql("Machine_data", conn, if_exists="replace", index=False)

c.execute(
    """  
    SELECT * FROM Machine_data
    """
)

print("\n--- CSV files merged succesfully ---\n")