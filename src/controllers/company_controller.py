from src.domains.models.DTOs.company.update_company_dto import UpdateCompanyDTO
from src.services.company_service import CompanyService
from src.domains.models.DTOs.company.create_company_dto import CreateCompanyDTO
from src.domains.models.DTOs.address.create_address_dto import CreateAddressRequestDTO

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
        treated_address = {}
        raw_address =  {
            'active': address_request.get('active'),
            'code': address_request.get('code'),
            'state': address_request.get('estado'),
            'city': address_request.get('cidade'),
            'neighborhood': address_request.get('bairro'),
            'street': address_request.get('rua'),
            'number': address_request.get('numero'),
            'postal_code': address_request.get('cep'),
            'complement': address_request.get('complemento')
        }

        for key, value in raw_address.items():
            if value is not None:
                treated_address[key] = value

        return treated_address

    def _normalize_company(self, request: dict):
        name = request.get('name')
        cnpj = request.get('cnpj')
        work_days = self._organize_operation(request.get('operation'))
        return name, cnpj, work_days

    def register_company(self, request: dict):
        name, cnpj, work_days = self._normalize_company(request)
        address = self._organize_address(request.get('address'))
        company_dto = CreateCompanyDTO(name, cnpj, work_days)
        address_dto = CreateAddressRequestDTO(
            address['active'],
            address['code'],
            address['state'],
            address['city'],
            address['neighborhood'],
            address['street'],
            address['number'],
            address['postal_code'],
            address['complement'],
            company_id = ''
            )
        register = self.service.register_company(company_dto, address_dto)
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

    def update_company_address(self, request: dict):
        cnpj = request.get('cnpj')
        address = self._organize_address(request.get('address'))
        update_company_dto = UpdateCompanyDTO(cnpj=cnpj, address=address)
        update = self.service.update_company_address(update_company_dto)
        return update


    # ------- Change company state -------
    def change_company_state(self, request: dict):
        cnpj = request.get('cnpj')
        active = request.get('active')
        change_state_dto = UpdateCompanyDTO(cnpj=cnpj, active=active)
        change_state = self.service.change_company_state(change_state_dto)
        return change_state


    # ------- Change address state -------
    def change_address_state(self, request: dict):
        cnpj = request.get('cnpj')
        address = {
            'code': request.get('code'),
            'active': request.get('active')
        }
        change_state_dto = UpdateCompanyDTO(cnpj=cnpj, address=address)
        change_state = self.service.change_address_state(change_state_dto)
        return change_state

