with select_with_row_number as(
    select row_number() over (partition by domain order by date desc) as row_n,
            *
    from scanned_domains
)
select * from select_with_row_number where row_n=1;
