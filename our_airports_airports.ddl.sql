-- public.our_airports_airports definition

-- Drop table

-- DROP TABLE public.our_airports_airports;

CREATE TABLE public.our_airports_airports (
	id int4 NOT NULL,
	ident varchar(10) NOT NULL,
	"type" varchar(255) NULL,
	name varchar(255) NULL,
	lat float4 NULL,
	lon float4 NULL,
	elev int4 NULL,
	continent varchar(5) NULL,
	iso_country varchar(5) NULL,
	iso_region varchar(10) NULL,
	municipality varchar(255) NULL,
	scheduled_service varchar(5) NULL,
	gps_code varchar(10) NULL,
	iata_code varchar(10) NULL,
	local_code varchar(10) NULL,
	home_link varchar(255) NULL,
	wikipedia_link varchar(255) NULL,
	keywords varchar(1000) NULL,
	CONSTRAINT airports_pkey PRIMARY KEY (ident)
);