import pandas as pd


# columns to build reports = games played, wins, losses, draws, goals for/against/ & diff, points


# Missing from data but included in Dictionary = "HHW", "AWH", "HO", "AO" ,"HBP", "ABP"
def clean_for_contex(func):
    """
    Decorator for extract stage. Data dictionary defined for future reuse looking
    into other columns. Columns missing in data that were included in dictionary:
    HHW, AWH, HO, AO, HBP, ABP, Attendance

    :param func: function to pull data.
    :return: Dataset filtered by data_dictionary
    """
    data_dictionary = ["Div", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HTHG", "HTAG",
                       "HTR", "Referee", "HS", "AS", "HST", "AST", "HC", "AC", "HF", "AF",
                       "HY", "AY", "HR", "AR"]

    # data dict = keys to filter in extraction
    def wrapper(*args, **kwargs):
        get = func(*args, **kwargs)
        new_df = [i[data_dictionary] for i in get]
        return new_df

    return wrapper


def add_index(dataset):
    """
    Creates list of new Dataframe's to use for position tables. Group original data
    by HomeTeam, and set as index in corresponding dataframe

    :param dataset: Original data grouped by HomeTeam
    :return: List of new Dataframe's indexed by team.
    """
    tables = [pd.DataFrame() for _ in range(len(dataset))]
    index = [i.groups.keys() for i in dataset]
    for i in range(len(dataset)):
        tables[i].index = list(index[i])
    return tables


def add_cols(dataset):
    """
    Adds columns in each Dataframe specific to position table in EPL. Frame's
    filled with 0 to avoid Exception.

    :param dataset: List output of function add_columns
    :return: List of DataFrames indexed by team with new columns.
    """
    tables = [pd.DataFrame() for _ in range(len(dataset))]
    report_columns = ["Games", "Wins", "Losses", "Draws", "Goals For", "Goals Against", "Points"]
    for i in tables:
        i[report_columns] = 0
    return dataset


def transform(dataset, stage):
    """
    Takes in list of newly indexed and columned dataframes, as well as extracted data.
    Function iterates through new data's index (teams) and original data filtered by team.

    When filtering by team, a subset of the data is selected, representing when the team
    was both home and away to represent the full season.

    EPL Position Tables use columns: Games Played, Wins, Losses, Draws, Goals For/Against & diff, and Points.

    While goals and points appear to represent the same concept, they are slightly different.
    The English Premier League uses a point system; 3 points for a win, 1 point for a draw, 0 for
    a loss to determine the winning team.

    :param dataset:Output of add_index/cols.
    :param stage:Original extracted data.
    :return:List of Position Tables sorted by Points column.
    """
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
        data.sort_values(by="Points", inplace=True, ascending=False)
    return dataset
