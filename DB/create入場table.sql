create table t_enter(
user_id varchar(16) not null  comment 'ユーザーID', 
enter_time DATETIME not null DEFAULT CURRENT_TIMESTAMP comment '入場時刻',
 PRIMARY KEY (user_id,enter_time)
)
comment='入場テーブル';