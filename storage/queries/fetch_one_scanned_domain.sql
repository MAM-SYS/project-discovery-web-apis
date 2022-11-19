select * from scanned_domains
join scanned_sub_domains on scanned_domains.scan_id = scanned_sub_domains.domain_id
where scanned_domains.scan_id="{scan_id}";