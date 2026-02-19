select id, code, name, active 
	from personal."Catalog"
	where code = %(code)s
	    and company_id = %(company_id)s