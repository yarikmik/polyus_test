from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_test import db
from flask_test.models import Products
from flask_test.products.forms import AddProductsForm

products = Blueprint('products', __name__)


@products.route("/allproducts")
def allproducts():
    """таблица всех товаров"""
    page = request.args.get('page', 1, type=int)
    products = Products.query.order_by(Products.selling_cost.desc()).paginate(page=page, per_page=5)
    return render_template('allproducts.html', products=products)


@products.route("/allproducts/new", methods=['GET', 'POST'])
def new_product():
    """добавить новый товар"""
    form = AddProductsForm()
    if form.validate_on_submit():
        product = Products(product_name=form.product_name.data,
                           purchase_cost=form.purchase_cost.data,
                           selling_cost=form.selling_cost.data)

        try:
            db.session.add(product)
            db.session.commit()
        except Exception:
            flash('Ошибка добавления продукта', 'warning')
            return redirect(url_for('products.allproducts'))

        flash('Продукт добавлен', 'success')
        return redirect(url_for('products.allproducts'))
    return render_template('add_products.html',
                           form=form,
                           legend='Новый продукт')


@products.route("/allproducts/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    """обновление товара"""
    product = Products.query.get_or_404(product_id)
    form = AddProductsForm()
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.purchase_cost = form.purchase_cost.data
        product.selling_cost = form.selling_cost.data

        try:
            db.session.commit()
        except Exception:
            flash('Ошибка обновления продукта', 'warning')
            return redirect(url_for('products.allproducts'))

        flash('Продукт обновлен', 'success')
        return redirect(url_for('products.allproducts'))
    elif request.method == 'GET':
        form.product_name.data = product.product_name
        form.purchase_cost.data = product.purchase_cost
        form.selling_cost.data = product.selling_cost
    return render_template('add_products.html', form=form, legend='Обновление покупателя')


@products.route("/allproducts/<int:product_id>/delete", methods=['GET', 'POST'])
def delete_product(product_id):
    """удаление товара"""
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Продукт удален', 'success')
    return redirect(url_for('products.allproducts'))
