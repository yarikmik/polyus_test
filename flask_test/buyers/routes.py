from flask import render_template, Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_test import db
from flask_test.models import Buyers
from flask_test.buyers.forms import (AddBuyersForm)

buyers = Blueprint('buyers', __name__)


@buyers.route("/allbuyers")
def allbuyers():
    page = request.args.get('page', 1, type=int)
    buyers = Buyers.query.order_by(Buyers.registration_date.desc()).paginate(page=page, per_page=5)
    return render_template('allbuyers.html', buyers=buyers)


@buyers.route("/allbuyers/new", methods=['GET', 'POST'])
def new_buyer():
    form = AddBuyersForm()
    if form.validate_on_submit():
        buyer = Buyers(username=form.username.data,
                       year_of_birth=form.year_of_birth.data,
                       gender=form.gender.data,
                       # registration_date=form.registration_date.data,
                       consent=form.consent.data,
                       image_file=form.image_file.data)

        try:
            db.session.add(buyer)
            db.session.commit()
        except Exception:
            flash('Ошибка добавления покупателя', 'warning')
            return redirect(url_for('buyers.allbuyers'))

        flash('Покупатель добавлен', 'success')
        return redirect(url_for('buyers.allbuyers'))
    return render_template('add_buyers.html',
                           form=form,
                           legend='Новый покупатель')


@buyers.route("/allbuyers/<int:buyer_id>/update", methods=['GET', 'POST'])
def update_buyer(buyer_id):
    buyer = Buyers.query.get_or_404(buyer_id)
    form = AddBuyersForm()
    if form.validate_on_submit():
        buyer.username = form.username.data
        buyer.year_of_birth = form.year_of_birth.data
        buyer.gender = form.gender.data
        buyer.consent = form.consent.data
        buyer.image_file = form.image_file.data if form.image_file.data else 'default.png'

        try:
            db.session.commit()
        except Exception:
            flash('Ошибка обновления покупателя', 'warning')
            return redirect(url_for('buyers.allbuyers'))

        flash('Покупатель обновлен', 'success')
        return redirect(url_for('buyers.allbuyers'))
    elif request.method == 'GET':
        form.username.data = buyer.username
        form.year_of_birth.data = buyer.year_of_birth
        form.gender.data = buyer.gender
        form.consent.data = buyer.consent
        form.image_file.data = buyer.image_file
    return render_template('add_buyers.html', form=form, legend='Обновление покупателя')


@buyers.route("/allbuyers/<int:buyer_id>/delete", methods=['GET', 'POST'])
def delete_buyer(buyer_id):
    buyer = Buyers.query.get_or_404(buyer_id)
    db.session.delete(buyer)
    db.session.commit()
    flash('Покупатель удален', 'success')
    return redirect(url_for('buyers.allbuyers'))
