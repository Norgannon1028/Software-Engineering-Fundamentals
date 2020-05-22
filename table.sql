PRAGMA foreign_keys = ON;

CREATE table User(
    id  integer PRIMARY KEY autoincrement, 
    username  VARCHAR(30) not null unique,
    password VARCHAR(30) not null,
    email VARCHAR(30) not null,
    sex int check(sex=0 or sex=1),
    old int check(old>0 and old<150),
    time text not null
)
go

CREATE table Blog(
    id  integer PRIMARY KEY autoincrement, 
    userid  INT not null REFERENCES User(id),
    title VARCHAR(30) not null,
    keyword VARCHAR(255) not null,
    like int not null,
    link VARCHAR(255) not null,
    time text not null
)
go

CREATE table File(
    id  integer PRIMARY KEY autoincrement, 
    userid  INT not null REFERENCES User(id),
    link VARCHAR(255) not null
)
go

CREATE table Follow(
    id  integer PRIMARY KEY autoincrement, 
    toid  INT not null REFERENCES User(id),
    fromid  INT not null REFERENCES User(id)
)
go

CREATE table Comment(
    id  integer PRIMARY KEY autoincrement, 
    userid  INT not null REFERENCES User(id),
    blogid  INT not null REFERENCES Blog(id),
    content text not null,
    time text not null
)
go
CREATE table Like(
    id  integer PRIMARY KEY autoincrement, 
    userid  INT not null REFERENCES User(id),
    blogid  INT not null REFERENCES Blog(id),
    time text not null
)
go

insert into User (username,password,email,time) values('admin','admin','test@test.com',date('now'));
insert into Blog (userid,keyword,like,link,title,time) values(1,'test',0,'./test.md','test title',date('now'));