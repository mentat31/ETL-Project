import pandas as pd

from scripts.helper_functions import *

source = "../data/*.json"


# convert_dates set to False in order to avoid formatting warning.
@clean_for_contex
def get_files(path):
    data = glob.glob(path)
    files = [pd.read_json(i, convert_dates=False) for i in data]
    return files


stage = get_files(source)


def create_position_tables(df):
    cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
    df = list(map(lambda x: x[cols], df))

    seasons = pd.Series((map(lambda x: x.groupby("HomeTeam"), df)))
    tables = [pd.DataFrame() for x in range(len(seasons))]

    indexed = add_index(seasons)
    columned = add_cols(indexed)
    t = transform(columned, stage)

    return t


def best_score_season(path):
    data = glob.glob(path)
    sort_data = sorted([i[8:19] for i in data])

    best_table = pd.DataFrame(index=sort_data)
    scores = create_position_tables(stage)

    for i in range(len(scores)):
        team = scores[i].index[0]
        season = sort_data[i]
        best_table.loc[season, "Team"] = team
        best_table.loc[season, "Goals"] = scores[i].loc[team, "Goals For"]

    return best_table


def load_data(files, names, destination):
    for i in range(len(files)):
        files[i].to_csv("{}{}.csv".format(destination, names[i]))

