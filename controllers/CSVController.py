import pandas as pd
import time
from flask_paginate import Pagination


class CSVController:
    def __init__(self):
        self.df = pd.read_csv("./data/personal_transactions.csv")

    def index(self, page, category):
        header = self.df.columns

        if(category == "None" or category == None):
            data = self.df.values
        else:
            data = self.df[self.df['category'] == category].values
        
        total = len(data)

        categories= self.df["category"].unique()
        pagination = Pagination(page=page, total=total)

        return header, data,categories, pagination

    def export(self, page):
        if page == 0:
            data = self.df
        else:
            data = self.df[(page - 1) * 10: 10 * (page)]

        filename = "./data/" + str(time.time()) + ".csv"
        return data, filename

    def save(self, data, page):
        # self.df[(page - 1) * 10 : 10 * (page)] = data\
        data = pd.DataFrame(data=data, columns=self.df.columns)
        self.df = pd.concat(
            [
                self.df.loc[: (page - 1) * 10 - 1],
                data,
                self.df.loc[10 * page:],
            ]
        ).reset_index(drop=True)
        self.df.to_csv("./data/personal_transactions.csv", index=False)
        return self.df

    def delete(self, id):
        index = self.df[self.df.id == id].index
        self.df = self.df.drop(index)
        self.df.to_csv("./data/personal_transactions.csv", index=False)
        return self.df
