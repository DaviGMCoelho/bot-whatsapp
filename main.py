from flask import Flask
from src.routes.webhook_routes import register_webhook_blueprint
from src.controller.webhook_controller import WebhookController
from src.services.webhook_service import WebhookService

def create_app():
    app = Flask(__name__)
    webhook_service = WebhookService()
    webhook_controller = WebhookController(webhook_service)
    register_webhook_blueprint(app, webhook_controller)
    return app

app = create_app()
app.run(host="0.0.0.0", port=5000, debug=True)
