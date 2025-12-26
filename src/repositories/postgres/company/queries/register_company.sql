insert into 
	personal.company
	(
		name,
		operation
	)
values
	(
		%(name)s,
		%(operation)s::jsonb
	)
RETURNING id;