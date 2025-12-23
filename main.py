import os
from dotenv import load_dotenv
from pathlib import Path

from flask import Flask

from src.routes.website_routes import website_bp
from src.routes.webhook_routes import webhook_bp


def create_app():
    load_dotenv()

    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir / "src" / "views"

    instance = Flask(
        __name__,
        template_folder = str(src_dir / "templates"),
        static_folder = str(src_dir / "static")
    )

    instance.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    instance.register_blueprint(website_bp)
    instance.register_blueprint(webhook_bp)

    return instance

app = create_app()

if __name__ == '__main__':
    debug = os.getenv("FLASK_ENV") == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug)
