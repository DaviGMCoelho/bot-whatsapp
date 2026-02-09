select id, name, operation, active, cnpj
    from personal."Company"
	where cnpj = %(cnpj)s;