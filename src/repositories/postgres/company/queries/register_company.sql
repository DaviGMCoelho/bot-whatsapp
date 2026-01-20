insert into 
	personal.Company
	(
		name,
		operation,
		cnpj
	)
values
	(
		%(name)s,
		%(operation)s::jsonb,
		%(cnpj)%s
	)
RETURNING id;