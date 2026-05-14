-- TOP 5 products by revenue within each category

with product_sales as (

    select
        category,
        item,
        sum(line_total) as total_revenue
    from fact_sales fs
    join dim_products dp
        on fs.product_id = dp.product_id
    group by
        category,
        item
),

ranked_products as (

    select
        category,
        item,
        total_revenue,
        row_number() over (
            partition by category
            order by total_revenue desc
        ) as rn
    from product_sales
)

select
    category,
    item,
    total_revenue
from ranked_products
where rn <= 5;

-- Monthly customer retention

with customer_months as (

    select distinct
        customer_id,
        date_trunc('month', sale_date) as month_start
    from fact_sales
),

next_month_activity as (

    select
        current_month.customer_id,
        current_month.month_start as current_month,
        next_month.month_start as next_month
    from customer_months current_month
    left join customer_months next_month
        on current_month.customer_id = next_month.customer_id
        and next_month.month_start =
            current_month.month_start + interval '1 month'
)

select
    current_month,
    count(distinct customer_id) as customers,
    count(distinct case
        when next_month is not null
        then customer_id
    end) as retained_customers,

    round(
        count(distinct case
            when next_month is not null
            then customer_id
        end
        ) * 100.0
        /
        count(distinct customer_id),
        2
    ) as retention_rate_pct

from next_month_activity
group by current_month
order by current_month;


-- Customers without purchases

select
    dc.customer_id,
    dc.customer_type
from dim_customers dc
left join fact_sales fs
    on dc.customer_id = fs.customer_id
where fs.customer_id is null;