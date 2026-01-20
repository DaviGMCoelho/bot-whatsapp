insert into 
	personal."Item"
	(
		code,
		name,
		description,
		price,
		catalog_id,
		active
	)
values
	(
		%(code)s,
		%(name)s,
		%(description)s,
		%(price)s,
		%(catalog_id)s,
		%(active)s
	)
returning id;