create table if not exists scanned_domains(
    scan_id uuid not null constraint domain_pkey primary key,
    domain varchar(20) not null,
    date timestamp,
    status varchar(25) check( status IN ('Ongoing','Finished','Error') )  not null default 'Ongoing'
);
