from src.controllers.company_controller import CompanyController
from src.controllers.catalog_controller import CatalogController
#from src.controllers.message_controller import MessageController
from src.controllers.item_controller import ItemController

class Container:
    def __init__(self, 
                 company_controller: CompanyController,
                 catalog_controller: CatalogController,
                 item_controller: ItemController
                ):
        self.company =  company_controller
        self.catalog =  catalog_controller
        #message_controller = message_controller
        self.item = item_controller
