CREATE SCHEMA IF NOT EXISTS personal;

CREATE TABLE personal."Company"(
    id int generated always as identity primary key,
    name varchar(50) not null,
    operation jsonb not null,
    active boolean not null default true,
    cnpj char(14) unique not null
);

CREATE TABLE personal."Customer"(
    id int generated always as identity primary key,
    name varchar(50) not null,
    remoteJid text unique not null
);

CREATE TABLE personal."Session_Status"(
    id int generated always as identity primary key,
    status varchar(50) not null
);

CREATE TABLE personal."Catalog"(
    id int generated always as identity primary key,
    code char(7) not null unique,
    name varchar(30) not null,
    company_id int not null references personal."Company"(id) ON DELETE CASCADE,
    active boolean not null default TRUE
);

CREATE TABLE personal."Item"(
    id int generated always as identity primary key,
    company_id int not null references personal."Company"(id) ON DELETE CASCADE,
    code char(7) not null unique,
    name varchar(30) not null,
    description TEXT not null,
    price numeric(10,2) not null,
    catalog_id int not null references personal."Catalog"(id) ON DELETE CASCADE,
    active boolean not null default TRUE
);

CREATE TABLE personal."Address"(
    id int generated always as identity primary key,
    active boolean not null default TRUE,
    code char(7) not null unique,
    state varchar(100) not null,
    city varchar(100) not null,
    neighborhood varchar(100) not null,
    street varchar(255) not null,
    number varchar(20) not null,
    postal_code varchar(20) not null,
    complement varchar(255),
    label varchar(100),
    company_id int not null references personal."Company"(id) ON DELETE CASCADE
);

CREATE TABLE personal."Instance_Hub"(
    id int generated always as identity primary key,
    name varchar(255) not null,
    company_id int not null references personal."Company"(id) ON DELETE CASCADE,
    instance_id text not null
);

CREATE TABLE personal."Credentials"(
    id int generated always as identity primary key,
    company_id int not null references personal."Company"(id) ON DELETE CASCADE,
    credential TEXT not null
);

CREATE TABLE personal."Session"(
    id int generated always as identity primary key,
    code char(15) not null unique,
    status_id int not null references personal."Session_Status"(id) ON DELETE RESTRICT,
    customer_id int not null references personal."Customer"(id) ON DELETE CASCADE,
    company_id int not null references personal."Company"(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ not null default CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ,
    closed_at TIMESTAMPTZ,
    summary jsonb not null
);

create table personal."Quote_Type"(
	id int generated always as identity primary key,
	quote_type varchar(50) not null,
    is_default boolean not null default false,
    company_id int null references personal."Company"(id) on delete cascade,
    active boolean not null default true,

    constraint unique_name_per_scope unique (quote_type, company_id),
    constraint check_default_or_company
    check(
        (is_default = true and company_id is null)
        or
        (is_default = false and company_id is not null)
    )
);

create table personal."Quote"(
	id int generated always as identity primary key,
	company_id int not null references personal."Company"(id) on delete cascade,
	quote_type_id int not null references personal."Quote_Type"(id) on delete restrict,
	content TEXT not null,
	active bool not null default true,
    code char(7) not null,

    constraint unique_code_per_scope unique (code, company_id)
);

create table personal."Memory_Type"(
	id int generated always as identity primary key,
	memory_type varchar(50) not null,
    description TEXT not null,
    active boolean not null default true,
    created_at timestamptz default now() not null
);

create table personal."Memory"(
	id int generated always as identity primary key,
	customer_id int not null references personal."Customer"(id) on delete cascade,
	memory_type_id int not null references personal."Memory_Type"(id),
	company_id int not null references personal."Company"(id) on delete cascade,
	content text not null,
	created_at timestamptz default now() not null,
	updated_at timestamptz default now() not null
);
