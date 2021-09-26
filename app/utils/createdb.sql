create table polls(
    id integer primary key,
    poll text not null
);

create table choices(
    id integer primary key,
    poll_id integer references polls(id) not null,
    choice text not null,
    voices integer default 0,
    FOREIGN KEY(poll_id) REFERENCES polls(id)
);