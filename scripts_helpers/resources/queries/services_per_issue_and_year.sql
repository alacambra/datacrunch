select * from 
(select count(*) as total_10_11 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 1
HAVING 
	t > UNIX_TIMESTAMP("2010-01-01") 
	and 
	t < UNIX_TIMESTAMP("2011-01-01")
) as tab) as t10_11,
(select count(*) as total_11_12 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 1
HAVING 
	t > UNIX_TIMESTAMP("2011-01-01") 
	and 
	t < UNIX_TIMESTAMP("2012-01-01")
) as tab) as t11_12,

(select count(*) as total_12_13 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  
FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 1
HAVING 
	t > UNIX_TIMESTAMP("2012-01-01") 
	and 
	t < UNIX_TIMESTAMP("2013-01-01")
) as tab) as t12_13,

(select count(*) as total_13_14 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 1
HAVING 
	t > UNIX_TIMESTAMP("2013-01-01") 
	and 
	t < UNIX_TIMESTAMP("2014-01-01")
) as tab) as t13_14

UNION

select * from 
(select count(*) as total_10_11 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 2
HAVING 
	t > UNIX_TIMESTAMP("2010-01-01") 
	and 
	t < UNIX_TIMESTAMP("2011-01-01")
) as tab) as t10_11,
(select count(*) as total_11_12 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 2
HAVING 
	t > UNIX_TIMESTAMP("2011-01-01") 
	and 
	t < UNIX_TIMESTAMP("2012-01-01")
) as tab) as t11_12,

(select count(*) as total_12_13 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  
FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 2
HAVING 
	t > UNIX_TIMESTAMP("2012-01-01") 
	and 
	t < UNIX_TIMESTAMP("2013-01-01")
) as tab) as t12_13,

(select count(*) as total_13_14 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 2
HAVING 
	t > UNIX_TIMESTAMP("2013-01-01") 
	and 
	t < UNIX_TIMESTAMP("2014-01-01")
) as tab) as t13_14

UNION

select * from 
(select count(*) as total_10_11 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 3
HAVING 
	t > UNIX_TIMESTAMP("2010-01-01") 
	and 
	t < UNIX_TIMESTAMP("2011-01-01")
) as tab) as t10_11,
(select count(*) as total_11_12 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 3
HAVING 
	t > UNIX_TIMESTAMP("2011-01-01") 
	and 
	t < UNIX_TIMESTAMP("2012-01-01")
) as tab) as t11_12,

(select count(*) as total_12_13 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  
FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 3
HAVING 
	t > UNIX_TIMESTAMP("2012-01-01") 
	and 
	t < UNIX_TIMESTAMP("2013-01-01")
) as tab) as t12_13,

(select count(*) as total_13_14 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 3
HAVING 
	t > UNIX_TIMESTAMP("2013-01-01") 
	and 
	t < UNIX_TIMESTAMP("2014-01-01")
) as tab) as t13_14

#order by created_on DESC

UNION

select * from 
(select count(*) as total_10_11 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 4
HAVING 
	t > UNIX_TIMESTAMP("2010-01-01") 
	and 
	t < UNIX_TIMESTAMP("2011-01-01")
) as tab) as t10_11,
(select count(*) as total_11_12 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 4
HAVING 
	t > UNIX_TIMESTAMP("2011-01-01") 
	and 
	t < UNIX_TIMESTAMP("2012-01-01")
) as tab) as t11_12,

(select count(*) as total_12_13 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  
FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 4
HAVING 
	t > UNIX_TIMESTAMP("2012-01-01") 
	and 
	t < UNIX_TIMESTAMP("2013-01-01")
) as tab) as t12_13,

(select count(*) as total_13_14 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 4
HAVING 
	t > UNIX_TIMESTAMP("2013-01-01") 
	and 
	t < UNIX_TIMESTAMP("2014-01-01")
) as tab) as t13_14

#order by created_on DESC

UNION

select * from 
(select count(*) as total_10_11 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 5
HAVING 
	t > UNIX_TIMESTAMP("2010-01-01") 
	and 
	t < UNIX_TIMESTAMP("2011-01-01")
) as tab) as t10_11,
(select count(*) as total_11_12 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 5
HAVING 
	t > UNIX_TIMESTAMP("2011-01-01") 
	and 
	t < UNIX_TIMESTAMP("2012-01-01")
) as tab) as t11_12,

(select count(*) as total_12_13 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  
FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 5
HAVING 
	t > UNIX_TIMESTAMP("2012-01-01") 
	and 
	t < UNIX_TIMESTAMP("2013-01-01")
) as tab) as t12_13,

(select count(*) as total_13_14 from (SELECT 
	UNIX_TIMESTAMP(i.created_on) as t, 
	i.created_on, 
	UNIX_TIMESTAMP(i.updated_on), 
	spi.total_services  

FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id 
where total_services = 5
HAVING 
	t > UNIX_TIMESTAMP("2013-01-01") 
	and 
	t < UNIX_TIMESTAMP("2014-01-01")
) as tab) as t13_14

#order by created_on DESC

