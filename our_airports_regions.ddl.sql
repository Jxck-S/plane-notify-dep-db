-- public.our_airports_regions definition

-- Drop table

-- DROP TABLE public.our_airports_regions;

CREATE TABLE public.our_airports_regions (
	id int4 NOT NULL,
	code varchar NULL,
	local_code varchar NULL,
	"name" varchar NULL,
	continent varchar NULL,
	iso_country varchar NULL,
	wikipedia_link varchar NULL,
	keywords varchar NULL,
	CONSTRAINT our_airports_regions_id PRIMARY KEY (id)
);