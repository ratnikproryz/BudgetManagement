import pandas as pd
from datetime import datetime
import time


class ExportCSVController:
    def __init__(self):
        self.df = pd.read_csv("./data/personal_transactions.csv")

    def export(self, page):
        if page == 0:
            data = self.df
        else:
            data = self.df[(page - 1) * 10 : 10 * (page)]

        filename = "./data/" + str(time.time()) + ".csv"
        return data, filename
