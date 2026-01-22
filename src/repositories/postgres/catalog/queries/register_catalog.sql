insert into personal."Catalog"
(
	code,
	name,
	company_id,
	active
)
values
(
	%(code)s,
	%(name)s,
	%(company_id)s,
	%(active)s
)

returning id;