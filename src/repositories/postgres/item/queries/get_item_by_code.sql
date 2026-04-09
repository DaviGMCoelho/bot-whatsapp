select 
    i.id,
    i.company_id,
    com.name,
    i.code,
    i.name,
    i.description,
    i.price,
    i.catalog_id,
    cat.name,
    i.active

from personal."Item" i
    inner join personal."Catalog" cat
    	on i.catalog_id = cat.id 
    inner join personal."Company" com
    	on i.company_id = com.id 
where i.code = %(item_code)s
    and i.company_id = %(company_id)s