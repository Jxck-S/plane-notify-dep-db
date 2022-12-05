-- public.adsbx_ac definition

-- Drop table

-- DROP TABLE public.adsbx_ac;

CREATE TABLE public.adsbx_ac (
	icao varchar(6) NOT NULL,
	reg varchar(20) NULL,
	icaotype varchar(8) NULL,
	"year" varchar(4) NULL,
	manufacturer varchar(200) NULL,
	model varchar(200) NULL,
	ownop varchar(255) NULL,
	faa_pia bool NULL,
	faa_ladd bool NULL,
	short_type varchar(5) NULL,
	mil bool NULL,
	CONSTRAINT icao_unique PRIMARY KEY (icao)
);