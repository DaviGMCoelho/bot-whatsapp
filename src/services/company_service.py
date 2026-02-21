from datetime import datetime
import json

from src.services.base_service import BaseService
from src.repositories.postgres.company.company_repository import CompanyRepository
from src.repositories.postgres.address.address_repository import AddressRepository
from src.database.connection_pg import PostgresConn
from src.domains.models.DTOs.create_company_dto import CreateCompanyDTO
from src.domains.models.DTOs.update_company_dto import UpdateCompanyDTO
from src.domains.models.company import Company
from src.domains.models.address import Address
from src.domains.value_objects.operation import Operation
from src.domains.value_objects.business_hours import BusinessHours


class CompanyService(BaseService):
    def __init__(
            self,
            psql_conn: PostgresConn,
            company_repo: CompanyRepository,
            address_repo: AddressRepository
    ):
        self.company_repo_psql = company_repo
        self.address_repo_psql = address_repo
        self.psql_conn = psql_conn

    def _create_operation(self, operation_dto: dict):
        operation = operation_dto
        days = []
        for day in operation['operation']:
            open_at = None
            close_at = None

            if day['active']:
                open_at = datetime.strptime(day['open_at'], "%H:%M").time()
                close_at = datetime.strptime(day['close_at'], "%H:%M").time()

            daily_hour = BusinessHours(
                day['day'],
                open_at,
                close_at,
                day['active']
                )
            days.append(daily_hour)
        return Operation(days)

    def _convert_to_company_model(self, create_company_dto: CreateCompanyDTO):
        company_name = create_company_dto.name
        company_cnpj = create_company_dto.cnpj
        operation = self._create_operation(create_company_dto.operation)
        address_dto = create_company_dto.address

        company = Company(company_name, operation, company_cnpj)
        address = Address(
            state = address_dto.get('estado'),
            city = address_dto.get('cidade'),
            neighborhood = address_dto.get('bairro'),
            street = address_dto.get('rua'),
            number = address_dto.get('numero'),
            postal_code = address_dto.get('cep'),
            complement = address_dto.get('complemento'),
        )
        return company, address

    def _merge_operation(self, current_operation_json: str, new_operation: dict):
        current_operation = json.loads(current_operation_json) if isinstance(current_operation_json, str) else current_operation_json
        current_days= {day['day']: day for day in current_operation.get('weekly_hours', [])}
        new_days_list = new_operation.get('operation', [])

        for new_day in new_days_list:
            day_name = new_day['day']
            if day_name in current_days:
                if 'open_at' in new_day and new_day['open_at'] is not None:
                    current_days[day_name]['open_at'] = new_day['open_at']
                if 'close_at' in new_day and new_day['close_at'] is not None:
                    current_days[day_name]['close_at'] = new_day['close_at']
                if 'active' in new_day:
                    current_days[day_name]['active'] = new_day['active']
            else:
                current_days[day_name] = new_day

        return {
            'operation': list(current_days.values())
        }


    def register_company(self, create_company_dto: CreateCompanyDTO):
        try:
            company, address = self._convert_to_company_model(create_company_dto)
            with self.psql_conn.transaction() as conn:
                company_id = self.company_repo_psql.company_data_register(conn, company)
                address.company_id = company_id
                self.address_repo_psql.insert(conn, address)

            return {
                'status': 'success',
                'message': 'Empresa registrada corretamente'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


    def update_company_base(self, update_company_dto: UpdateCompanyDTO):
        try:
            data = update_company_dto.to_base_dict()
            with self.psql_conn.connect() as conn:
                self.company_repo_psql.update(conn, update_company_dto.cnpj, data)
            return {
                'status':'sucess',
                'message': 'Dados básicos atualizados com sucesso'                
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


    def update_company_operation(self, update_company_dto: UpdateCompanyDTO):
        if not update_company_dto.operation:
            raise ValueError("Operation é obrigatório para a atualização")

        with self.psql_conn.connect() as conn:
            current_operation = self.company_repo_psql.get_company_operation(
                conn, update_company_dto.cnpj
            )
            if not current_operation:
                raise ValueError('Empresa não encontrada')

            if isinstance(current_operation, dict):
                current_operation = json.dumps(current_operation)

            merged_operation_dict = self._merge_operation(current_operation, update_company_dto.operation)
            operation = self._create_operation(merged_operation_dict)
            data = {'operation': operation.to_json()}

            self.company_repo_psql.update(conn, update_company_dto.cnpj, data)


    def update_company_address(self, update_company_dto: UpdateCompanyDTO):
        if not update_company_dto.address:
            raise ValueError("Address é obrigatório para a atualização")

        with self.psql_conn.connect() as conn:
            company_id = self.company_repo_psql.get_company_by_cnpj(conn, update_company_dto.cnpj)[0]
            self.address_repo_psql.update(conn, company_id, update_company_dto.address['code'], update_company_dto.address)

    def change_company_state(self, update_company_dto: UpdateCompanyDTO):
        is_active = self._translate_state(update_company_dto.active)

        with self.psql_conn.connect() as conn:
            company_id = self.company_repo_psql.get_company_by_cnpj(conn, update_company_dto.cnpj)[0]
            self.company_repo_psql.change_state(conn, company_id, is_active)

