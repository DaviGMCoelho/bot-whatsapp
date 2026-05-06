insert into personal."Quote"
    (
        company_id,
        code,
        quote_type_id,
        content,
        active
    )
values
    (
        %(company_id)s,
        %(code)s,
        %(quote_type_id)s,
        %(content)s,
        %(active)s
    )
returning id;