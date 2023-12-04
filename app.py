from flask import Flask, Response, send_file
from flask import render_template
from flask import request
from flask_paginate import Pagination, get_page_parameter
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from controllers.StatisticController import StatisticController
from controllers.ExportCSVController import ExportCSVController

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
        print(pagination.per_page)
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


@app.route("/export-csv")
def export():
    csvController = ExportCSVController()

    page = int(request.args.get("page", 1))

    data, filename = csvController.export(page)
    return Response(
        data.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=" + filename},
    )
