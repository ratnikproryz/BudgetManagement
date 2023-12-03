from flask import Flask
from flask import render_template
import csv
from flask import request
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)


@app.route("/")
def home():
    with open("./data/personal_transactions.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        page = int(request.args.get("page") or 1)
        data = list(csv_reader)
        total = len(data)
        per_page = 10
        pagination = Pagination(page=page, total=total)
        return render_template(
            "home.html",
            header=header,
            data=data[(page - 1) * 10 : 10 * (page)],
            pagination=pagination,
        )
