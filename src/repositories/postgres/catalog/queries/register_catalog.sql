insert into personal."catalog"
(
	name,
	company_id,
	active
)
values
(
	%(name)s,
	%(company_id)s,
	%(active)s
)

returning id;