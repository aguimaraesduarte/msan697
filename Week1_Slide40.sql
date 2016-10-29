--select name, min(score)
--from (businesses left join inspections using(business_id)) as lhs
--left join
--violations
--using(business_id)
--where description like 'Improper food storage'
--group by 1;

select name, min(score)
from
(select businesses.name as name, businesses.business_id as business_id
from businesses
join violations
on businesses.business_id = violations.business_id
where violations.description like '%Improper food storage%') as business_violation
left join
inspections
on businesses.business_id = inspections.business_id
group by name;