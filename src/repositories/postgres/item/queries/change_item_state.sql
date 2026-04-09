update personal."Item"
	set active = %(active)s
where 
	code = %(code)s
	and company_id = %(company_id)s
    and catalog_id = %(catalog_id)s
returning id;
