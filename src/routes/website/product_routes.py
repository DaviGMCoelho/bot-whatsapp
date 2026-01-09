from flask import Blueprint, render_template, request, current_app


product_bp = Blueprint("product", __name__, url_prefix='/products')

@product_bp.route('/register', methods=['GET', 'POST'])
def register_product():
    if request.method == 'POST':
        return request.form.to_dict()
    return render_template('catalog_products.html', titulo='catalogo')
