update personal."Quote"
    set {{set_clause}}
where code = %(quote_code)s
    and company_id = %(company_id)s
returning id;