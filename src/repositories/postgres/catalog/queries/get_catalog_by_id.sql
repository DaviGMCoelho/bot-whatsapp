select id, code, name, active 
	from personal."Catalog"
	where id = %(catalog_id)s