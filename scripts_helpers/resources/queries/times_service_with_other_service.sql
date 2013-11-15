select s1, sum(t.times) 
from
	(select 
		t1.name as s1,
		count(*) as times,
		t2.name as s2
	from
		(select 
			te.activity_id as service_id, 
			i.id as issue_id,
			e.name as name
		from
			issues as i, 
			time_entries as te,
			enumerations as e
		where 
			i.id = te.issue_id
			and e.id = te.activity_id
			AND i.created_on < "2014-01-01"
			AND i.created_on > "2013-01-01"
		group by i.id, te.activity_id 
		) as t1,

		(select 
			te.activity_id as service_id, 
			i.id as issue_id,
			e.name as name
		from
			issues as i, 
			time_entries as te,
			enumerations as e
		where 
			i.id = te.issue_id
			and e.id = te.activity_id
			AND i.created_on < "2014-01-01"
			AND i.created_on > "2013-01-01"
		group by i.id, te.activity_id 
		) as t2

	where 
		t1.service_id <> t2.service_id
		and t1.issue_id = t2.issue_id
	group by s1, s2) as t
group by s1

