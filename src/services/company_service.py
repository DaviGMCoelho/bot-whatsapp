from datetime import datetime

from src.repositories.postgres.company.company_repository import CompanyRepository
from src.repositories.postgres.address.address_repository import AddressRepository
from src.database.connection_pg import PostgresConn
from src.domains.models.DTOs.create_company_dto import CreateCompanyDTO
from src.domains.models.company import Company
from src.domains.models.address import Address
from src.domains.value_objects.operation import Operation
from src.domains.value_objects.business_hours import BusinessHours


class CompanyService:
    def __init__(self, psql_conn: PostgresConn, company_repo: CompanyRepository, address_repo: AddressRepository):
        self.company_repo_psql = company_repo
        self.address_repo_psql = address_repo
        self.psql_conn = psql_conn

    def _create_operation(self, operation_dto: dict):
        operation = operation_dto
        days = []
        for day in operation['operation']:
            opens_at = None
            closes_at = None

            if day['active']:
                opens_at = datetime.strptime(day['open_at'], "%H:%M").time()
                closes_at = datetime.strptime(day['close_at'], "%H:%M").time()

            daily_hour = BusinessHours(
                day['day'],
                opens_at,
                closes_at,
                day['active']
                )
            days.append(daily_hour)
        return Operation(days)

    def _convert_to_model(self, create_company_dto: CreateCompanyDTO):
        company_name = create_company_dto.name
        operation = self._create_operation(create_company_dto.operation)
        address_dto = create_company_dto.address

        company = Company(company_name, operation)
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


    def register_company(self, create_company_dto: CreateCompanyDTO):
        try:
            company, address = self._convert_to_model(create_company_dto)
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
