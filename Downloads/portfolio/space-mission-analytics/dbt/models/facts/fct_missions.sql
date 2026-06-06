with missions as (
    select * from {{ ref('stg_missions') }}
)

select
    mission_name,
    company,
    rocket,
    country,
    launch_date,
    launch_year,
    launch_decade,
    rocket_status,
    mission_status,
    is_success,
    sector,
    cost_usd_millions
from missions
