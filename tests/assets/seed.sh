set -xe

mkdir -p /tmp/mysqldump_analyzer_dumps/

# dump.sql
export DB="db"
export DUMP="dump.sql"
mysql -u root -e "create database $DB"
mysql -u root $DB << EOM
    create table table_a (
        column_a1 int primary key,
        column_a2 int null,
        column_a3 varchar(100),
        column_a4 bool,
        column_a5 TEXT,
        index (column_a2),
        index idx_column_a2 (column_a2)
    )
EOM
mysql -u root $DB << EOM
    create table table_b (
        column_b1 int primary key,
        column_b2 int,
        column_b3 int not null,
        foreign key (column_b2) references table_a (column_a1)
    )
EOM
mysql -u root $DB -e "alter table table_a add foreign key (column_a2) references table_b (column_b1)"
mysqldump -u root $DB --no-data > /tmp/mysqldump_analyzer_dumps/$DUMP

# dump_other.sql
export DB="db_other"
export DUMP="dump_other.sql"
mysql -u root -e "create database $DB"
mysql -u root $DB << EOM
    create table table_a (
        column_a1 int primary key,
        column_a2 int null,
        column_a3 varchar(100),
        column_a4 bool,
        column_a5 TEXT,
        index (column_a2)
    )
EOM
mysql -u root $DB << EOM
    create table table_b (
        column_b1 int primary key,
        column_b2 int null,
        column_b3 int,
        column_b4 int not null
    )
EOM
mysql -u root $DB -e "alter table table_a add foreign key (column_a2) references table_b (column_b1)"
mysqldump -u root $DB --no-data > /tmp/mysqldump_analyzer_dumps/$DUMP

# dump_another.sql
export DB="db_another"
export DUMP="dump_another.sql"
mysql -u root -e "create database $DB"
mysql -u root $DB << EOM
    create table table_a (
        column_a1 int primary key,
        column_a2 int null,
        column_a3 varchar(100),
        column_a4 bool,
        column_a5 TEXT,
        index (column_a2)
    )
EOM
mysqldump -u root $DB --no-data > /tmp/mysqldump_analyzer_dumps/$DUMP

exit 0
