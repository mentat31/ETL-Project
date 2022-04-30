import pandas as pd
import glob

# need cols = games played, wins, losses, draws, goals for/against/ & diff, points

patho = "../../data/*.json"
cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]


# convert_dates set to False in order to avoid formatting warning.


# Missing from data = "HHW", "AWH", "HO", "AO" ,"HBP", "ABP"
def clean_for_contex(func):
    data_dictionary = ["Div", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HTHG", "HTAG",
                       "HTR", "Referee", "HS", "AS", "HST", "AST", "HC", "AC", "HF", "AF",
                       "HY", "AY", "HR", "AR"]

    # data dict = keys to filter in extraction
    def wrapper(*args, **kwargs):
        get = func(*args, **kwargs)
        new_df = [i[data_dictionary] for i in get]
        return new_df

    return wrapper


def position_tables(df, columns):
    context_columns = [i[columns] for i in df]
    return context_columns

# def scoring_team_by_season()

# j = position_tables(dfs, cols)

# print(j)

def add_index(dataset):
    index = [i.groups.keys() for i in dataset]
    combine = list(zip(tables,index))
    for i in range(len(dataset)):
        tables[i].index = list(index[i])
    return tables


