with missions as (
    select * from {{ ref('stg_missions') }}
),

rocket_stats as (
    select
        rocket,
        rocket_status,
        count(*)                                            as total_launches,
        sum(case when is_success then 1 else 0 end)         as successful_launches,
        round(
            sum(case when is_success then 1 else 0 end)::numeric
            / count(*) * 100, 1
        )                                                   as success_rate_pct,
        min(launch_year)                                    as first_launch_year,
        max(launch_year)                                    as last_launch_year,
        count(distinct company)                             as num_operators
    from missions
    group by rocket, rocket_status
)

select * from rocket_stats
order by total_launches desc
