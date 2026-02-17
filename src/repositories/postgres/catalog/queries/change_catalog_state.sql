update personal."Catalog"
	set active = %(active)s
where 
	code = %(code)s
	and company_id = %(company_id)s