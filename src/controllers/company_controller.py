from src.domains.models.DTOs.update_company_dto import UpdateCompanyDTO
from src.services.company_service import CompanyService
from src.domains.models.DTOs.create_company_dto import CreateCompanyDTO

class CompanyController:
    def __init__(self, service: CompanyService):
        self.service = service

    def _organize_operation(self, operation_request: dict):
        days = {}
        for key, value in operation_request.items():
            day, topic = key.split('_', 1)
            if day not in days:
                days[day] = {
                        'day': day,
                        'open_at': None,
                        'close_at': None,
                        'active': False
                    }
            if topic == 'abre':
                days[day]['open_at'] = value
            elif topic == 'fecha':
                days[day]['close_at'] = value
            elif topic == 'ativo':
                days[day]['active'] = value == 'on'
        return {'operation': list(days.values())}

    def _organize_address(self, address_request: dict):
        address =  {
            'estado': address_request.get('estado'),
            'cidade': address_request.get('cidade'),
            'bairro': address_request.get('bairro'),
            'rua': address_request.get('rua'),
            'numero': address_request.get('numero'),
            'cep': address_request.get('cep'),
            'complemento': address_request.get('complemento')
        }
        return address

    def _normalize_company(self, request: dict):
        name = request.get('name')
        cnpj = request.get('cnpj')
        work_days = self._organize_operation(request.get('operation'))
        address = self._organize_address(request.get('address'))
        return name, cnpj, work_days, address

    def register_company(self, request: dict):
        name, cnpj, work_days, address = self._normalize_company(request)
        company_dto = CreateCompanyDTO(name, work_days, address, cnpj)
        register = self.service.register_company(company_dto)
        return register

    def update_company_base(self, request: dict):
        name = request.get('name')
        cnpj = request.get('cnpj')
        active = request.get('active')
        update_company_dto = UpdateCompanyDTO(cnpj=cnpj, name=name, active=active)
        update = self.service.update_company_base(update_company_dto)
        return update

    def update_company_operation(self, request: dict):
        cnpj = request.get('cnpj')
        operation = self._organize_operation(request.get('operation'))
        update_company_dto = UpdateCompanyDTO(operation=operation, cnpj=cnpj)
        update = self.service.update_company_operation(update_company_dto)
        return update
