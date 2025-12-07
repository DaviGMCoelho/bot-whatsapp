from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm

website_bp = Blueprint("manager", __name__)

@website_bp.route('/register', methods=['GET', 'POST'])
def manager():
    if request.method == 'POST':
        data = request.form.to_dict()
        return f'{data}'
    return render_template('address.html', titulo='Endereço')
