select distinct on (qt.quote_type) id
from personal."Quote_Type" qt
where qt.quote_type = %(quote_type)s
	and (qt.company_id is null or qt.company_id = %(company_id)s)
order by
	qt.quote_type,
	case
		when qt.company_id = %(company_id)s then 0
		else 1 
	end;