insert into 
	personal."items"
	(
		name,
		description,
		price,
		catalog_id,
		active
	)
values
	(
		%(name)s,
		%(description)s,
		%(price)s,
		%(catalog_id)s,
		%(active)s
	)
returning id;
