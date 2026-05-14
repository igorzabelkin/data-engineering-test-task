create table dim_customers (
    customer_id int primary key,
    customer_type varchar(50)
);


create table dim_products (
    product_id int primary key,
    item varchar(255),
    category varchar(255)
);


create table fact_sales (
    invoice_id bigint,
    sale_date date,
    customer_id int,
    product_id int,
    quantity int,
    price decimal(10,2),
    line_total decimal(12,2),

    foreign key (customer_id)
        references dim_customers(customer_id),

    foreign key (product_id)
        references dim_products(product_id)
);