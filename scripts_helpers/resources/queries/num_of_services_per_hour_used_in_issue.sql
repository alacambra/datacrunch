#select services_per_hour, count(*) as total from (
select t.total_services/t.hours as services_per_hour from (
	SELECT 
		i.id, i.parent_id,
		tnsi.total_services as total_services, 
		sum(te.hours) as hours, 
		i.subject, 
		i.created_on, 
		due_date, 
		author_id
	FROM 
		issues as i, time_entries as te, total_number_of_services_per_issue as tnsi 
	where te.issue_id = i.id
		and tnsi.issue_id = i.id
		and hours <> 0
		AND i.created_on > "2013-01-01"
		AND due_date < NOW()
	group by i.id
	) as t
order by services_per_hour asc, total_services, hours
limit 10000
#) as t1
#group by services_per_hour
#order by total desc, services_per_hour

