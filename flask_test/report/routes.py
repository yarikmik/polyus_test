from flask import render_template, request, Blueprint
from sqlalchemy import func, desc
from flask_test import db
from flask_test.models import Purchases, Buyers
from flask_test.report.forms import SelectDateFrom

report = Blueprint('report', __name__)


@report.route("/report", methods=['GET', 'POST'])
def build_report():
    """Таблица отчета по покупателям и их общей сумме покупок"""
    form = SelectDateFrom()
    report_page = request.args.get('page', 1, type=int)

    if form.validate_on_submit():
        # если задействован фильтр по времении
        date_from = form.date_from.data
        print('date_from', date_from)
        report_rows = db.session.query(Purchases.purchase_date, Buyers.username,
                                       func.sum(Purchases.total_cost).label('total')) \
            .join(Buyers, Purchases.buyer_id == Buyers.id) \
            .group_by(Buyers.username).order_by(desc('total')).filter(Purchases.purchase_date >= date_from) \
            .paginate(page=report_page, per_page=5)
        return render_template('report.html', report_rows=report_rows, form=form)

    report_rows = db.session.query(Purchases.purchase_date, Buyers.username,
                                   func.sum(Purchases.total_cost).label('total')) \
        .join(Buyers, Purchases.buyer_id == Buyers.id) \
        .group_by(Buyers.username).order_by(desc('total')) \
        .paginate(page=report_page, per_page=5)
    return render_template('report.html', report_rows=report_rows, form=form)
