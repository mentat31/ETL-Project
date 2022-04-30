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


    indexed = add_index(seasons)

    tables = [pd.DataFrame() for x in range(len(seasons))]
    for i in seasons:
        index = [x.groups.keys() for x in seasons]
        #i.set_index(index)

    return index


test = create_position_tables(stage)


#def printer(group):
    #for name, group in group:
        #print(name)
        #print(group)

print(test)
#print(test.apply(lambda x: x.groups.keys()) )
