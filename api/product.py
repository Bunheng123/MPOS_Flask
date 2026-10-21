from flask import jsonify, request
from api import api_bp
from product import products, get_product_by_id, get_product_by_category


@api_bp.get('/products', endpoint='get_products')
@api_bp.get('/product', endpoint='get_product_list')
def api_products():
    category = request.args.get('category')
    search = request.args.get('q')

    result = products
    if category:
        result = [p for p in result if p.get('category', '').lower() == category.lower()]
    if search:
        search_lower = search.lower()
        result = [
            p for p in result
            if search_lower in p.get('name', '').lower()
            or search_lower in p.get('description', '').lower()
        ]

    return jsonify({
        "success": True,
        "count": len(result),
        "data": result
    })


@api_bp.get('/products/<int:product_id>', endpoint='get_product_by_id')
@api_bp.get('/product/<int:product_id>', endpoint='get_product_detail')
def api_product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({
            "success": False,
            "error": "Product not found"
        }), 404

    return jsonify({
        "success": True,
        "data": product
    })


@api_bp.get('/products/categories', endpoint='get_product_categories')
def api_product_categories():
    categories = sorted(list({p.get('category') for p in products if p.get('category')}))
    return jsonify({
        "success": True,
        "categories": categories
    })
