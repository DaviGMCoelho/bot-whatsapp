from flask import request, Blueprint
from src.controller.webhook_controller import WebhookController

def create_webhook_blueprint(webhook_controller: WebhookController):
    webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')

    @webhook_bp.route("/", methods=['POST'])
    def webhook():
        data = request.get_json()
        return webhook_controller.handle_webhook(data)

    return webhook_bp

def register_webhook_blueprint(app, webhook_controller: WebhookController):
    blueprint = create_webhook_blueprint(webhook_controller)
    app.register_blueprint(blueprint)
