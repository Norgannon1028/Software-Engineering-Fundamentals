PRAGMA foreign_keys = ON;

CREATE table User(
    id INT primary key,
    username  VARCHAR(30) not null unique,
    password VARCHAR(30) not null,
    email VARCHAR(30) not null,
    sex int check(sex=0 or sex=1),
    old int check(old>0 and old<150),
    time text not null
)
go

CREATE table Blog(
    id INT primary key,
    userid  INT not null REFERENCES User(id),
    title VARCHAR(30) not null,
    keyword VARCHAR(255) not null,
    like int not null,
    link VARCHAR(255) not null,
    time text not null
)
go

CREATE table File(
    id INT primary key,
    userid  INT not null REFERENCES User(id),
    link VARCHAR(255) not null
)
go

CREATE table Follow(
    id INT primary key,
    toid  INT not null REFERENCES User(id),
    fromid  INT not null REFERENCES User(id)
)
go

CREATE table Comment(
    id INT primary key,
    userid  INT not null REFERENCES User(id),
    blogid  INT not null REFERENCES Blog(id),
    content text not null,
    time text not null
)
go
CREATE table Like(
    id INT primary key,
    userid  INT not null REFERENCES User(id),
    blogid  INT not null REFERENCES Blog(id),
    time text not null
)
go