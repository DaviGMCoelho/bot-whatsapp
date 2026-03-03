insert into 
	personal."Item"
	(
		company_id,
		code,
		name,
		description,
		price,
		catalog_id,
		active
	)
values
	(
		%(company_id)s,
		%(code)s,
		%(name)s,
		%(description)s,
		%(price)s,
		%(catalog_id)s,
		%(active)s
	)
returning id;