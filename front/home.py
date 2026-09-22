from front import front_bp
from flask import render_template
from product import products

@front_bp.get('/')
def home():
    module = 'home'
    return render_template("front/home.html", products=products, module=module)
