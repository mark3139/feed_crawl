charset utf8;
create table feed(
	id int auto_increment,
	title varchar(64) not null,
	link varchar(256) not null,
	subtitle varchar(128) null,
	image varchar(256) null,
	des varchar(512) not null,
	updated timestamp not null default current_timestamp,
	`type` enum('rss', 'atom') not null,
	sub_num int not null default 0,
    push_time enum('day', 'week') not null default 'day',
	hash char(32) not null,
	primary key(id),
	key title (title),
	unique key (hash)
) engine=myisam default charset=utf8;
