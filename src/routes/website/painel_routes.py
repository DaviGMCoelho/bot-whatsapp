from flask import Blueprint, render_template, request, current_app
from src.controller_container import Container


painel_bp = Blueprint("painel", __name__, url_prefix='/painel')

@painel_bp.route('/', methods=["GET"])
def home_page():
    return render_template('dashboard.html')

@painel_bp.route('/sua-empresa', methods=["GET"])
def your_company():
    container: Container = current_app.container
    vm = container.company.your_company_page({'current_company': 1})
    return render_template('your_company.html', company = vm)

@painel_bp.route('/produtos', methods=["GET"])
def products():
    return render_template('products.html')

@painel_bp.route('/desempenho', methods=["GET"])
def performance():
    return render_template('performance.html')
