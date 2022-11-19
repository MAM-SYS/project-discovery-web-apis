select *
    join scanned_domains on scanned_sub_domains.domain_id = scanned_domain.scan_id
    from scanned_sub_domains
where row_n=1 and scanned_domain.scan_id={scan_id};
