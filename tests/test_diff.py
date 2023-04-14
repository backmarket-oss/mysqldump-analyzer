from mysqldump_analyzer.diff import diff_dbs, diff_tables


def test_diff_tables_missing_index(table_a, table_a_other):
    result = diff_tables(db1=table_a, db2=table_a_other)
    assert result["indexes"] == {
        "idx_column_a2": {
            "db1": "index `idx_column_a2` on (`column_a2`)",
            "db2": "missing",
        }
    }


def test_diff_tables_columns(table_b, table_b_other):
    result = diff_tables(db1=table_b, db2=table_b_other)
    assert result["columns"] == {
        "column_b3": {
            "db1": "column `column_b3` int(11) not null",
            "db2": "column `column_b3` int(11) default null",
        },
        "column_b4": {
            "db1": "missing",
            "db2": "column `column_b4` int(11) not null",
        },
    }


def test_diff_tables_foreign_keys(table_b, table_b_other):
    result = diff_tables(db1=table_b, db2=table_b_other)
    assert result["foreign_keys"] == {
        "table_b_ibfk_1": {
            "db1": "foreign key `table_b_ibfk_1` reference to `table_a`.`column_a1`",
            "db2": "missing",
        }
    }


def test_diff_dbs(db, db_other, db_another, expected_diff):
    result = diff_dbs(db1=db, db2=db_other, db3=db_another)
    assert result == expected_diff
