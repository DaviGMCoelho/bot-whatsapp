import os
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask

from src.container import init_dependencies
from src.routes.website_routes import website_bp
from src.routes.webhook_routes import webhook_bp
from src.routes.website.product_routes import product_bp

def create_app():
    load_dotenv()

    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir / "src" / "views"
    csv_path = os.path.join(base_dir, "data", "base_dados.csv")

    instance = Flask(
        __name__,
        template_folder = str(src_dir / "templates"),
        static_folder = str(src_dir / "static")
    )

    instance.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    instance.config["GEMINI"] = {
        "GOOGLE_API": os.getenv("GOOGLE_API_KEY"),
        "CSV_PATH": str(csv_path)
    }
    instance.config["EVOLUTION"] = {
        "EVOLUTION_API": os.getenv("AUTHENTICATION_API_KEY"),
        "EVOLUTION_HOST": os.getenv("EVOLUTION_API_HOST", "evolution-api")
    }
    instance.config["CHROMADB"] = {
        "CHROMADB_HOST": os.getenv("CHROMADB_HOST"),
        "CHROMADB_PORT": os.getenv("CHROMADB_PORT")
    }
    instance.config["POSTGRES"] = {
        "PSQL_MIGRATIONS": os.getenv("POSTGRES_RUN_MIGRATIONS") == "true",
        "PSQL_DB": os.getenv("POSTGRES_DB"),
        "PSQL_USER": os.getenv("POSTGRES_USER"),
        "PSQL_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "PSQL_HOST": os.getenv("POSTGRES_HOST"),
        "PSQL_PORT": int(os.getenv("POSTGRES_PORT", "5432"))
    }

    init_dependencies(instance)

    instance.register_blueprint(website_bp)
    instance.register_blueprint(webhook_bp)
    instance.register_blueprint(product_bp)

    return instance

app = create_app()

if __name__ == '__main__':
    debug = os.getenv("FLASK_ENV") == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug)
