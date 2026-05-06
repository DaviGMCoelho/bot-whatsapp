update personal."Quote"
	set active = %(active)s
where 
	code = %(code)s
	and company_id = %(company_id)s
returning id;
