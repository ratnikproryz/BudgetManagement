from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


class StatisticController:
    def __init__(self):
        self.df = pd.read_csv("./data/personal_transactions.csv")

    def getYears(self):
        self.df["date"] = pd.to_datetime(self.df["date"])
        years = self.df["date"].dt.year.unique()
        return years

    def generateImage(self, fig):
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode("utf8")

        return pngImageB64String

    def generatePie(self, top):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)

        category = self.df["category"].value_counts()
        axis.pie(category[0:top], labels=category[0:top].index, autopct="%.2f")

        return self.generateImage(fig)

    def generateBar(self, year):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)

        self.df["date"] = pd.to_datetime(self.df["date"])
        filter_data = self.df.loc[self.df["date"].dt.year == year]

        amount = filter_data["amount"].values
        month = filter_data["date"].dt.month.values

        axis.set_xlabel("Month")
        axis.set_ylabel("Amount")
        axis.set_title("Spending of All Months")
        month = filter_data["date"].dt.month.values
        axis.autoscale(enable=True, axis="x", tight=True)
        axis.bar(month, amount)

        return self.generateImage(fig)
