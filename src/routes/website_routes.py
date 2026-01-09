from flask import Blueprint, render_template, request, current_app, redirect, url_for, session

website_bp = Blueprint("register", __name__, url_prefix='/register')

@website_bp.route('/address', methods=['GET', 'POST'])
def register_address():
    if request.method == 'POST':
        session['address'] = request.form.to_dict()
        return redirect(url_for('register.register_operation'))
    return render_template('register_address.html', titulo='Endereço')

@website_bp.route('/operation', methods=['GET', 'POST'])
def register_operation():
    controller = current_app.container['company_controller']
    if request.method == 'POST':
        operation = request.form.to_dict()
        address = session.get('address')
        data = {
            'address': address,
            'operation': operation
        }
        data = controller.register_company(data)
    return render_template('register_operation.html', titulo='Funcionamento')
