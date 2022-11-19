create table if not exists scanned_sub_domains(
    scan_id uuid not null primary key,
    sub_domain varchar(20) not null,
    scan_log varchar,
    domain_id uuid not null,
    FOREIGN KEY(domain_id) REFERENCES scanned_domains(scan_id)
);