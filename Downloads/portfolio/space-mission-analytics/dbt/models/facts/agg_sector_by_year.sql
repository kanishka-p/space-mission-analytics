with missions as (
    select * from {{ ref('stg_missions') }}
)

select
    launch_year,
    sector,
    count(*)                                            as total_launches,
    round(
        sum(case when is_success then 1 else 0 end)::numeric
        / count(*) * 100, 1
    )                                                   as success_rate_pct
from missions
group by launch_year, sector
order by launch_year, sector
