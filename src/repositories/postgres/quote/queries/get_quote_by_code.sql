select
	q.content, q.company_id, qt.quote_type,	q.code
from
	personal."Quote" q
inner join personal."Quote_Type" qt 
	on q.quote_type_id = qt.id
where q.code = %(code)s