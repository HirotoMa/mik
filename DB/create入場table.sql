create table t_enter(
user_id varchar(16) not null  comment '���[�U�[ID', 
enter_time DATETIME not null DEFAULT CURRENT_TIMESTAMP comment '���ꎞ��',
 PRIMARY KEY (user_id,enter_time)
)
comment='����e�[�u��';