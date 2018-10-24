CREATE TABLE public.source_file (
  code        uuid CONSTRAINT firstkey PRIMARY KEY,
  file_path   varchar(40) NOT NULL
);

insert into public.source_file (code, file_path) values
  ('bd141ba3-9047-445f-a90e-46261b1952bb', 'awrf34yf4h5gf24hf43.jpg');

CREATE TABLE public.merch
(
  uuid uuid PRIMARY KEY NOT NULL,
  name varchar(255) NOT NULL,
  description text
);
CREATE UNIQUE INDEX merch_uuid_uindex ON public.merch (uuid);
COMMENT ON TABLE public.merch IS 'description of product';

CREATE TABLE public.merch_file
(
    id serial PRIMARY KEY NOT NULL,
    merch_uuid uuid NOT NULL,
    file_uuid uuid NOT NULL,
    CONSTRAINT merch_file___fk_merch FOREIGN KEY (merch_uuid) REFERENCES public.merch (uuid),
    CONSTRAINT merch_file___fk_file FOREIGN KEY (file_uuid) REFERENCES public.source_file (code)
);

commit ;