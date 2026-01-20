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
        name = self._organize_operation(request.get('name')) or 'EmpresaTeste'
        cnpj = self._organize_operation(request.get('cnpj')) or 'CNPJTeste'
        work_days = self._organize_operation(request.get('operation'))
        address = self._organize_address(request.get('address'))
        return name, cnpj, work_days, address

    def register_company(self, request_raw: dict):
        name, work_days, address, cnpj = self._normalize_company(request_raw)
        company_dto = CreateCompanyDTO(name, work_days, address, cnpj)
        register = self.service.register_company(company_dto)
        return register
