with missions as (
    select * from {{ ref('stg_missions') }}
),

agency_stats as (
    select
        company,
        sector,
        count(*)                                            as total_launches,
        sum(case when is_success then 1 else 0 end)         as successful_launches,
        round(
            sum(case when is_success then 1 else 0 end)::numeric
            / count(*) * 100, 1
        )                                                   as success_rate_pct,
        min(launch_year)                                    as first_launch_year,
        max(launch_year)                                    as last_launch_year,
        round(avg(cost_usd_millions)::numeric, 2)           as avg_cost_usd_millions
    from missions
    group by company, sector
)

select * from agency_stats
order by total_launches desc
