from flask import render_template, url_for, flash, redirect, request, Blueprint
from sqlalchemy import func, desc
from flask_test import db
from flask_test.models import Purchases, Buyers

report = Blueprint('report', __name__)


@report.route("/report")
def build_report():
    report_page = request.args.get('page', 1, type=int)
    report_rows = db.session.query(Purchases.purchase_date, Buyers.username,
                                   func.sum(Purchases.total_cost).label('total'))\
                             .join(Buyers, Purchases.buyer_id==Buyers.id)\
                             .group_by(Buyers.username).order_by(desc('total'))\
                             .paginate(page=report_page, per_page=5)
    print(report_rows.items)
    return render_template('report.html', report_rows=report_rows)
