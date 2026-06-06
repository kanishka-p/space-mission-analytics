with source as (
    select * from public.raw_space_missions
),

cleaned as (
    select
        mission                                         as mission_name,
        company,
        rocket,
        location,
        country,
        date::date                                      as launch_date,
        year::int                                       as launch_year,
        decade::int                                     as launch_decade,
        rocketstatus                                    as rocket_status,
        missionstatus                                   as mission_status,
        price                                           as cost_usd_millions,
        case
            when missionstatus = 'Success' then true
            else false
        end                                             as is_success,
        case
            when company in (
                'SpaceX', 'Rocket Lab', 'Blue Origin',
                'Virgin Orbit', 'Arianespace', 'ULA'
            ) then 'Commercial'
            else 'Government'
        end                                             as sector
    from source
    where date is not null
)

select * from cleaned
