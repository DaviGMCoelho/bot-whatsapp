from flask import Blueprint, render_template, request, current_app

painel_bp = Blueprint("painel", __name__, url_prefix='/painel')

@painel_bp.route('/', methods=["GET"])
def home_page():
    return render_template('dashboard.html')

@painel_bp.route('/sua-empresa', methods=["GET"])
def your_company():
    return render_template('your_company.html')

@painel_bp.route('/produtos', methods=["GET"])
def products():
    return render_template('products.html')

@painel_bp.route('/desempenho', methods=["GET"])
def performance():
    return render_template('performance.html')