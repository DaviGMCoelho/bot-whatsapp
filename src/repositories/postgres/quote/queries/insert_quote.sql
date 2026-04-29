insert into personal."Quote"
    (
        company_id,
        quote_type_id,
        content,
        active
    )
values
    (
        %(company_id)s,
        %(quote_type_id)s,
        %(content)s,
        %(active)s
    )
returning id;