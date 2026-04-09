select id, name, operation, active, cnpj
    from personal."Company"
	where id = %(company_id)s;