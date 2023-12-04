from flask import Flask
from flask import render_template
from flask import request
from flask_paginate import Pagination, get_page_parameter
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from controllers.StatisticController import StatisticController

app = Flask(__name__)


@app.route("/")
def home():
    with open("./data/personal_transactions.csv", "r") as csv_file:
        df = pd.read_csv(csv_file)
        header = df.columns
        data = df.values
        page = int(request.args.get("page") or 1)
        total = len(data)
        pagination = Pagination(page=page, total=total)
        return render_template(
            "home.html",
            header=header,
            data=data[(page - 1) * 10 : 10 * (page)],
            pagination=pagination,
        )


@app.route("/statistic")
def statistic():
    statistic = StatisticController()

    top = int(request.args.get("top") or 3)
    pieChart = statistic.generatePie(top)

    year = int(request.args.get("year") or 2019)
    barChart = statistic.generateBar(year)
    years = statistic.getYears()

    return render_template(
        "statistic.html", pieChart=pieChart, barChart=barChart, years=years
    )
