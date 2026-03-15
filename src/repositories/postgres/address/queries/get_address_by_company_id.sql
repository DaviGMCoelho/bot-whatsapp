select
    id,
	active,
	code,
	state,
	city,
	neighborhood,
	street, 
	number, 
	postal_code, 
	complement, 
	label
from 
	personal."Address"
	where company_id = %(company_id)s