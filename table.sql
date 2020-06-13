PRAGMA foreign_keys = ON;

CREATE table User(
    id INTEGER primary key AUTOINCREMENT,
    username  VARCHAR(30) not null unique,
    password VARCHAR(30) not null,
    email VARCHAR(30) not null,
    sex int check(sex=0 or sex=1),
    old int check(old>0 and old<150),
    time text not null,
    avatar TEXT not null default 'http://127.0.0.1:5000/static/default_avatar.jpg'
)
go

CREATE table Blog(
    id INTEGER primary key AUTOINCREMENT,
    userid  INTEGER not null REFERENCES User(id),
    title VARCHAR(30) not null,
    keyword VARCHAR(255) not null,
    like INTEGER not null,
    link text not null,
    time text not null
)
go

CREATE table File(
    id INTEGER primary key AUTOINCREMENT,
    userid  INTEGER not null REFERENCES User(id),
    filename Text not null,
    link VARCHAR(255) not null,
    time text not null 
)
go

CREATE table Follow(
    id INTEGER primary key AUTOINCREMENT,
    toid  INTEGER not null REFERENCES User(id),
    fromid  INTEGER not null REFERENCES User(id)
)
go

CREATE table Comment(
    id INTEGER primary key AUTOINCREMENT,
    userid  INTEGER not null REFERENCES User(id),
    blogid  INTEGER not null REFERENCES Blog(id),
    content text not null,
    time text not null
)
go
CREATE table Like(
    id INTEGER primary key AUTOINCREMENT,
    userid  INTEGER not null REFERENCES User(id),
    blogid  INTEGER not null REFERENCES Blog(id),
    time text not null
)
go
CREATE table Draft(
    id INTEGER primary key AUTOINCREMENT,
    userid  INTEGER not null REFERENCES User(id),
    title VARCHAR(30) not null,
    keyword VARCHAR(255) not null,
    link text not null,
    time text not null
)
go

alter table User RENAME TO olduser
go
alter table Blog RENAME TO oldblog
go
alter table Draft RENAME TO olddraft
go
alter table Like RENAME TO oldlike
go
alter table Comment RENAME TO oldcomment
go
alter table Follow RENAME TO oldfollow
go
alter table File RENAME TO oldfile
go


insert into User select * from olduser
go
insert into Blog select * from oldblog
go
insert into Draft select * from olddraft
go
insert into Like select * from oldlike
go
insert into Comment select * from oldcomment
go
insert into Follow select * from oldfollow
go
insert into File select * from oldfile
go

drop table olduser
go
drop table oldblog
go
drop table oldcomment
go
drop table oldfile
go
drop table oldfollow
go
drop table olddraft
go
drop table oldlike
go