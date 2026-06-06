with missions as (
    select * from {{ ref('stg_missions') }}
)

select
    country,
    count(*)                                            as total_launches,
    sum(case when is_success then 1 else 0 end)         as successful_launches,
    round(
        sum(case when is_success then 1 else 0 end)::numeric
        / count(*) * 100, 1
    )                                                   as success_rate_pct,
    min(launch_year)                                    as first_launch_year
from missions
group by country
order by total_launches desc
