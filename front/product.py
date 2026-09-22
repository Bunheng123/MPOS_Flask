from flask import render_template, abort
from front import front_bp
from product import products, get_product_by_id, get_product_by_category

@front_bp.get('/products', endpoint='products')
def all_products():
    module = 'products'
    return render_template("front/products.html", products=products, module=module)

@front_bp.get('/product/<int:product_id>', endpoint='product')
def product(product_id):
    module = 'product_detail'
    product_item = get_product_by_id(product_id)
    if product_item is None:
        abort(404)

    related_product = get_product_by_category(product_item['category'])
    return render_template(
        "front/product.html",
        product=product_item,
        related_product=related_product,
        module=module
    )