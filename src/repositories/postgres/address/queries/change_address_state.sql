update personal."Address"
	set active = %(active)s
where 
	company_id = %(company_id)s
    and code = %(address_code)s