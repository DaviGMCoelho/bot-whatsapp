from flask import Flask

from src.routes.website_routes import website_bp
from src.routes.webhook_routes import webhook_bp

import os
from dotenv import load_dotenv

def create_app():
    app = Flask(
        __name__,
        template_folder=r'src\views\templates',
        static_folder=r'src\views\static'
    )
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.register_blueprint(website_bp)
    app.register_blueprint(webhook_bp)

    return app

app_instance = create_app()
app_instance.run(host='0.0.0.0', port=5000, debug=True)
