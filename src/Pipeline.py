from scripts.helper_functions import *

source = "../data/*.json"


# convert_dates set to False in order to avoid formatting warning.
@clean_for_contex
def get_files(path):
    data = glob.glob(path)
    files = [pd.read_json(i, convert_dates=False) for i in data]
    return files


stage = get_files(source)


# need cols = games played, wins, losses, draws, goals for/against/ & diff, points
def create_position_tables(df):
    cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
    df = list(map(lambda x: x[cols], df))

    seasons = pd.Series((map(lambda x: x.groupby("HomeTeam"), df)))
    tables = [pd.DataFrame() for x in range(len(seasons))]

    indexed = add_index(seasons)
    columned = add_cols(indexed)

    t = transform(columned,stage)

    return t

test = create_position_tables(stage)


print(test)
