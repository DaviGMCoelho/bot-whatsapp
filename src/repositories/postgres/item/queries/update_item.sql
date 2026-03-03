update personal."Item"
    set {{set_clause}}
where code = %(code)s
    and company_id = %(company_id)s
    and catalog_id = %(catalog_id)s