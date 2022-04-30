from Pipeline import *
import glob


class Pipeline:
    import Pipeline

    def __init__(self):
        print("Pipeline Initialized")

    def extract(self, source):
        return self.Pipeline.get_files(source)

    def position_tables(self, data):
        return self.Pipeline.create_position_tables(data)

    def best_team(self, source):
        return self.Pipeline.best_score_season(source)

    def load(self, files, names, destination):
        return self.Pipeline.load_data(files, names, destination)


if __name__ == "__main__":

    data = glob.glob(source)
    sort_data = sorted([i[8:19] for i in data])
    source = "../data/*.json"
    pipe = Pipeline()
    dfs = pipe.extract(source)
    make_tables = pipe.position_tables(dfs)
    best_team = pipe.best_team(source)

    pipe.load([best_team], ["Best_Team_By_Season"], "../reports/")
    pipe.load(make_tables, sort_data, "../reports/position_tables/")
    #print(make_tables)

