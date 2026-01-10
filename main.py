import os
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask

from src.clients.evolution_client import EvolutionClient
from src.clients.gemini_client import GeminiClient

from src.database.connection_pg import PostgresConn
from src.database.migrations import init_database
from src.repositories.postgres.message.message_repository import MessageRepository
from src.repositories.postgres.company.company_repository import CompanyRepository
from src.repositories.postgres.address.address_repository import AddressRepository
from src.repositories.postgres.catalog.catalog_repository import CatalogRepository
from src.repositories.postgres.item.item_repository import ItemRepository

from src.services.evolution_service import EvolutionService
from src.services.gemini_service import GeminiService
from src.services.message_service import MessageService
from src.services.company_service import CompanyService
from src.services.catalog_service import CatalogService

from src.controllers.message_controller import MessageController
from src.controllers.company_controller import CompanyController
from src.controllers.catalog_controller import CatalogController

from src.routes.website_routes import website_bp
from src.routes.webhook_routes import webhook_bp
from src.routes.website.product_routes import product_bp

def init_dependencies(app: Flask):
    evolution_cfg = app.config["EVOLUTION"]
    gemini_cfg = app.config["GEMINI"]
    postgres_cfg = app.config["POSTGRES"]

    evolution_client = EvolutionClient(
        evolution_cfg["EVOLUTION_API"],
        evolution_cfg["EVOLUTION_HOST"]
        )

    gemini_client = GeminiClient(
        gemini_cfg["GOOGLE_API"]
    )

    conn_postgres = PostgresConn(
        postgres_cfg["PSQL_DB"],
        postgres_cfg["PSQL_USER"],
        postgres_cfg["PSQL_PASSWORD"],
        postgres_cfg["PSQL_HOST"],
        postgres_cfg["PSQL_PORT"]
        )
    psql_message_repo = MessageRepository()
    psql_company_repo = CompanyRepository()
    psql_address_repo = AddressRepository()
    psql_catalog_repo = CatalogRepository()
    psql_item_repo = ItemRepository()

    psql_item_repo.insert()

    if app.config["POSTGRES"]["PSQL_MIGRATIONS"] is True:
        init_database(conn_postgres)

    evolution_service = EvolutionService(evolution_client)
    gemini_service = GeminiService(gemini_client, gemini_cfg["CSV_PATH"])
    message_service = MessageService(conn_postgres, evolution_service, gemini_service, psql_message_repo)
    company_service = CompanyService(conn_postgres, psql_company_repo, psql_address_repo)
    catalog_service = CatalogService(conn_postgres, psql_catalog_repo, psql_company_repo)

    message_controller = MessageController(message_service)
    company_controller = CompanyController(company_service)
    catalog_controller = CatalogController(catalog_service)

    app.container = {
        "message_controller": message_controller,
        "company_controller": company_controller,
        "catalog_controller": catalog_controller
    }


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
