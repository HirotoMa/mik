create table t_leave(
user_id varchar(16) not null  comment 'ユーザーID', 
leave_time DATETIME not null DEFAULT CURRENT_TIMESTAMP comment '退場時刻',
 PRIMARY KEY (user_id,leave_time)
)
comment='退場テーブル';