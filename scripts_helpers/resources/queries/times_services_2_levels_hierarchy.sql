select 
#	c1.service as s1,
#	c2.service as s2,
	e1.name,
	count(*) as total,
	e2.name
from 
	(select 
		i.id,
		i.parent_id,
		te.activity_id as service
	from
		issues as i,
		time_entries as te
	where 
		i.id = te.issue_id
		and i.parent_id <> 0
		AND i.created_on > "2012-01-01"
		AND i.created_on < "2013-01-01"
		
	group by
		i.id,
		te.activity_id) as c1,
	
	(select
		i.id,
		i.parent_id,
		te.activity_id as service
	from
		issues as i,
		time_entries as te
	where 
		i.id = te.issue_id
		and i.parent_id <> 0
		AND i.created_on > "2012-01-01"	
		AND i.created_on < "2013-01-01"		
	group by 
		i.id,
		te.activity_id) as c2,
	enumerations as e1,
	enumerations as e2

where 
	c2.parent_id = c1.parent_id
	and c2.id <> c1.id
	and c1.service <> c2.service
	and e1.id = c1.service
	and e2.id = c2.service

group by
	c1.service, c2.service

order by c1.service,c2.service desc

limit 100000




