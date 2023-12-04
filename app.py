from flask import Flask
from flask import render_template
from flask import request
from flask_paginate import Pagination, get_page_parameter
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    with open("./data/personal_transactions.csv", "r") as csv_file:
        df = pd.read_csv(csv_file)
        print(df.columns)
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
