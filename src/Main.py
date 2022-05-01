from Pipeline import *
import glob
from datetime import datetime
from re import search


class Pipeline:
    import Pipeline

    def __init__(self):
        print("Starting Pipeline")

    def extract(self, source):
        now = datetime.now()
        print("{}: Extracting from {}".format(now, source))
        return self.Pipeline.get_files(source)

    def position_tables(self, data):
        now = datetime.now()
        print("{}: Creating Position Tables".format(now))
        return self.Pipeline.create_position_tables(data)

    def best_team(self, source):
        now = datetime.now()
        print("{}: Creating Best Scoring Team by Season".format(now))
        return self.Pipeline.best_score_season(source)

    def load(self, files, names, destination):
        now = datetime.now()
        print("{}: Loading {} to {}".format(now, names, destination))
        return self.Pipeline.load_data(files, names, destination)


if __name__ == "__main__":
    source = "../data/*.json"
    data = glob.glob(source)
    sort_data = sorted([search(r"season-[0-9]*", i).group() for i in data])
    pipe = Pipeline()
    dfs = pipe.extract(source)
    make_tables = pipe.position_tables(dfs)
    best_team = pipe.best_team(dfs)

    pipe.load([best_team], ["Best_Team_By_Season"], "../reports/")
    pipe.load(make_tables, sort_data, "../reports/")
