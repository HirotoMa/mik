create table m_user(
user_id varchar(16) not null PRIMARY KEY comment 'ユーザーID', 
user_name varchar(16) not null comment 'ユーザー名', 
user_password varchar(16)not null UNIQUE comment 'ユーザーパスワード', 
user_IDm varchar(16) not null comment 'ユーザーIDm(IDmは、FeliCaのICチップ製造時に、ICチップに記録され書き換えができない固有のID番号)'
)
comment='ユーザーテーブル';
