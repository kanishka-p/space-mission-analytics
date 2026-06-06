with missions as (
    select * from "postgres"."analytics_staging"."stg_missions"
)

select
    launch_year,
    launch_decade,
    count(*)                                            as total_launches,
    sum(case when is_success then 1 else 0 end)         as successful_launches,
    sum(case when not is_success then 1 else 0 end)     as failed_launches,
    round(
        sum(case when is_success then 1 else 0 end)::numeric
        / count(*) * 100, 1
    )                                                   as success_rate_pct
from missions
group by launch_year, launch_decade
order by launch_year