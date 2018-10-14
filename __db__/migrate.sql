CREATE TABLE source_file (
    code        uuid CONSTRAINT firstkey PRIMARY KEY,
    file_path   varchar(40) NOT NULL
);

insert into source_file (code, file_path) values
    ('bd141ba3-9047-445f-a90e-46261b1952bb', 'awrf34yf4h5gf24hf43.jpg');

commit ;