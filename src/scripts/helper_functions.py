import pandas as pd
import glob

# need cols = games played, wins, losses, draws, goals for/against/ & diff, points

patho = "../../data/*.json"
cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]


def get_files(path):
    data = glob.glob(path)
    files = map(pd.read_json, data)
    return list(files)


def clean_for_contex(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


dfs = get_files(patho)


@clean_for_contex
def reports_data(df, columns):
    context_columns = [i[columns] for i in df]
    return context_columns

j = reports_data(dfs,cols)

print(j)





