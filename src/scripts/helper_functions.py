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



def add_index(dataset):
    tables = [pd.DataFrame() for x in range(len(dataset))]
    index = [i.groups.keys() for i in dataset]
    for i in range(len(dataset)):
        tables[i].index = list(index[i])
    return tables

def add_cols(dataset):
    tables = [pd.DataFrame() for x in range(len(dataset))]
    report_columns = ["Games", "Wins", "Losses", "Draws", "Goals For", "Goals Against", "Points"]
    for i in tables:
        i[report_columns] = 0
    return dataset


def transform(dataset,stage):
    for i in range(len(dataset)):
        teams = dataset[i].index

        for j in teams:
            home = stage[i][stage[i].HomeTeam == j]
            away = stage[i][stage[i].AwayTeam == j]
            games = len(home) + len(away)
            dataset[i].loc[j, "Games"] = games

            wins = len(home[home['FTR'] == "H"]) + len(away[away["FTR"] == "A"])
            dataset[i].loc[j, "Wins"] = wins

            losses = len(home[home['FTR'] == "A"]) + len(away[away["FTR"] == "H"])
            dataset[i].loc[j, "Losses"] = losses

            draws = len(home[home['FTR'] == "D"]) + len(away[away["FTR"] == "D"])
            dataset[i].loc[j, "Draws"] = draws

            goals_for = sum(home['FTHG']) + sum(away["FTAG"])
            dataset[i].loc[j, "Goals For"] = goals_for

            goals_against = sum(home['FTAG']) + sum(away["FTHG"])
            dataset[i].loc[j, "Goals Against"] = goals_against

            dataset[i].loc[j, "Goal Difference"] = dataset[i].loc[j, "Goals For"] - dataset[i].loc[j, "Goals Against"]

            dataset[i].loc[j, "Points"] = (dataset[i].loc[j, "Wins"] * 3) + dataset[i].loc[j, "Draws"]

    for data in dataset:
        data.sort_values(by="Points",inplace=True,ascending=False)
    return dataset


def best_score_season(path):
    data = glob.glob(path)
    data = sorted([i[11:22] for i in data])





