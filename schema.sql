charset utf8;
create table feeds(
	id int auto_increment,
	title varchar(64) not null,
	link varchar(256) not null,
	user_link varchar(256) not null,
	subtitle varchar(128) not null default '',
	image varchar(256) not null default '',
	des varchar(512) not null default '将要添加...',
	updated timestamp not null default current_timestamp,
	`type` enum('rss', 'atom') not null,
	sub_num int not null default 0,
    push_time enum('day', 'week') not null default 'day',
	hash char(32) not null,
	primary key(id),
	key title (title),
	unique key (hash)
) engine=myisam default charset=utf8;

create table items(
	id int auto_increment,
	fid int not null,
	title varchar(64) not null,
	link varchar(256) not null,
	des varchar(512) not null,
	category varchar(128) not null,
	author varchar(64) not null,
	pubdate timestamp not null,
	hash char(32) not null,
	primary key(id),
	unique key (hash)
) engine=myisam default charset=utf8;
