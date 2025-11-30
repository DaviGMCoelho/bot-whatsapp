from flask import Blueprint, render_template

website_bp = Blueprint("manager", __name__)

@website_bp.route('/manager')
def manager():
    return render_template('manager.html', titulo='Configurações')
