from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_test import db
from flask_test.models import Purchases, Buyers, Products
from flask_test.purchases.forms import AddPurchasesForm

purchases = Blueprint('purchases', __name__)


@purchases.route("/allpurchases")
def allpurchases():
    purchase = request.args.get('page', 1, type=int)
    purchases = db.session.query(Purchases.id, Purchases.purchase_date, Purchases.count, Purchases.total_cost,
                                 Purchases.unit_cost, Purchases.buyer_id, Buyers.username, Products.product_name) \
                            .join(Buyers, Purchases.buyer_id == Buyers.id) \
                            .join(Products, Purchases.product_id == Products.id) \
                            .order_by(Purchases.total_cost.desc()).paginate(page=purchase, per_page=5)
    return render_template('allpurchases.html', purchases=purchases)


@purchases.route("/allpurchases/new", methods=['GET', 'POST'])
def new_purchase():
    form = AddPurchasesForm()

    # обновляем список доступных товаров и продуктов
    buyer_list = [(u.username, u.username) for u in db.session.query(Buyers).all()]
    product_list = [(p.product_name, p.product_name) for p in db.session.query(Products).all()]
    form.buyer_name.choices = buyer_list
    form.product_name.choices = product_list

    if form.validate_on_submit():
        # дергаем экземпляры товара и покупателя по имени
        buyer = Buyers.query.filter_by(username=form.buyer_name.data).first_or_404()
        product = Products.query.filter_by(product_name=form.product_name.data).first_or_404()

        purchase = Purchases(purchase_date=form.purchase_date.data,
                             buyer_id=buyer.id,
                             product_id=product.id,
                             count=form.count.data,
                             unit_cost=product.selling_cost,  # добавляем стоимость продажи товара
                             total_cost=form.count.data * product.selling_cost)  # добавляем общую стоимость
        db.session.add(purchase)
        db.session.commit()
        flash('Покупка добавлена', 'success')
        return redirect(url_for('purchases.allpurchases'))
    return render_template('add_purchases.html',
                           form=form,
                           legend='Новая покупка')


@purchases.route("/allpurchases/<int:purchase_id>/update", methods=['GET', 'POST'])
def update_purchase(purchase_id):
    purchase = Purchases.query.get_or_404(purchase_id)
    form = AddPurchasesForm()

    if form.validate_on_submit():
        #  экземпляры товара и покупателя по имени
        buyer = Buyers.query.filter_by(username=form.buyer_name.data).first_or_404()
        product = Products.query.filter_by(product_name=form.product_name.data).first_or_404()

        purchase.purchase_date = form.purchase_date.data
        purchase.buyer_id = buyer.id
        purchase.product_id = product.id
        purchase.count = form.count.data
        purchase.unit_cost = product.selling_cost  # изменяем стоимость продажи товара
        purchase.total_cost = form.count.data * product.selling_cost  # изменяем общую стоимость

        db.session.commit()
        flash('Покупка изменена', 'success')
        return redirect(url_for('purchases.allpurchases'))
    elif request.method == 'GET':
        #  экземпляры товара и покупателя по id
        buyer = Buyers.query.filter_by(id=purchase.buyer_id).first_or_404()
        product = Products.query.filter_by(id=purchase.product_id).first_or_404()

        form.purchase_date.data = purchase.purchase_date
        form.buyer_name.data = buyer.username
        form.product_name.data = product.product_name
        form.count.data = purchase.count

    return render_template('add_purchases.html', form=form, legend='Изменение покупки')


@purchases.route("/allpurchases/<int:purchase_id>/delete", methods=['GET', 'POST'])
def delete_purchase(purchase_id):
    purchase = Purchases.query.get_or_404(purchase_id)
    db.session.delete(purchase)
    db.session.commit()
    flash('Покупка удалена', 'success')
    return redirect(url_for('purchases.allpurchases'))
