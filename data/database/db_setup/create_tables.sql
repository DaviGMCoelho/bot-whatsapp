CREATE SCHEMA IF NOT EXISTS personal;

CREATE TABLE personal.Tax_type(
    id int generated always as identity primary key,
    tax_type varchar(10)
);

CREATE TABLE personal.Company(
    id int generated always as identity primary key,
    tax_type_id int not null references personal.Tax_type(id) ON DELETE RESTRICT,
    tax_code varchar(50) not null,
    name varchar(50) not null,
    operation jsonb not null,
    active boolean not null default TRUE
);

CREATE TABLE personal.Customer(
    id int generated always as identity primary key,
    name varchar(50) not null,
    remoteJid text unique not null
);

CREATE TABLE personal.Session_Status(
    id int generated always as identity primary key,
    status varchar(50) not null
);

CREATE TABLE personal.Session(
    id int generated always as identity primary key,
    status_id int not null references personal.Session_Status(id) ON DELETE RESTRICT,
    customer_id int not null references personal.Customer(id) ON DELETE CASCADE,
    company_id int not null references personal.Company(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ not null default CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ,
    closed_at TIMESTAMPTZ,
    summary jsonb not null
);

CREATE TABLE personal.Address(
    id int generated always as identity primary key,
    state varchar(100) not null,
    city varchar(100) not null,
    neighborhood varchar(100) not null,
    street varchar(255) not null,
    number varchar(20) not null,
    postal_code varchar(20) not null,
    complement varchar(255),
    label varchar(100),
    company_id int not null references personal.Company(id) ON DELETE CASCADE
);

CREATE TABLE personal.Instance_Hub(
    id int generated always as identity primary key,
    name varchar(255) not null,
    company_id int not null references personal.Company(id) ON DELETE CASCADE,
    instance_id text not null
);

CREATE TABLE personal.Offer(
    id int generated always as identity primary key,
    offer varchar(30) not null
);

CREATE TABLE personal.Catalog(
    id int generated always as identity primary key,
    name varchar(30) not null,
    description text,
    company_id int not null references personal.Company(id) ON DELETE CASCADE,
    offer_id int not null references personal.Offer(id) ON DELETE NO ACTION,
    active boolean not null default TRUE
);

CREATE TABLE personal.Items(
    id int generated always as identity primary key,
    name varchar(20) not null,
    description TEXT not null,
    price numeric(10,2) not null,
    catalog_id int not null references personal.Catalog(id) ON DELETE CASCADE,
    active boolean not null default TRUE
);