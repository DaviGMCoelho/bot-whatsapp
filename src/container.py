from flask import Flask

#from src.clients.evolution_client import EvolutionClient
#from src.clients.gemini_client import GeminiClient
from src.database.chroma_db.connection import ChromaConn
from src.database.connection_pg import PostgresConn
from src.database.migrations import init_database
#from src.repositories.postgres.message.message_repository import MessageRepository
from src.repositories.postgres.company.company_repository import CompanyRepository
from src.repositories.postgres.address.address_repository import AddressRepository
from src.repositories.postgres.catalog.catalog_repository import CatalogRepository
from src.repositories.postgres.item.item_repository import ItemRepository

#from src.services.evolution_service import EvolutionService
#from src.services.gemini_service import GeminiService
#from src.services.message_service import MessageService
from src.services.company_service import CompanyService
from src.services.catalog_service import CatalogService
from src.services.item_service import ItemService

#from src.controllers.message_controller import MessageController
from src.controllers.company_controller import CompanyController
from src.controllers.catalog_controller import CatalogController
from src.controllers.item_controller import ItemController


def init_dependencies(app: Flask):
    #evolution_cfg = app.config["EVOLUTION"]
    #gemini_cfg = app.config["GEMINI"]
    postgres_cfg = app.config["POSTGRES"]
    chromadb_cfg = app.config["CHROMADB"]

    #evolution_client = EvolutionClient(
    #    evolution_cfg["EVOLUTION_API"],
    #    evolution_cfg["EVOLUTION_HOST"]
    #   )

    #gemini_client = GeminiClient(
    #    gemini_cfg["GOOGLE_API"]
    #)

    conn_chromadb = ChromaConn(
        chromadb_cfg["CHROMADB_HOST"],
        chromadb_cfg["CHROMADB_PORT"]
    )

    conn_postgres = PostgresConn(
        postgres_cfg["PSQL_DB"],
        postgres_cfg["PSQL_USER"],
        postgres_cfg["PSQL_PASSWORD"],
        postgres_cfg["PSQL_HOST"],
        postgres_cfg["PSQL_PORT"]
        )
    #psql_message_repo = MessageRepository()
    psql_company_repo = CompanyRepository()
    psql_address_repo = AddressRepository()
    psql_catalog_repo = CatalogRepository()
    psql_item_repo = ItemRepository()

    if app.config["POSTGRES"]["PSQL_MIGRATIONS"] is True:
        init_database(conn_postgres)

    #evolution_service = EvolutionService(evolution_client)
    #gemini_service = GeminiService(gemini_client, gemini_cfg["CSV_PATH"])
    #message_service = MessageService(conn_postgres, evolution_service, gemini_service, psql_message_repo)
    company_service = CompanyService(conn_postgres, psql_company_repo, psql_address_repo)
    catalog_service = CatalogService(conn_postgres, psql_catalog_repo, psql_company_repo)
    item_service = ItemService(conn_postgres, psql_company_repo, psql_catalog_repo, psql_item_repo)

    #message_controller = MessageController(message_service)
    company_controller = CompanyController(company_service)
    catalog_controller = CatalogController(catalog_service)
    item_controller = ItemController(item_service)

    app.container = {
        #"message_controller": message_controller,
        "company_controller": company_controller,
        "catalog_controller": catalog_controller,
        "item_controller": item_controller
    }