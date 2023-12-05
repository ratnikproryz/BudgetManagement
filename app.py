from flask import Flask, Response, redirect
from flask import render_template
from flask import request
import json

from controllers.StatisticController import StatisticController
from controllers.CSVController import CSVController

app = Flask(__name__)


@app.route("/")
def home():
    csvController = CSVController()

    page = int(request.args.get("page", 1))
    header, data, pagination = csvController.index(page)
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
    csvController = CSVController()

    page = int(request.args.get("page", 1))
    data, filename = csvController.export(page)

    return Response(
        data.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=" + filename},
    )


@app.route("/save-csv", methods=["POST"])
def save_csv():
    data = json.loads(request.data)
    data = list(filter(None, data))
    page = int(request.args.get("page", 1))

    csvController = CSVController()
    csvController.save(data, page)

    return redirect("/" + "?page=" + str(page))


@app.route("/delete/<int:id>")
def delete(id):
    csvController = CSVController()
    csvController.delete(id)
    page = int(request.args.get("page", 1))

    return redirect("/" + "?page=" + str(page))
