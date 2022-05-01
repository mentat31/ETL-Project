import pandas as pd
from scripts.helper_functions import *
from re import search
import glob


@clean_for_contex
def get_files(path):
    """
    Pull data from source's path. Convert_dates set to False in order to avoid formatting warning.

    :param path: path to pull files from.
    :return: list of pandas dataframes.
    """
    data = glob.glob(path)
    files = [pd.read_json(i, convert_dates=False) for i in data]
    return files


def create_position_tables(df):
    """
    Create Position Table for each season in df. List cols used to filter for required columns.

    :param df: Data from extract stage as List of Dataframes.
    :return: List of Position Tables of type Dataframe.
    """
    cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
    df = list(map(lambda x: x[cols], df))

    seasons = pd.Series((map(lambda x: x.groupby("HomeTeam"), df)))

    indexed = add_index(seasons)
    columned = add_cols(indexed)
    t = transform(columned, df)

    return t


def best_score_season(dfs):
    """
    Takes in extracted data and makes a call to create_position_tables. The format of the
    dataframes returned by create_position_tables makes computing the highest scoring team by season
    much easier as each team's goals are already aggregated.

    The original filename (season) is used to index this table.

    :param dfs: Extracted data.
    :return: Table indexed by season recording the highest scoring team and their Goals by season.
    """
    data = glob.glob("../data/*.json")
    sort_data = sorted([search(r"season-[0-9]*", i).group() for i in data])

    best_table = pd.DataFrame(index=sort_data)
    scores = create_position_tables(dfs)

    for i in range(len(scores)):
        team = scores[i].index[0]
        season = sort_data[i]
        best_table.loc[season, "Team"] = team
        best_table.loc[season, "Goals"] = scores[i].loc[team, "Goals For"]

    return best_table


def load_data(files, names, destination):
    """
    Load files to target.

    :param files: File/s to be loaded.
    :param names: Filenames
    :param destination: Target directory
    :return: File's written to destination as .csv.
    """
    for i in range(len(files)):
        files[i].to_csv("{}{}.csv".format(destination, names[i]))
