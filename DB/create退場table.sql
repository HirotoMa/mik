create table t_leave(
user_id varchar(16) not null  comment '���[�U�[ID', 
leave_time DATETIME not null DEFAULT CURRENT_TIMESTAMP comment '�ޏꎞ��',
 PRIMARY KEY (user_id,leave_time)
)
comment='�ޏ�e�[�u��';